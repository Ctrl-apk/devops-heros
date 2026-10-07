# Mini Project: Complete CI Pipeline for a Python App

**Name:** Shifa | **Enrollment:** 24BCS10354 | **Email:** shifa.24bcs10354@sst.scaler.com

---

## Project Structure

```
mini-project/
├── app.py                        ← Flask web application
├── requirements.txt              ← Python dependencies
├── Dockerfile                    ← Container image definition
├── tests/
│   ├── __init__.py
│   └── test_app.py               ← pytest test suite (7 tests)
└── .github/
    └── workflows/
        └── ci.yml                ← GitHub Actions CI pipeline
```

---

## The Application

A simple Flask REST API with 6 endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Hello World message |
| `/health` | GET | Health check — returns `{"status": "healthy"}` |
| `/add/<a>/<b>` | GET | Returns `a + b` |
| `/subtract/<a>/<b>` | GET | Returns `a - b` |
| `/multiply/<a>/<b>` | GET | Returns `a * b` |
| `/divide/<a>/<b>` | GET | Returns `a / b` (400 if b=0) |

### Run locally

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

### Run with Docker

```bash
docker build -t python-ci-app .
docker run -p 5000:5000 python-ci-app
```

---

## The CI Pipeline

The pipeline has **3 jobs** that run in sequence:

```
Push to main/develop
        │
        ▼
  ┌─────────────┐
  │  Job 1      │
  │  lint       │  flake8 checks code style
  └──────┬──────┘
         │ (only if lint passes)
         ▼
  ┌─────────────┐
  │  Job 2      │
  │  test       │  pytest runs 7 tests + coverage report
  └──────┬──────┘
         │ (only if tests pass)
         ▼
  ┌─────────────┐
  │  Job 3      │
  │  docker     │  builds image + verifies /health endpoint
  └─────────────┘
```

### Triggers

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
```

---

## Job Details

### Job 1: Lint (`flake8`)

Checks Python code style and catches syntax errors before tests run.

```bash
flake8 app.py tests/
```

### Job 2: Test (`pytest`)

Runs all 7 tests with coverage reporting. Uploads results as artifacts.

```bash
python -m pytest tests/ --cov=app --cov-report=term-missing -v
```

**Tests:**
- `test_home` — checks `/` returns 200 and correct message
- `test_health` — checks `/health` returns `healthy`
- `test_add` — checks `3 + 5 = 8`
- `test_subtract` — checks `10 - 4 = 6`
- `test_multiply` — checks `4 × 5 = 20`
- `test_divide` — checks `10 / 2 = 5.0`
- `test_divide_by_zero` — checks `/divide/10/0` returns 400

### Job 3: Docker Build

Builds the Docker image and verifies the container starts and responds to `/health`.

```bash
docker build -t python-ci-app .
docker run -d -p 5000:5000 python-ci-app
curl http://localhost:5000/health
```

---

## Artifacts

After every run, GitHub Actions uploads:
- `test-results/results.xml` — JUnit test report
- `coverage.xml` — code coverage report

Both are kept for 7 days and visible in the **Actions** tab on GitHub.

---

## How to Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run lint
flake8 app.py tests/

# Run tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=term-missing
```

---

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [pytest Docs](https://docs.pytest.org/)
- [flake8 Docs](https://flake8.pycqa.org/)
- [Flask Docs](https://flask.palletsprojects.com/)
