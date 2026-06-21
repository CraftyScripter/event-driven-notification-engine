from fastapi import FastAPI
from core.database import MongoDatabase
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from consumers.rabbitmq_consumer import RabbitMQConsumer
from notifications.provider_manager import ProviderManager
from notifications.service import NotificationService
from core import RedisManager
from notifications.template_engine import TemplateEngine

@asynccontextmanager
async def lifespan(app: FastAPI):

    # await MongoDatabase.connect()
    print("Successfully connected to MongoDB")

    # await RedisManager().connect()
    # print("Successfully connected to Redis")

    # Dependency Injection for NotificationService and RabbitMQConsumer
    notification_service = (
        NotificationService(
            TemplateEngine(),
            ProviderManager(),
        )
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

        # await MongoDatabase.close()

        # await RedisManager().disconnect()
        print("Successfully disconnected from Redis")

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
