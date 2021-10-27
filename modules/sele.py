from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
import chromedriver_autoinstaller
from urllib.error import URLError
import getpass
import errno
import os
import platform
import subprocess
from subprocess import PIPE, CREATE_NO_WINDOW
import time
import warnings


class ServiceHideConsole(Service):

    def start(self):
        try:
            cmd = [self.path]
            cmd.extend(self.command_line_args())
            self.process = subprocess.Popen(cmd, env=self.env,
                                            close_fds=platform.system() != 'Windows',
                                            stdout=self.log_file,
                                            stderr=self.log_file,
                                            stdin=PIPE,
                                            creationflags=CREATE_NO_WINDOW)
        except TypeError:
            raise
        except OSError as err:
            if err.errno == errno.ENOENT:
                raise WebDriverException(
                    "'%s' executable needs to be in PATH. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            elif err.errno == errno.EACCES:
                raise WebDriverException(
                    "'%s' executable may have wrong permissions. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            else:
                raise
        except Exception as e:
            raise WebDriverException(
                "The executable %s needs to be available in the path. %s\n%s" %
                (os.path.basename(self.path), self.start_error_message, str(e)))
        count = 0
        while True:
            self.assert_process_still_running()
            if self.is_connectable():
                break
            count += 1
            time.sleep(1)
            if count == 30:
                raise WebDriverException("Can not connect to the Service %s" % self.path)


class ChromeHideConsole(RemoteWebDriver):
    def __init__(self, executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True):
        if chrome_options:
            warnings.warn('use options instead of chrome_options',
                          DeprecationWarning, stacklevel=2)
            options = chrome_options

        if options is None:
            # desired_capabilities stays as passed in
            if desired_capabilities is None:
                desired_capabilities = Options().to_capabilities()
        else:
            if desired_capabilities is None:
                desired_capabilities = options.to_capabilities()
            else:
                desired_capabilities.update(options.to_capabilities())

        self.service = ServiceHideConsole(
            executable_path,
            port=port,
            service_args=service_args,
            log_path=service_log_path)
        self.service.start()

        try:
            RemoteWebDriver.__init__(
                self,
                command_executor=ChromeRemoteConnection(
                    remote_server_addr=self.service.service_url,
                    keep_alive=keep_alive),
                desired_capabilities=desired_capabilities)
        except Exception:
            self.quit()
            raise
        self._is_remote = False


class Driver:
    def __init__(self) -> None:
        self.driver = None

    def start(self) -> None:
        try:
            chromedriver_autoinstaller.install(cwd=True)
        except URLError:
            pass
        path = os.path.join(
            "C:", os.sep, "Users", getpass.getuser(), "AppData", "Local", "Google", "Chrome", "User Data")
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--user-data-dir=" + path)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = ChromeHideConsole(options=options)
        self.driver.get("https://www.facebook.com")

    def end(self) -> None:
        if self.is_open():
            self.driver.quit()
        else:
            kill_driver()
        self.driver = None

    def logged(self) -> bool:
        locator = (By.CSS_SELECTOR, 'svg[class="a8c37x1j ms05siws hwsy1cff b7h9ocf4"]')
        try:
            WebDriverWait(self.driver, 1).until(ec.presence_of_element_located(locator))
        except (TimeoutException, AttributeError):
            return False
        return True

    def create_cookies(self) -> str:
        cookies = self.driver.get_cookies()[::-1]
        str_cookie = ""
        for cookie in cookies[:-1]:
            str_cookie += cookie["name"] + "=" + cookie["value"] + "; "
        str_cookie += cookies[-1]["name"] + "=" + cookies[-1]["value"]
        return str_cookie

    def is_open(self) -> bool:
        if self.driver:
            if "disconnected" not in self.driver.get_log("driver")[-1]["message"]:
                return True
        return False


def kill_chrome() -> None:
    os.system("taskkill /f /im chrome.exe 2> nul")


def kill_driver() -> None:
    os.system("taskkill /f /im chromedriver.exe 2> nul")
