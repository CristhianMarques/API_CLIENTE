
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aplicacao import views

def start():
    #scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")
    scheduler = BackgroundScheduler(timezone="America/Sao_Paulo")
    scheduler.add_job(views.gera_eventos, 'interval', minutes=1)
    scheduler.start()