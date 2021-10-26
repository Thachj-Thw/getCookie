from selenium import webdriver
import chromedriver_autoinstaller
from urllib.error import URLError
import os
import getpass


def init_driver() -> webdriver.Chrome:
    try:
        chromedriver_autoinstaller.install(cwd=True)
    except URLError:
        pass
    path = os.path.join("C:", os.sep, "Users", getpass.getuser(), "AppData", "Local", "Google", "Chrome", "User Data")
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--user-data-dir=" + path)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(options=options)


def kill_chrome() -> None:
    os.system("taskkill /f /im chrome.exe 2> nul")


def kill_driver() -> None:
    os.system("taskkill /f /im chromedriver.exe 2> nul")


def create_cookies(driver) -> str:
    cookies = driver.get_cookies()[::-1]
    str_cookie = ""
    for cookie in cookies[:-1]:
        str_cookie += cookie["name"] + "=" + cookie["value"] + "; "
    str_cookie += cookies[-1]["name"] + "=" + cookies[-1]["value"]
    return str_cookie
