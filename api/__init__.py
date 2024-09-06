from fastapi import FastAPI
from api.views import routers
from api.files.views import router_files

app = FastAPI()
app.include_router(routers, prefix='/api')
app.include_router(router_files, prefix='/api/file')
