from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sitelens.reporter import run_all_checks

app = FastAPI(title="SiteLens Dashboard")

templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"report": None, "domain": None, "error": None},
    )


@app.post("/scan", response_class=HTMLResponse)
def scan(request: Request, domain: str = Form(...)):
    try:
        report = run_all_checks(domain)
        return templates.TemplateResponse(
            request,
            "index.html",
            {"report": report, "domain": domain, "error": None},
        )
    except Exception as e:
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "report": None,
                "domain": domain,
                "error": f"Failed to scan {domain}: {e}",
            },
        )


def run() -> None:
    import uvicorn
    uvicorn.run("sitelens.web.app:app", host="127.0.0.1", port=8000, reload=True)
