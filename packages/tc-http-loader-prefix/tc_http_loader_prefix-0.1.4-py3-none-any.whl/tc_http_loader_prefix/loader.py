import asyncio
from thumbor.loaders.http_loader import load as http_loader
from urllib.parse import urljoin
from .config import register_config

register_config()

def load(context, url):
    """
    Extended HTTP loader that prefixes the URL with a fixed base URL.
    """
    prefix = context.config.TC_HTTP_LOADER_PREFIX
    if not prefix:
        raise RuntimeError("TC_HTTP_LOADER_PREFIX is not set in the config")

    # Ensure the URL is properly joined with the fixed base
    full_url = urljoin(prefix, url)

    # Call the default HTTP loader with the modified URL
    return http_loader(context, full_url)
