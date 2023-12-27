from abc import ABC, abstractmethod

from core.database import get_connection_sync
from config import settings as global_settings

collection = global_settings.mongo_collection


class Repository(ABC):
    @abstractmethod
    async def create(self, insert_data: dict):
        raise NotImplemented

    @abstractmethod
    async def get(self, filter_data: dict):
        raise NotImplemented

    @abstractmethod
    async def get_list(self, filter_data: dict):
        raise NotImplemented

    @abstractmethod
    async def update(self, doc_filter: dict, doc_setter: dict):
        raise NotImplemented

    @abstractmethod
    async def delete(self, doc_filter: dict):
        raise NotImplemented


class MongoRepository(Repository):
    def __init__(self):
        connection_dict = get_connection_sync()
        self.mongo_client = connection_dict[collection]

    async def create(self, insert_data: dict):
        await self.mongo_client.insert_one(insert_data)
        return await self.get(insert_data)

    async def get(self, filter_data: dict):
        return await self.mongo_client.find_one(filter_data, {"_id": 0})

    async def update(self, doc_filter: dict, doc_setter: dict):
        await self.mongo_client.update_one(doc_filter, {"$set": doc_setter})
        return await self.get(doc_filter)

    async def delete(self, doc_filter: dict):
        await self.mongo_client.delete_one(doc_filter)

    async def get_list(self, filter_data: dict):
        return self.mongo_client.find(filter_data, {"_id": 0})
