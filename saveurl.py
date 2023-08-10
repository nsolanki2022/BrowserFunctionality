#!/usr/bin/env python3
"""
API to store the chrome windows & tabs.

This script provides functionality to store URLs of opened browser windows and tabs, and encrypts and saves them to a file.

Usage:
    python script_name.py [browser] [filename] [passphrase]

Make sure to replace 'script_name.py' with the actual name of this script.

Example:
    python script_name.py chrome urls.txt my_secret_passphrase

Note: Before using this script, you need to install the required modules using 'pip install pygetwindow pyautogui pyperclip'.

Module dependencies:
    - pygetwindow
    - pyautogui
    - pyperclip

"""

import importlib
import os
import argparse
import pygetwindow as gw
import pyautogui
import pyperclip
import my_crypto

def get_opened_browser_windows(browser_name="Google Chrome"):
    """
    Get a list of opened browser windows with the specified name.

    Args:
        browser_name (str): Name of the browser (default is "Google Chrome").

    Returns:
        list: A list of opened browser windows.
    """
    browser_windows = []
    for window in gw.getWindowsWithTitle(browser_name):
        browser_windows.append(window)
    return browser_windows

def get_opened_tabs_urls(window):
    """
    Get a list of URLs of opened tabs within a window.

    Args:
        window: The window to retrieve tab URLs from.

    Returns:
        list: A list of URLs of opened tabs in the window.
    """
    # Activate the window to make sure we are getting information from the right one
    window.activate()
    # Open a new tab to ensure the tab strip is visible
    pyautogui.hotkey("ctrl", "\t")
    # Go to the first tab (index 0)
    pyautogui.hotkey("ctrl", "1")
    # Get the URLs of the open tabs
    tab_urls = []
    while True:
        pyautogui.hotkey("ctrl", "\t")
        pyautogui.hotkey("ctrl", "l")  # Select the URL bar
        pyautogui.hotkey("ctrl", "c")  # Copy the URL
        tab_url = pyperclip.paste()
        if tab_url in tab_urls:  # Check if you rotate and got the same URL
            break
        tab_urls.append(tab_url)

    return tab_urls

def save_browser_windows_and_tabs(passphrase="test", file_path="urls.txt", urls=""):
    """
    Save browser windows and tabs URLs to a file.

    Args:
        passphrase (str): Passphrase for encryption and decryption (default is "my_secret_word").
        file_path (str): Path to the file where URLs will be saved (default is "urls.txt").
        urls (list): List of lists containing URLs of opened tabs in each window (default is an empty list).
    """
    file_string = ""
    for urllist in urls:
        for url in urllist:
            file_string += url
            file_string += '\n'
        file_string += '\n'

    encryptor = my_crypto.FileEncryptor(passphrase)
    encrypted_string = encryptor.encrypt_data(file_string.encode())

    with open(file_path, 'wb') as file:
        file.write(encrypted_string)

def install_and_import(package):
    """
    Install and import a Python package.

    Args:
        package (str): Name of the package to install and import.
    """
    try:
        importlib.import_module(package)
    except ImportError:
        import subprocess
        subprocess.check_call(["pip", "install", package])
    finally:
        globals()[package] = importlib.import_module(package)

# List of required modules
required_modules = ["pygetwindow", "pyautogui", "pyperclip"]

if __name__ == "__main__":
    for module in required_modules:
        install_and_import(module)

    parser = argparse.ArgumentParser(description="Save URLs of opened browser windows and tabs.")
    parser.add_argument("browser", choices=["chrome", "firefox", "edge"], default="chrome", nargs="?",
                        help="Choose browser (chrome/firefox/edge, default: chrome)")
    parser.add_argument("filename", default="urls.txt", nargs="?",
                        help="Name of the file to save URLs, default: urls.txt")
    parser.add_argument("passphrase", help="Passphrase for encryption and decryption")
   
    args = parser.parse_args()

    if args.browser == "chrome":
        browser_name = "Google Chrome"
    elif args.browser == "firefox":
        browser_name = "Mozilla Firefox"
    elif args.browser == "edge":
        browser_name = "Microsoft Edge"

    passphrase = args.passphrase.encode()

    file_path = args.filename

    browser_windows = get_opened_browser_windows(browser_name)
    urls = [get_opened_tabs_urls(window) for window in browser_windows]

    save_browser_windows_and_tabs(passphrase, file_path, urls)