from fastapi import FastAPI
from core.database import MongoDatabase
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from consumers.rabbitmq_consumer import RabbitMQConsumer
from notifications.service import NotificationService

@asynccontextmanager
async def lifespan(app: FastAPI):

    await MongoDatabase.connect()
    print("Successfully connected to MongoDB")

    notification_service = (
        NotificationService()
    )

    consumer = RabbitMQConsumer(
        notification_service=notification_service
    )
    consumer_task = asyncio.create_task(
        consumer.start()
    )

    print("RabbitMQ Consumer Started")

    try:
        yield

    finally:

        consumer_task.cancel()

        await MongoDatabase.close()

        print("Successfully closed MongoDB connection")

app = FastAPI(
    title="Notification Engine API",
    description="API for handling notification events and sending notifications.",
    version="1.0.0",
    lifespan=lifespan
)


# ✅ CORS should be added BEFORE routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   # This enables OPTIONS automatically
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {
        "message": "Notification Engine API is running!",
        "version": "1.0"
    }
