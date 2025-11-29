# ---------- convert large hdf5 to memory mappable parquet using pyarrow  ------------
# colorscheme lackluster-night

import h5py
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from loguru import logger

# directory constants
inH5dir = Path("./data/hdf5")
inH5file = inH5dir / "ES.h5"
outdir = Path("./data/rawinput")


def convert(h5file, outpth, setname):
    with h5py.File(h5file, "r") as f:
        dset = f["tick"][setname]
        n_rows = dset.shape[0]
        chunk = int(10e6)
        logger.info(f"total rows are {n_rows}, total chunks are {n_rows / chunk}")

        for iout, start in enumerate(range(0, n_rows, chunk)):
            data = dset[start:start + chunk]
            
            table = pa.Table.from_arrays([
                pa.array(data["Instrument"]),
                pa.array(data["Price"]),
                pa.array(data["Time"].astype('U17')),   # string
                pa.array(data["Volume"])
            ], names=["Instrument", "Price", "Time", "Volume"])\
            .sort_by([("Time", "ascending")])
            
            pq.write_table(table, outpath / f"es_{iout:04d}.parquet")
            logger.info(f"Wrote part {iout} – rows {start}–{start+len(data)}")


if __name__ == "__main__":
    if not inH5file.exists():
        logger.error(f"Cannot find {inH5file}")
    else:
        outdir.mkdir(exist_ok = True, parents = True)
        convert(inH5file, outdir, "trades")
        convert(inH5file, outdir, "trades_filter0vol")

