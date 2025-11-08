# Fraktal

Small Python library + Dash app scaffold for Fraktal project.

## Setup (Windows / PowerShell)

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run tests:

```powershell
pytest -q
```

4. Run the Dash app:

```powershell
python -m dash_app.app
```

## GitHub sync

Initialize git, create a repo on GitHub and push:

```powershell
git init
git add .
git commit -m "Initial scaffold"
# create a repo on GitHub and then:
git remote add origin https://github.com/<your-username>/fraktal.git
git push -u origin main
```

Alternatively, use GitHub Desktop to create and push the repository.

## What is included

- `fraktal/` : library package with `config` loader and `decorators`.
- `dash_app/` : Dash app skeleton using `dash-mantine-components`.
- `config/default.yaml` : default YAML configuration loaded by `fraktal`.
- `tests/` : pytest tests for the basic components.
- `requirements.txt`, `pyproject.toml`, `.gitignore`, `README.md`.

## Next steps (suggested)

- Implement actual fractal computation modules inside `fraktal/`.
- Improve logging configuration (structured logs, file handlers).
- Add GitHub Actions workflow for CI (run tests and linting).
