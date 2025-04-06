# ensure-shebang-runtime

A lightweight helper to re-execute a Python script using the interpreter defined in its shebang (`#!`) line — even if it was run via `python script.py`.

## Usage

```python
import ensure_shebang_runtime
ensure_shebang_runtime.reexec_with_shebang(__file__)

