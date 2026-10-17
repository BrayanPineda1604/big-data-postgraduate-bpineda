import polars as pl
from polars.testing import assert_frame_equal

consulta = pl.LazyFrame({"valor": [1, 2, 3]}).select(pl.col("valor").sum())
cpu = consulta.collect(engine="in-memory")
gpu = consulta.collect(engine=pl.GPUEngine(raise_on_fail=True))
assert gpu.item() == 6
assert_frame_equal(cpu, gpu)
print("Consulta GPU correcta:", gpu)