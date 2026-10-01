"""Clasificación didáctica con separación temporal y línea base."""
import json
from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

df = pd.read_parquet('datos/limpio.parquet').sort_values(['event_time', 'id'])
df['event_time'] = pd.to_datetime(df['event_time'])
df['hour'] = df['event_time'].dt.hour
df['late'] = (df['delivery_minutes'] > 60).astype(int)
cut = df['event_time'].quantile(0.8)
train, test = df[df.event_time < cut], df[df.event_time >= cut]
assert train.event_time.max() < test.event_time.min()
features = ['city', 'category', 'units', 'price_cents', 'hour']
X_train, y_train = train[features], train['late']
X_test, y_test = test[features], test['late']
prep = ColumnTransformer([
 ('cat', OneHotEncoder(handle_unknown='ignore'), ['city', 'category']),
 ('num', StandardScaler(), ['units', 'price_cents', 'hour'])],
 sparse_threshold=1.0)
model = Pipeline([('prep', prep), ('model', LogisticRegression(
    solver='liblinear', random_state=64, max_iter=1000))])
baseline = DummyClassifier(strategy='most_frequent')
output = {}
for name, estimator in [('baseline', baseline), ('logistic', model)]:
    estimator.fit(X_train, y_train)
    pred = estimator.predict(X_test)
    output[name] = dict(precision=precision_score(y_test, pred, zero_division=0),
     recall=recall_score(y_test, pred, zero_division=0),
     f1=f1_score(y_test, pred, zero_division=0),
     confusion_matrix=confusion_matrix(y_test, pred, labels=[0, 1]).tolist())
output['train_rows'], output['test_rows'] = len(train), len(test)
output['test_prevalence'] = float(y_test.mean())
Path('datos/metricas.json').write_text(json.dumps(output, indent=2))
print(json.dumps(output, indent=2))
