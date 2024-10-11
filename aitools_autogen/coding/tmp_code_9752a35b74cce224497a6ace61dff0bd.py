

### Usage

# To use these clients in your application, you would do something like the following:


import asyncio
from api.client import MetadataClient, SearchClient

async def main():
    metadata_client = MetadataClient()
    datasets = await metadata_client.list_datasets()
    print(datasets)

    searchable_fields = await metadata_client.list_searchable_fields("patents", "v1")
    print(searchable_fields)

    search_client = SearchClient()
    search_results = await search_client.perform_search("patents", "v1", criteria="inventor_name:Smith")
    print(search_results)

if __name__ == "__main__":
    asyncio.run(main())