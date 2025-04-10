from .data import flatten_list  # Экспорт функций
from .download import download_file
from .gui import EasyWindow
from .telegram import EasyBot
from .web import scrape_links, fetch_url
from .files import read_lines, write_json

__version__ = "0.1.0"
__all__ = ["download_file", "flatten_list", "EasyWindow", "EasyBot", "scrape_links", "fetch_url", "read_lines", "write_json"]    # Что импортировать при `from my_library import *`