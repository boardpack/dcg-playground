import uvicorn

from dcg_playground.main import create_app


app = create_app(debug=True)

if __name__ == '__main__':
    uvicorn.run(app)
