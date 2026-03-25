# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**farialimer** is a Python library for converting between structured data (Python dicts) and Brazilian financial file formats (CNAB and IMBARQ). It works in both directions: parsing CNAB/IMBARQ fixed-width text files into Python dicts, and converting input data into CNAB-formatted output. Layout definitions are driven by YAML specs for each bank (Itau, Santander) and B3 (Brazilian stock exchange).

## Commands

### Install dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run all tests
```bash
pytest tests/
```

### Run a single test file
```bash
pytest tests/parser/b3/test_b3_parser.py
```

### Run tests with coverage
```bash
pytest tests/ --cov=./ --cov-report=xml
```

### Linting
```bash
ruff check .
ruff format --check .
```

### Format code
```bash
ruff format .
```

## Architecture

### Spec-driven parsing

The core design is **spec-driven**: YAML files in `farialimer/specs/{provider}/` define the layout of each document type (field names, positions, data types, converters). Parsers read these specs at init time and use them to extract fields from fixed-width text lines.

### Parser hierarchy

- `BasicParser` (ABC in `farialimer/parser/basic_parser.py`) — base class that handles reading files, loading YAML specs, and parsing lines into `OrderedDict` results. Each subclass must implement `get_line_register(line)` to determine which register/record type a line belongs to.
- Provider-specific base classes: `ItauParser`, `SantanderParser` — intermediate classes under `farialimer/parser/{provider}/`.
- Concrete parsers: `B3Parser`, `ItauCobranca`, `PagamentoFornecedoresParser` — implement register-type detection logic specific to each document format.

### Key concepts

- **Register type**: Each line in a file has a register type (e.g., header, detail, trailer) determined by character positions. The `get_line_register()` method maps lines to their register type key, which is used to look up the correct field layout from the YAML spec.
- **Field model** (`farialimer/parser/models.py`): `Field` namedtuple with `(name, description, datatype, convert, start, end)`. `ParseObject` namedtuple wraps the raw value with its converter.
- **Data types**: `X` = string, `9` = integer, `9V` = Febraban numeric (decimal), `N` = B3 integer, `NV` = B3 numeric. Converters in `farialimer/utils/converters.py`.

### YAML spec format

Each spec YAML has metadata (`provider`, `service`, `version`, `layout`) and a `register` block mapping register type keys to field definitions with `description`, `type`, `pos` (start/end positions, 1-indexed), and optional `convert`.

## Language

The project uses Portuguese for variable names, comments, YAML field names, and documentation. Maintain this convention.
