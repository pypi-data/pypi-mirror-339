# Fastapi Vite
from fastapi_vite_dara.config import settings
from fastapi_vite_dara.loader import vite_asset, vite_asset_url, vite_hmr_client

__version__ = "0.4.0"

__all__ = ["vite_asset_url", "vite_hmr_client", "vite_asset", "settings"]
