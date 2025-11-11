<<<<<<< HEAD
# career-compass
Career-compass help to evaluate your skills and suggest the best career path to take.
=======
# CareerCompass AI

CareerCompass AI is a full‑stack resume analysis and job matching application. It provides a web frontend for uploading resumes (PDF/DOCX/TXT) and a Flask backend that parses resumes with spaCy and matches them to sample jobs using simple NLP/ML techniques.

## Features

- Drag & drop resume upload (PDF / DOCX / TXT)
- Resume parsing (skills, education, experience) using spaCy
- Job matching with a simple matching algorithm (scikit-learn utilities)
- Interactive dashboard visualizations with Chart.js
- Modular backend and utilities for parsing and matching
- Mobile-first responsive frontend

## Repository layout

```
careercompass/
├─ backend/
│  ├─ api/
│  │  ├─ resume_parser.py
│  │  └─ job_matcher.py
│  ├─ models/
│  │  └─ resume.py
│  ├─ utils/
# CareerCompass AI

CareerCompass AI is a full‑stack resume analysis and job matching application. It provides a web frontend for uploading resumes (PDF/DOCX/TXT) and a Flask backend that parses resumes with spaCy and matches them to sample jobs using simple NLP/ML techniques.

## Features

- Drag & drop resume upload (PDF / DOCX / TXT)
- Resume parsing (skills, education, experience) using spaCy
- Job matching with a simple matching algorithm (scikit-learn utilities)
- Interactive dashboard visualizations with Chart.js
- Modular backend and utilities for parsing and matching
- Mobile-first responsive frontend

## Repository layout

```
careercompass/
├─ backend/
│  ├─ api/
│  │  ├─ resume_parser.py
│  │  └─ job_matcher.py
│  ├─ models/
│  │  └─ resume.py
│  ├─ utils/
│  │  ├─ text_extractor.py
│  │  └─ file_handler.py
│  ├─ app.py
│  └─ requirements.txt
├─ frontend/
│  ├─ css/styles.css
│  ├─ js/app.js
│  ├─ js/charts.js
│  └─ index.html
└─ README.md
```

## Requirements

- Windows (PowerShell examples shown)
- Python 3.10+ (3.13 works with the current pinned packages; virtualenv recommended)
- NodeJS not required (frontend is static)

## Quick setup (backend)

Open PowerShell and run the following commands from the `backend` directory.

```powershell
# 1. Create and activate a virtual environment
cd "C:\Users\Hp\Desktop\New folder\careercompass\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install Python dependencies
pip install -r requirements.txt
# If you installed newer/changed packages, ensure spaCy model is downloaded:
python -m spacy download en_core_web_sm
```

Notes:
- If you encounter build errors for binary packages, use the prebuilt wheels (pip will normally fetch them for modern Python versions).
- If using Command Prompt instead of PowerShell, activate with `venv\Scripts\activate`.

## Run backend

```powershell
# From backend directory, with venv activated
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
python -m flask run
```

This will start the API at: http://localhost:5000

### Health check

To verify the backend and dependencies are healthy:

```powershell
Invoke-WebRequest -Uri http://localhost:5000/api/health -UseBasicParsing | Select-Object -ExpandProperty Content
```

You should see a JSON payload describing `status` and dependency health (spaCy, scikit-learn, upload folder).

## Run frontend

The frontend is static. From the `frontend` folder run a simple HTTP server and open the page in your browser:

```powershell
cd "C:\Users\Hp\Desktop\New folder\careercompass\frontend"
python -m http.server 8080
```

Open: http://localhost:8080

The web UI will POST resumes to the backend API at `http://localhost:5000/api/upload`.

## Uploading / Testing

Preferred (easy): use the browser frontend at http://localhost:8080 and upload a resume file.

Curl example (Linux/Git Bash or Windows curl):

```bash
curl -v -F "resume=@./path/to/your_resume.pdf" http://localhost:5000/api/upload
```

If PowerShell's `Invoke-WebRequest` does not support `-Form` on your system (older PS versions), use Postman, the browser UI, or Git Bash/curl for multipart uploads.

Simple health test from PowerShell (already shown above):

```powershell
Invoke-WebRequest -Uri http://localhost:5000/api/health -UseBasicParsing | ConvertFrom-Json
```

## Troubleshooting

- 500 errors during upload:
  - Check backend terminal logs. `app.py` now logs progress for saving, parsing, and matching.
  - Ensure uploads directory exists and is writable (backend verifies this in health check).

- spaCy errors during startup
  - Make sure the `en_core_web_sm` model is installed with:
    ```powershell
    python -m spacy download en_core_web_sm
    ```

- Dependency installation failures
  - Ensure you have a recent pip version (upgrade with `python -m pip install --upgrade pip`).
  - On Windows, use prebuilt wheels (pip typically selects them automatically). If you see compilation errors you may need build tools, but for most users the wheels will suffice.

- CORS errors
  - The Flask app allows requests from `http://localhost:8080`. If you serve the frontend from a different origin, update the `CORS(...)` call in `backend/app.py`.

## Development notes & next steps

- Add persistent job data (database) and richer job descriptions.
- Improve the matching algorithm: train a model with job descriptions and labeled matches.
- Add authentication and user accounts to save resumes and history.
- Add unit tests for `api/` modules and tooling for CI (GitHub Actions).

## API Endpoints

- GET /api/health — Returns health status and dependency checks.
- POST /api/upload — Accepts multipart form with `resume` file. Returns parsed `skills`, `industries`, and `recommendations` JSON.

Example successful response shape:

```json
{
  "skills": [{"name":"Python","score":80}, ...],
  "industries": [{"name":"Technology","matchScore":90}, ...],
  "recommendations": [{"title":"Software Engineer","description":"...","matchScore":85}, ...]
}
```

## Contributing

Contributions welcome. Please open issues or PRs. For significant changes, open an issue first to discuss design.

## License

MIT License — include your preferred license text if desired.

---

If you'd like, I can also:
- Add a sample `.env` and start scripts
- Add a simple GitHub Actions workflow to run lint/tests
- Add a sample test that validates the health endpoint

Tell me which of those you'd like next and I'll add it to the todo list and implement it.
