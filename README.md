# AI Experts Assignment (Python)

Small Python project with an HTTP client and focused tests.

## Prerequisites

- Python 3.12+
- Docker Desktop (for container runs)

## Run Tests Locally

1. Create a virtual environment:

```powershell
python -m venv .venv
```

2. Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Run tests:

```powershell
python -m pytest -v
```

## Run Tests with Docker

1. Build the image:

```powershell
docker build -t ai-experts-assignment-3 .
```

2. Run the container:

```powershell
docker run --rm ai-experts-assignment-3
```

The image runs tests by default via:

```dockerfile
CMD ["python", "-m", "pytest", "-v"]
```

## Run with Docker Compose

Start tests with build:

```powershell
docker compose up --build --abort-on-container-exit
```

Stop and remove containers/volumes:

```powershell
docker compose down -v
```
