# --------------------- ADIA Question 11 Tick Data -------------------------------
# ------------- main parquet disk based lazy analysis routines -------------------
# --------------------------------------------------------------------------------
# colorscheme lackluster-hack

import polars as pl
from loguru import logger
from pathlib import Path
from rich.console import Console; console = Console()
from pprint import pprint
import IPython
import datetime as dt

from hdf5_convert import setname, outdir as indir
SETIN = indir / "*.parquet"
DIROUT = Path(__file__).resolve().parent / "data" / f"processed_{setname}"
DIROUT.mkdir(exist_ok = True, parents = True)


def unique_tickers(setfl):
    """ return unique tickers in the dataset """
    ccols = pl.scan_parquet(stfl)\
        .select("Instrument")\
        .unique()\
        .collect()
    return ccols

def columns(setfl):
    """column names"""
    return pl.read_parquet_schema(setfl)


def time_ranges(inp):
    """ First and last timestamp for each Instrument.
    Also akes sure there is no time range overlap so 
    that trs can be performed. 
    """
    ee = (
            pl.scan_parquet(inp, low_memory= True)
            .group_by("Instrument")
            .agg([pl.col("Time").min().alias("first_time"), 
                  pl.col("Time").max().alias("last_time")])
            .sort("last_time")
            .collect()
        )
    assert all(ee["last_time"][:-1] < ee["first_time"][1:])
    return ee


def trs_dv(inp, outp):
    """ Makes a total return series from all the prices in each contract.
    Uses polars lazy scans and is therefore able to operate on data sets bigger than memory.
    Algo: sort over time, group over instrument ('over'), take percentage returns
          make first nulls zero, cum_prod (returns+1), multiply by first price 
          in entire set.
    Also will add Volume x Price series dolvlm
    inp: string input file(s) 
    outp: string output file location
    """
    (
        pl.scan_parquet(inp, low_memory = True)
        .sort(["Time"])
        .with_columns(
            pl.col("Price")
                .pct_change()
                .over("Instrument", mapping_strategy  = "group_to_rows")
                # nulls between instruments to zero pct_change
                .fill_null(0)
                .alias("pct_change")
        )
        # back to series from pct returns
        .with_columns(
            (pl.col("pct_change") + 1)
            .cum_prod()
            .alias("pct_cumprod")
        )
        # multiple by first price
        .with_columns(
            (pl.col("pct_cumprod") * pl.col("Price").first()).alias("trs")
        ) 
        # add price x volumen column
        .with_columns((pl.col("Volume") * pl.col("price")).alias("dolvlm"))
        # lazy stream materialize and save to disk
        .sink_parquet(outp, compression = "zstd")
    )


if __name__ == "__main__":
    #ut = unique_tickers()
    #pprint(ut)
    #pprint(f"Count: {len(ut)}")
    nowtime = dt.datetime.now()
    ee = time_ranges(SETIN)
    logger.info(f"time_ranges time taken: {(dt.datetime.now() - nowtime).total_seconds()}")

    nowtime = dt.datetime.now()
    trs_dv(SETIN, DIROUT / "trs.parquet")
    logger.info(f"trs_dv time taken: {(dt.datetime.now() - nowtime).total_seconds()}")
    IPython.embed()



    

