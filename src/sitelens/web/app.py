from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sitelens.reporter import run_all_checks
from sitelens.web.database import get_recent_scans, init_db, save_scan


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="SiteLens Dashboard", lifespan=lifespan)

templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@app.get("/", response_class=HTMLResponse)
def home(request: Request, error: str | None = None):
    history = get_recent_scans()

    # Hasil scan terakhir (jika ada) akan jadi item pertama di history
    report = history[0].to_report_dict() if history and not error else None

    return templates.TemplateResponse(
        request,
        "index.html",
        {"report": report, "domain": None, "error": error, "history": history},
    )


@app.post("/scan")
def scan(request: Request, domain: str = Form(...)):
    try:
        report = run_all_checks(domain)
        save_scan(report)
    except Exception as e:
        return RedirectResponse(
            url=f"/?error=Failed to scan {domain}: {e}", status_code=303
        )

    return RedirectResponse(url="/", status_code=303)


def run() -> None:
    import uvicorn
    uvicorn.run("sitelens.web.app:app", host="127.0.0.1", port=8000, reload=True)
