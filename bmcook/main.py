from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from bmcook.api.rest import recipe

app = FastAPI()

app.include_router(recipe.router, prefix="/recipes")


@app.get("/")
def root():
    return RedirectResponse(url="/recipes", status_code=301)


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()