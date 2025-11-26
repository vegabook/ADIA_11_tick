# ---------- convert large hdf5 to memory mappable parquet using pyarrow  ------------
# colorscheme lackluster-night

import h5py
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from loguru import logger

# directory constants
inH5dir = Path("./data/hdf5/ES.h5")
inH5file = inH5dir / "ES.h5"
setname = "trades_filter0vol" # "trades_filter0vol" or "trades"
outdir = Path("./data/rawinput") / setname
outdir.mkdir(exist_ok = True, parents = True)


def convert():
    with h5py.File("./data/hdf5/ES.h5", "r") as f:
        dset = f["tick"][setname]
        n_rows = dset.shape[0]
        chunk = int(10e6)
        print(f"total rows are {n_rows}, total chunks are {n_rows / chunk}")

        for iout, start in enumerate(range(0, n_rows, chunk)):
            data = dset[start:start + chunk]
            
            table = pa.Table.from_arrays([
                pa.array(data["Instrument"]),
                pa.array(data["Price"]),
                pa.array(data["Time"].astype('U17')),   # string
                pa.array(data["Volume"])
            ], names=["Instrument", "Price", "Time", "Volume"])\
            .sort_by([("Time", "ascending")])
            
            pq.write_table(table, outdir / f"es_{iout:04d}.parquet")
            logger.info(f"Wrote part {iout} – rows {start}–{start+len(data)}")


if __name__ == "__main__":
    convert()
