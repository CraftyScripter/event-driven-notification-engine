"""
database.py
-------------
MongoDB connection setup using PyMongo async client + Beanie ODM.
"""

from __future__ import annotations
from core import settings
from beanie import init_beanie
from pymongo import AsyncMongoClient



class MongoDatabase:
    """
    MongoDatabase handles MongoDB lifecycle.
    Singleton-like usage recommended.
    """

    # client: Optional[AsyncMongoClient] = None  # Use string literal

    @classmethod
    async def connect(cls):
        """
        Initialize MongoDB connection and Beanie ODM.

        Called ONCE during FastAPI startup.
        """

        if not settings.MONGO_DB_URI or not settings.MONGO_DB_NAME:
            raise ValueError("MongoDB environment variables not set")

        cls.client: AsyncMongoClient = AsyncMongoClient(settings.MONGO_DB_URI)  # type: ignore

        await init_beanie(
            database=cls.client[settings.MONGO_DB_NAME],
            document_models=[

            ],
        )

        print("✅ MongoDB connected successfully")

    @classmethod
    async def close(cls):
        """
        Gracefully close MongoDB connection.

        Called during FastAPI shutdown.
        """
        if cls.client:
            await cls.client.close()
            print("🛑 MongoDB connection closed")
