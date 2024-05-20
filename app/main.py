from fastapi import FastAPI
from app.users.router import router as user_router


app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app_v1 = FastAPI()


app_v1.include_router(user_router)


app.mount("/v1", app_v1)
