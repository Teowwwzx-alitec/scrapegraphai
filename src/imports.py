import sys
import os
import json
import asyncio
import aiofiles
import logging
import requests
import datetime

from dotenv import load_dotenv
from typing import List
from lxml import html
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from playwright.async_api import async_playwright
from urllib.parse import urlparse
from datetime import datetime

from src.config import Config
from src.utils import *
from src.auth.csrf import *
from src.core.navigator import *
from src.core.analyzer import *
from src.scrapers.base_scraper import *