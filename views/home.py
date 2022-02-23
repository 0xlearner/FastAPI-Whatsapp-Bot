import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates


templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home/index.html", {"request": request})
