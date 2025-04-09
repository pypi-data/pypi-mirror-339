# RaySpatial

## Installation

```bash
pip install rayspatial
```

## Usage

```python
import rayspatial
```

## Project Structure

```
.
├── example/                 # Example usage
├── rayspatial/                        # Main package directory
│   ├── engine/                 # Engine functionality
│   ├── serve/                 # Serve functionality
├── stac_data/                 # demo stac data 
├── temp_data/                 # caclulate result data 
├── LICENSE                  # License information
├── README.md               # Project documentation
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Project dependencies
```

### Core Modules

- **engine/****: import function
- **serve/****: calculate function

### docs 
- execute generate_routes.py
```
python3 generate_routes.py
```
- run progress.html  
```
 python3 -m http.server 8000 
```

