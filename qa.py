# --------------------- Question Answers -------------------------------
# colorscheme base16-atelier-heath-light
from pathlib import Path
import polars as pl; pl.Config(tbl_rows=50)
from loguru import logger
import numpy as np
import IPython
from scipy.stats import jarque_bera
import matplotlib.pyplot as plt
from pprint import pprint


# hourly bars
dpath = Path(__file__).resolve().parent / "data" 
dfiles = list(dpath.glob("*.parquet"))
dv_file = [x for x in dfiles if x.name.startswith("dolvlm")][0]
ts_file = [x for x in dfiles if x.name.startswith("Timestamp")][0]
vm_file = [x for x in dfiles if x.name.startswith("Volume")][0]

dv_file = Path(__file__).resolve().parent / "data" / "dolvlm_87217326_bars.parquet"
ts_file = Path(__file__).resolve().parent / "data" / "Timestamp_1h_bars.parquet"
vm_file = Path(__file__).resolve().parent / "data" / "Volume_64371_bars.parquet"

files = {"Dollar": dv_file, "Timestamp": ts_file, "Volume": vm_file}

def c_weeklycount():
    counts = dict() 
    for n, fln in files.items():
        mask = (pl.scan_parquet(fln)
                .select("Timestamp")
                .collect()
                .with_columns(pl.from_epoch("Timestamp", time_unit = "ms"))["Timestamp"]
                .dt.truncate("1w"))
                #.dt.truncate("w"))

        count  = (pl.scan_parquet(fln)
                  .select("Timestamp")
                  .with_columns(pl.Series("mask", mask))
                  .group_by("mask", maintain_order = True)
                  .agg([pl.col("Timestamp").count().alias("count")])
                  .rename({"mask": "time"})
                  .collect())
        counts[n] = count
    return counts

def c_plotcounts(counts):
    imagedir = Path(__file__).resolve().parent / "images"
    imagedir.mkdir(exist_ok = True)
    plt.switch_backend("Agg")
    for n, df in counts.items():
        df.to_pandas().plot(x = "time", y = "count", title = n)
        plt.savefig(imagedir / (n + ".png"), dpi = 200, bbox_inches = "tight")
        plt.close()






def d_serialcorrel():
    correls = dict() 
    for n, fln in files.items():
        d = (pl.scan_parquet(fln)
             .select("close")
             .collect()["close"]
             .to_numpy())
        r = np.diff(np.log(d))
        correls[n] = np.corrcoef(r[:-1], r[1:])[0][1]
    return(correls)

def e_varvar():
    vars = dict() 
    for n, fln in files.items():
        mask = (pl.scan_parquet(fln)
                .select("Timestamp")
                .collect()
                .with_columns(pl.from_epoch("Timestamp", time_unit = "ms"))["Timestamp"]
                .dt.truncate("1mo"))

        var = (pl.read_parquet(fln)
               .select(["close", "Timestamp"])
               .with_columns(pl.Series("mask", mask))
               .group_by("mask", maintain_order = True)
               .agg(pl.col("close").pct_change().var())
               .select("close").var())
                
        vars[n] = var
    return(vars)

def f_jb():
    jbs = dict() 
    for n, fln in files.items():
        d = (pl.scan_parquet(fln)
             .sort("Timestamp")
             .select("close")
             .collect()["close"]
             .to_numpy())
        r = np.diff(np.log(d))
        jbs[n] = jarque_bera(r)
    return(jbs)

def test_periodicity():
    jbs = dict() 
    for n, fln in files.items():
        d = (pl.scan_parquet(fln)
             .select("close")
             .collect()["close"]
             .to_numpy())
        r = np.diff(np.log(d))
        jbs[n] = jarque_bera(r)
    return(jbs)


if __name__ == "__main__":
    counts = c_weeklycount()
    c_plotcounts(counts)
    print("Question C: counts")
    pprint(counts)
    correls = d_serialcorrel()
    print("Question D: correls")
    pprint(correls)
    varvars = e_varvar()
    print("Question E: var of var")
    pprint(varvars)
    jbs = f_jb()
    print("Question F: Jarque-Bera")
    pprint(jbs)


