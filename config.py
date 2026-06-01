# config.py
import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")

    BROWSER = "chrome"
    EXPLICIT_WAIT = 15       # max seconds for specific wait conditions (used in BasePage)
    PAGE_LOAD_TIMEOUT = 30   # max seconds for a page to fully load

    STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER   = os.getenv("LOCKED_USER", "locked_out_user")
    PASSWORD      = os.getenv("PASSWORD", "secret_sauce")