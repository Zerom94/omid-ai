# Artist Data Fetcher

A small Python utility that queries a PHP endpoint (`php?artist=ID`) to retrieve
information about a musical artist.

## Features

- Command‑line interface with simple arguments.
- Supports plain‑text or JSON output.
- Clean separation between CLI (`main.py`) and HTTP client (`client.py`).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py 1          # fetch artist with ID 1, pretty‑print
python main.py 5 --output json   # fetch artist 5 and print raw JSON
```

## Configuration

Edit `config.py` to point `BASE_URL` at the actual server providing the PHP
endpoint.

## License

MIT
