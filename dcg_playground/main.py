from starlette.applications import Starlette

from dcg_playground import views


def create_app(debug: bool = False):
    application = Starlette(debug=debug, routes=views.routes)
    return application
