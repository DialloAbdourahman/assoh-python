from fastapi import FastAPI
from mongoengine import connect, disconnect
from settings import Settings
from utils.config import database_name, database_host
from routers import auth, admin, category

settings = Settings()
app = FastAPI(root_path=settings.base_path)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(category.router)


async def startup_event():
    connect(db=database_name, host=database_host)
    print('Assoh service connected to DB.')

async def shutdown_event():
    disconnect()
    print('Assoh service disconnected to DB.')

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

@app.get('/health')
def get_health():
    return {'Status':"Running"}