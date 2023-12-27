from motor.motor_asyncio import AsyncIOMotorClient

from config import settings


async def get_connection() -> dict[str, AsyncIOMotorClient]:
    mongo_client = AsyncIOMotorClient(settings.mongo_url)
    mongo_database = mongo_client[settings.mongo_db]
    mongo_collections = {
        settings.mongo_collection: mongo_database.get_collection(
            settings.mongo_collection
        ),
    }
    return mongo_collections


def get_connection_sync() -> dict[str, AsyncIOMotorClient]:
    mongo_client = AsyncIOMotorClient(settings.mongo_url)
    mongo_database = mongo_client[settings.mongo_db]
    mongo_collections = {
        settings.mongo_collection: mongo_database.get_collection(
            settings.mongo_collection
        ),
    }
    return mongo_collections
