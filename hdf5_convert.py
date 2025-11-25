# ---------- convert ginormous hdf5 to memory mappable parquet using polars ------------

import h5py
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
from pathlib import Path
from loguru import logger

Path("data/parquet").mkdir(exist_ok=True)

with h5py.File("./data/hdf5/ES.h5", "r") as f:
    dset = f["tick"]["trades_filter0vol"]
    n_rows = dset.shape[0]
    chunk = 50_000_000
    print(f"total rows are {n_rows}, total chunks are {n_rows / chunk}")

    for i, start in enumerate(range(0, n_rows, chunk)):
        data = dset[start:start + chunk]
        
        table = pa.Table.from_arrays([
            pa.array(data["Instrument"]),
            pa.array(data["Price"]),
            pa.array(data["Time"].astype('U17')),   # string
            pa.array(data["Volume"])
        ], names=["Instrument", "Price", "Time", "Volume"])
        
        pq.write_table(table, f"data/parquet/es_{i:03d}.parquet")
        print(f"Wrote part {i} – rows {start}–{start+len(data)}")
