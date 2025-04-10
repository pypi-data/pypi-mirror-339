# -*- coding: utf-8 -*-

import configparser
import glob
import http.cookiejar
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import platform
import lz4.block
from pathlib import Path
from typing import Dict, List, Union


is_wsl: bool = False
DEBUG_PORT = 9222
DEBUG_URL = f'http://localhost:{DEBUG_PORT}/json'

if (platform.uname().release.find("microsoft") >= 0 and platform.uname().system.lower() != "windows"):
    is_wsl = True

shadowcopy = None
if sys.platform == 'win32' and not is_wsl:
    try:
        import shadowcopy
    except ImportError:
        pass

ignore_wsl = os.environ.get('IGNORE_WSL', 'false')

if ignore_wsl.lower() == 'true' and is_wsl:
    is_wsl = False

wsl_path_dict: dict = {}
if is_wsl:
    cmd = "cat /proc/mounts|grep drvfs"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    win_drives_list = ps.communicate()[0].decode("utf-8").strip()
    for drive in win_drives_list.splitlines()[:2]:
        drive_details = drive.split(';')
        drive_letter = drive_details[0].replace("path=", "").split(':', 1)[0]
        linux_path = drive_details[4].replace("symlinkroot=", "").split(',', 1)[0]
        wsl_path_dict[drive_letter] = { "windows_path": f"{drive_letter}:\\", "linux_path": f"{linux_path}{drive_letter.lower()}" }
        
    env_vars = ["UserProfile", "LOCALAPPDATA", "APPDATA"]
    for var in env_vars:
        cmd = f"cmd.exe /c 'echo %{var}%'"
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=wsl_path_dict["C"]["linux_path"])
        env_path = ps.communicate()[0].decode("utf-8").strip()
        wsl_path_dict[var] = env_path
        

def _wsl_path_from_windows(path_name: str):
    if path_name[0] in ("~", "/"):
        return path_name
        
    args = ("wslpath", "-a", "-u", path_name)
    
    tempfp = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=None, universal_newlines=True)
    return tempfp.communicate()[0].strip()

def _wsl_path_from_wsl(path_name: str):
    args = ("wslpath", "-a", "-m", path_name)

    tempfp = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=None, universal_newlines=True)
    return tempfp.communicate()[0].strip()

def _wsl_get_windows_env(env_var: str, wsl_path: bool = True):
    cmd = f"cmd.exe /c 'echo %{env_var}%'"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=wsl_path_dict["C"]["linux_path"])
    win_path = ps.communicate()[0].decode("utf-8").strip()
    if not wsl_path:
        return win_path
    return _wsl_path_from_windows(win_path)
        

__doc__ = 'Load browser cookies into a cookiejar'

class BrowserCookieError(Exception):
    pass

def _expand_win_path(path: Union[dict, str]):
    if not isinstance(path, dict):
        path = {'path': path, 'env': 'APPDATA'}
    return os.path.join(os.getenv(path['env'], ''), path['path'])

def _expand_wsl_path(path: Union[dict, str]):
    if not isinstance(path, dict):
        path = {'path': path, 'env': 'APPDATA'}
    wsl_env_path = _wsl_get_windows_env(path['env'])
    sanitized_path = path['path'].replace("\\", "/")
    
    return os.path.join(wsl_env_path, sanitized_path)

class _DatabaseConnetion():
    def __init__(self, database_file: os.PathLike, try_legacy_first: bool = False):
        self.__database_file = database_file
        self.__temp_cookie_file = None
        self.__connection = None
        self.__methods = [
            self.__sqlite3_connect_readonly,
        ]

        if try_legacy_first:
            self.__methods.insert(0, self.__get_connection_legacy)
        else:
            self.__methods.append(self.__get_connection_legacy)

        if shadowcopy:
            self.__methods.append(self.__get_connection_shadowcopy)

    def __enter__(self):
        return self.get_connection()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __check_connection_ok(self, connection):
        try:
            connection.cursor().execute('select 1 from sqlite_master')
            return True
        except sqlite3.OperationalError:
            return False

    def __sqlite3_connect_readonly(self):
        uri = Path(self.__database_file).absolute().as_uri()
        for options in ('?mode=ro', '?mode=ro&nolock=1', '?mode=ro&immutable=1'):
            try:
                con = sqlite3.connect(uri + options, uri=True)
            except sqlite3.OperationalError:
                continue
            if self.__check_connection_ok(con):
                return con

    def __get_connection_legacy(self):
        with tempfile.NamedTemporaryFile(suffix='.sqlite') as tf:
            self.__temp_cookie_file = tf.name
        try:
            shutil.copyfile(self.__database_file, self.__temp_cookie_file)
        except PermissionError:
            return
        con = sqlite3.connect(self.__temp_cookie_file)
        if self.__check_connection_ok(con):
            return con

    def __get_connection_shadowcopy(self):
        if not shadowcopy:
            raise RuntimeError("shadowcopy is not available")

        self.__temp_cookie_file = tempfile.NamedTemporaryFile(
            suffix='.sqlite').name
        shadowcopy.shadow_copy(self.__database_file, self.__temp_cookie_file)
        con = sqlite3.connect(self.__temp_cookie_file)
        if self.__check_connection_ok(con):
            return con

    def get_connection(self):
        if self.__connection:
            return self.__connection
        for method in self.__methods:
            con = method()
            if con is not None:
                self.__connection = con
                return con
        raise BrowserCookieError('Unable to read database file')

    def cursor(self):
        return self.connection().cursor()

    def close(self):
        if self.__connection:
            self.__connection.close()
        if self.__temp_cookie_file:
            try:
                os.remove(self.__temp_cookie_file)
            except Exception:
                pass

class FirefoxBased:
    """Superclass for Firefox based browsers"""

    def __init__(self, browser_name, cookie_file=None, domain_name="", key_file=None, **kwargs):
        self.browser_name = browser_name
        self.cookie_file = cookie_file or self.__find_cookie_file(**kwargs)
        # current sessions are saved in sessionstore.js
        self.session_file = os.path.join(
            os.path.dirname(self.cookie_file), 'sessionstore.js')
        self.session_file_lz4 = os.path.join(os.path.dirname(
            self.cookie_file), 'sessionstore-backups', 'recovery.jsonlz4')
        # domain name to filter cookies by
        self.domain_name = domain_name

    def __str__(self):
        return self.browser_name

    @staticmethod
    def get_default_profile(user_data_path):
        config = configparser.ConfigParser()
        profiles_ini_path = glob.glob(os.path.join(
            user_data_path + '**', 'profiles.ini'))
        fallback_path = user_data_path + '**'

        if not profiles_ini_path:
            return fallback_path

        profiles_ini_path = profiles_ini_path[0]
        config.read(profiles_ini_path, encoding="utf8")

        profile_path = None
        for section in config.sections():
            if section.startswith('Install'):
                profile_path = config[section].get('Default')
                break
            # in ff 72.0.1, if both an Install section and one with Default=1 are present, the former takes precedence
            elif config[section].get('Default') == '1' and not profile_path:
                profile_path = config[section].get('Path')

        for section in config.sections():
            # the Install section has no relative/absolute info, so check the profiles
            if config[section].get('Path') == profile_path:
                absolute = config[section].get('IsRelative') == '0'
                return profile_path if absolute else os.path.join(os.path.dirname(profiles_ini_path), profile_path)

        return fallback_path

    def __expand_and_check_path(self, paths: Union[str, List[str], Dict[str, str], List[Dict[str, str]]]) -> str:
        """Expands a path to a list of paths and returns the first one that exists"""
        if not isinstance(paths, list):
            paths = [paths]
        for path in paths:
            if isinstance(path, dict):
                if not is_wsl:
                    expanded = _expand_win_path(path)
                else:
                    expanded = _expand_wsl_path(path)
            else:
                expanded = os.path.expanduser(path)
            if os.path.isdir(expanded):
                return expanded
        raise BrowserCookieError(
            f'Could not find {self.browser_name} profile directory')

    def __find_cookie_file(self, linux_data_dirs=None, windows_data_dirs=None, osx_data_dirs=None):
        cookie_files = []

        if sys.platform == 'darwin':
            user_data_path = self.__expand_and_check_path(osx_data_dirs)
        elif not is_wsl and (sys.platform.startswith('linux') or 'bsd' in sys.platform.lower()):
            user_data_path = self.__expand_and_check_path(linux_data_dirs)
        elif sys.platform == 'win32' or is_wsl:
            user_data_path = self.__expand_and_check_path(windows_data_dirs)
        else:
            raise BrowserCookieError(
                'Unsupported operating system: ' + sys.platform)

        cookie_files = glob.glob(os.path.join(FirefoxBased.get_default_profile(user_data_path), 'cookies.sqlite')) \
            or cookie_files

        if cookie_files:
            return cookie_files[0]
        else:
            raise BrowserCookieError(
                f'Failed to find {self.browser_name} cookie file')

    @staticmethod
    def __create_session_cookie(cookie_json):
        return create_cookie(cookie_json.get('host', ''), cookie_json.get('path', ''),
                             cookie_json.get('secure', False), None,
                             cookie_json.get('name', ''), cookie_json.get(
                                 'value', ''),
                             cookie_json.get('httponly', False))

    def __add_session_cookies(self, cj):
        if not os.path.exists(self.session_file):
            return
        try:
            with open(self.session_file, 'rb') as file_obj:
                json_data = json.load(file_obj)
        except ValueError as e:
            print(f'Error parsing {self.browser_name} session JSON:', str(e))
        else:
            for window in json_data.get('windows', []):
                for cookie in window.get('cookies', []):
                    if self.domain_name == '' or self.domain_name in cookie.get('host', ''):
                        cj.set_cookie(
                            FirefoxBased.__create_session_cookie(cookie))

    def __add_session_cookies_lz4(self, cj):
        if not os.path.exists(self.session_file_lz4):
            return
        try:
            with open(self.session_file_lz4, 'rb') as file_obj:
                file_obj.read(8)
                json_data = json.loads(lz4.block.decompress(file_obj.read()))
        except ValueError as e:
            print(
                f'Error parsing {self.browser_name} session JSON LZ4:', str(e))
        else:
            for cookie in json_data.get('cookies', []):
                if self.domain_name == '' or self.domain_name in cookie.get('host', ''):
                    cj.set_cookie(FirefoxBased.__create_session_cookie(cookie))

    def load(self):
        cj = http.cookiejar.MozillaCookieJar()
        # firefoxbased seems faster with legacy mode
        with _DatabaseConnetion(self.cookie_file, True) as con:
            cur = con.cursor()
            try:
                cur.execute('select host, path, isSecure, expiry, name, value, isHttpOnly from moz_cookies '
                            'where host like ?', ('%{}%'.format(self.domain_name),))
            except sqlite3.DatabaseError as e:
                if e.args[0].startswith(('no such table: ', 'file is not a database')):
                    raise BrowserCookieError('File {} is not a Firefox cookie file'.format(self.tmp_cookie_file))
                raise

            for item in cur.fetchall():
                host, path, secure, expires, name, value, http_only = item
                c = create_cookie(host, path, secure, expires ,
                                  name, value, http_only)
                cj.set_cookie(c)

        self.__add_session_cookies(cj)
        self.__add_session_cookies_lz4(cj)

        return cj


class Firefox(FirefoxBased):
    """Class for Firefox"""

    def __init__(self, cookie_file=None, domain_name="", key_file=None):
        args = {
            'linux_data_dirs': [
                '~/snap/firefox/common/.mozilla/firefox',
                '~/.mozilla/firefox'
            ],
            'windows_data_dirs': [
                {'env': 'APPDATA', 'path': r'Mozilla\Firefox'},
                {'env': 'LOCALAPPDATA', 'path': r'Mozilla\Firefox'}
            ],
            'osx_data_dirs': [
                '~/Library/Application Support/Firefox'
            ]
        }
        super().__init__('Firefox', cookie_file, domain_name, key_file, **args)


class LibreWolf(FirefoxBased):
    """Class for LibreWolf"""

    def __init__(self, cookie_file=None, domain_name="", key_file=None):
        args = {
            'linux_data_dirs': [
                '~/snap/librewolf/common/.librewolf',
                '~/.librewolf'
            ],
            'windows_data_dirs': [
                {'env': 'APPDATA', 'path': 'librewolf'},
                {'env': 'LOCALAPPDATA', 'path': 'librewolf'}
            ],
            'osx_data_dirs': [
                '~/Library/Application Support/librewolf'
            ]
        }
        super().__init__('LibreWolf', cookie_file, domain_name, key_file, **args)


def create_cookie(host, path, secure, expires, name, value, http_only):
    """Shortcut function to create a cookie"""
    # HTTPOnly flag goes in _rest, if present (see https://github.com/python/cpython/pull/17471/files#r511187060)
    return http.cookiejar.Cookie(0, name, value, None, False, host, host.startswith('.'), host.startswith('.'), path,
                                 True, secure, expires if expires != None else 0, False, None, None, {})

def firefox(cookie_file=None, domain_name="", key_file=None):
    """Returns a cookiejar of the cookies and sessions used by Firefox. Optionally
    pass in a domain name to only load cookies from the specified domain
    """
    return Firefox(cookie_file, domain_name, key_file).load()


def librewolf(cookie_file=None, domain_name="", key_file=None):
    """Returns a cookiejar of the cookies and sessions used by LibreWolf. Optionally
    pass in a domain name to only load cookies from the specified domain
    """
    return LibreWolf(cookie_file, domain_name, key_file).load()

all_browsers = [firefox, librewolf]

def load(domain_name=""):
    """Try to load cookies from all supported browsers and return combined cookiejar
    Optionally pass in a domain name to only load cookies from the specified domain
    """
    cj = http.cookiejar.CookieJar()
    for cookie_fn in all_browsers:
        try:
            for cookie in cookie_fn(domain_name=domain_name):
                cj.set_cookie(cookie)
        except BrowserCookieError:
            pass
    return cj


__all__ = ['BrowserCookieError', 'load', 'all_browsers'] + all_browsers


if __name__ == '__main__':
    print(load())
