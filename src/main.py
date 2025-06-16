from fastapi import FastAPI
from mongoengine import connect, disconnect
import scheduler
from settings import Settings
from utils.config import database_name, database_host
from routers import auth, admin, category, product, order, webhook

settings = Settings()
app = FastAPI(root_path=settings.base_path)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(webhook.router)

async def startup_event():
    try:
        connect(db=database_name, host=database_host)
        print('Assoh service connected to DB.')
        scheduler.start_scheduler()
        print('Scheduler started')
    except Exception as e:
        print(f"Failed to start scheduler: {e}")

async def shutdown_event():
    try:
        disconnect()
        print('Assoh service disconnected to DB.')
        scheduler.scheduler.shutdown()
        print('Scheduler stopped')
    except Exception as e:
        print(f"Failed to shutdown scheduler: {e}")

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

@app.get('/health')
def get_health():
    return {'Status':"Running"}

# Modify the create product route to accept a list of images.
# Manage error middleware
# Complete testing course 