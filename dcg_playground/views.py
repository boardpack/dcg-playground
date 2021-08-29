import os
import traceback
from pathlib import Path
from tempfile import TemporaryDirectory

from starlette.routing import Route, Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from datamodel_code_generator import InputFileType, generate as generate_models


templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))


async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})


async def generate(request: Request) -> JSONResponse:
    data: dict = await request.json()
    openapi_schema: str = data['source']

    with TemporaryDirectory() as temporary_directory_name:
        temporary_directory = Path(temporary_directory_name)
        output = Path(temporary_directory / 'model.py')
        try:
            generate_models(
                openapi_schema,
                input_file_type=InputFileType.OpenAPI,
                output=output,
            )
        except Exception:
            tb = traceback.format_exc()
            return JSONResponse({"output": tb}, status_code=400)

        models: str = output.read_text()

    return JSONResponse({"output": models})


routes = [
    Route('/', endpoint=homepage),
    Route('/generate', endpoint=generate, methods=['POST']),
]
