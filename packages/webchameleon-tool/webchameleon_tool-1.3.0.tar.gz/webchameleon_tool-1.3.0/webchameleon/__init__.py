from .core import WebChameleon
from .utils.logger import configure_logging

__version__ = "1.3.0"
__all__ = ["WebChameleon"]

# Konfigurasi logging secara global saat modul diimpor
configure_logging()
