

#### 4. __init__.py

# Finally, let's make sure that the clients are accessible from the `api.client` package.


# filename: api/client/__init__.py
from .metadata import MetadataClient
from .search import SearchClient

__all__ = ["MetadataClient", "SearchClient"]