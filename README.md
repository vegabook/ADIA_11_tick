## Adia tick processing

### *MEMORY USAGE*
This project uses memory mapped arrays for larger than memory data.  
Tested on Linux and MacOS with 16GB of Ram (Linux: 80GB swap file required). 


### Usage
Clone repo or unzip (https://github.com/vegabook/ADIA_11_tick)   
`cd ADIA_11_tick`  
either: install [uv](https://docs.astral.sh/uv/getting-started/installation/) or on nix[os], `nix develop`
ensure ES.h5 is in the `<project_root>/data/hdf5` directory  
either:  
* convert to parquet: `uv run hdf5_convert.py`  
* make bars: `uv run barmake.py`  
* answer questions: `uv run qa.py`  
or:   
`./runall.sh` (might need to `chmod +x runall.sh` first)

### Data prep
Project expects to find exercise data file as `./data/ES.h5`

### Explanation
* `hdf5_convert.py`
    * `convert()`
        * Converts HDF5 dataset to a parquet dataset. This is necessary to use full power of `polars` [larger-than-memory](https://docs.pola.rs/api/python/dev/reference/api/polars.scan_parquet.html) capabilities. 
* `barmake.py`
    * `trs_dv`
        * Ensures that there are no time overlaps between contract names.
        * Merges by taking returns and concatenating, and taking (x + 1) cumprod, with special treatment for instrument jumps (return set to 0). Multiplies by first price in dataset to get to a total single series.
        * In the same pass as trs creation, dollar volume ("dolvlm") series (volume x price) was added.
* `qa.py`
    * Runs all the questions, and writes plots to disk. 

### Answers
* Question c: the hourly bars have the most stable count because they're pre-selected as a fixed time period, whereas the frequency of the others depends on volume of trades (and price).  
* Question d:
```
Question D: correls
{'Dollar': np.float64(-0.015800925371829838),
 'Timestamp': np.float64(-0.030008005932149917),
 'Volume': np.float64(-0.0063460528150651434)}
```
* Question e:
```
Question E: var of var
{'Dollar': shape: (1, 1)
┌────────────┐
│ close      │
│ ---        │
│ f32        │
╞════════════╡
│ 7.3787e-11 │
└────────────┘,
 'Timestamp': shape: (1, 1)
┌────────────┐
│ close      │
│ ---        │
│ f32        │
╞════════════╡
│ 1.8788e-10 │
└────────────┘,
 'Volume': shape: (1, 1)
┌────────────┐
│ close      │
│ ---        │
│ f32        │
╞════════════╡
│ 3.0094e-11 │
└────────────┘}
```
* Question f:
```
Question F: Jarque-Bera
{'Dollar': SignificanceResult(statistic=np.float32(1.5158135e+06), pvalue=np.float32(0.0)),
 'Timestamp': SignificanceResult(statistic=np.float32(9.573886e+06), pvalue=np.float32(0.0)),
 'Volume': SignificanceResult(statistic=np.float32(408052.44), pvalue=np.float32(0.0))}
```

* Chart outputs in .png form in ./images directory. 

### Notes
* Used trades_filter0vol dataset
* Code would probably be faster in imperative style, but opportunity was used to test polars lib speed on disk scan workflows.
* Non prod, exploratory, so no type hints. 
* No in-IDE ai assistant.  Extensive docs consulted for parameters and functions. 
* No thresholds were provided for volume and dollar traded. Used 1h and corresponding averages over 1h for volume, dollars. 



