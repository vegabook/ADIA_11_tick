## Adia tick processing

### *MEMORY USAGE*
This project uses memory mapped arrays for larger than memory data.  
Tested on Macbook Air 16GB RAM and NixOS 16GB RAM. On Linux requires swapfile of 96GB.  

### Usage or Nix/NixOS
Clone repo  
`cd adia`  
`nix develop`  
`uv run main.py`

### Usage Linux/Mac
Clone repo  
`cd adia`  
install [uv](https://docs.astral.sh/uv/getting-started/installation/)  
install [ollama](https://ollama.com/download/linux)  :w
`uv run main.py`  

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
* Non prod, exploratory, so no type hints in interest of time. 
* Documentation was googled. Grok was for syntax and data types and polars functions.
* No in-IDE ai assistant. 



