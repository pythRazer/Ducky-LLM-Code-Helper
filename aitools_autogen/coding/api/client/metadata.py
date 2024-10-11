

#### 2. Metadata Client

# This client will handle the requests for listing available data sets and searchable fields.


# filename: api/client/metadata.py
from .base_client import BaseClient

class MetadataClient(BaseClient):
    async def list_datasets(self):
        return await self.get("/")

    async def list_searchable_fields(self, dataset, version):
        return await self.get(f"/{dataset}/{version}/fields")