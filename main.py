# --------------------- ADIA Question 11 Tick Data -------------------------------
# ------------- main parquet disk based lazy analysis routines -------------------
# --------------------------------------------------------------------------------
# colorscheme 

import polars as pl
from loguru import logger
from pathlib import Path
from rich.console import Console; console = Console()
from pprint import pprint

DATALOC = Path(__file__).resolve().parent / "data" / "parquet"
console.print(f"[bright blue]Data location set to {DATALOC}")

def unique_tickers():
    ccols = pl.scan_parquet(str(DATALOC))\
        .select("Instrument")\
        .unique()\
        .collect()
    return ccols
    
if __name__ == "__main__":
    ut = unique_tickers()
    pprint(ut)
    pprint(f"Count: {len(ut)}")
    

