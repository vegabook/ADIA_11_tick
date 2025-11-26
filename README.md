## Adia sentiment

### Usage or Nix/NixOS
Clone repo  
`cd adia`  
`nix develop`  
`uv run main.py`

### Usage Linux/Mac
Clone repo  
`cd adia` 
install [uv](https://docs.astral.sh/uv/getting-started/installation/)
install [ollama](https://ollama.com/download/linux)
`uv run main.py`

### Data prep
Project expects to fine exercise data file as `./data/hdf5/ES.h5`

### Explanation
* Converts HDF5 dataset to a parquet dataset. This is necessary to use full power of `polars` [larger-than-memory](https://docs.pola.rs/api/python/dev/reference/api/polars.scan_parquet.html) capabilities. 
* Ensures that there are no time overlaps between contract names
* Merges by taking returns and concatenating, and taking (x + 1) cumprod, with special treatment for instrument jumps (return set to 0). Multiplies by first price in dataset to get to a total single series. 


