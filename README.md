## Adia tick processing

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
* `hdf5_convert.py`
    * Converts HDF5 dataset to a parquet dataset. This is necessary to use full power of `polars` [larger-than-memory](https://docs.pola.rs/api/python/dev/reference/api/polars.scan_parquet.html) capabilities. 
* `main.py`
    * `trs_dv`
        * Ensures that there are no time overlaps between contract names
        * Merges by taking returns and concatenating, and taking (x + 1) cumprod, with special treatment for instrument jumps (return set to 0). Multiplies by first price in dataset to get to a total single series. 
        * In the same pass as trs creation, dollar volume ("dolvlm") series (volume x price) was added. 

### Notes
* Non prod, exploratory, so no type hints in interest of time. 
* Dataset and intermediate allocations is much bigger than my Macbook Air can handle hence the memory-maped disk scan usage. Expect circa 2 orders of magnitude more speed for in-memory workflow. 
* Documentation was googled. Grok was constulted but found to be counterproductive. No IDE-based AI was used.



