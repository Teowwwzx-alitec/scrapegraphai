import sys
import os
import json
import asyncio
import aiofiles
from datetime import datetime
from src.config import Config
from src.utils import create_menu_selectors_dir
from src.auth.csrf import OdooSession
from src.core.navigator import run_authenticated_navigator
from src.core.analyzer import analyzer
from src.scrapers.base_scraper import xpath_scraper