

#### 3. Search Client

# This client will handle the search requests.


# filename: api/client/search.py
from .base_client import BaseClient

class SearchClient(BaseClient):
    async def perform_search(self, dataset, version, criteria="*:*", start=0, rows=100):
        data = {
            "criteria": criteria,
            "start": start,
            "rows": rows
        }
        return await self.post(f"/{dataset}/{version}/records", data)