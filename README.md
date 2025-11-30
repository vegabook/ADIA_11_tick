## Adia tick processing

### *MEMORY USAGE*
This project uses memory mapped arrays for larger than memory data.  


### Usage
Clone repo or unzip   
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
* `main.py`
    * `trs_dv`
        * Ensures that there are no time overlaps between contract names
        * Merges by taking returns and concatenating, and taking (x + 1) cumprod, with special treatment for instrument jumps (return set to 0). Multiplies by first price in dataset to get to a total single series. 
        * In the same pass as trs creation, dollar volume ("dolvlm") series (volume x price) was added. 

### Notes
* used trades_filter0vol dataset
* Code would probably be faster in imperative style, but opportunity was used to test polars lib speed on disk scan workflows.
* Non prod, exploratory, so no type hints. 
* No in-IDE ai assistant.  
* No thresholds were provided for volume and dollar traded. Used 1h and corresponding averages over 1h for volume, dollars. 



