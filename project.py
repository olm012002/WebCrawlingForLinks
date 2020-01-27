#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import sys

"""
@author => OLM.
@version => 1.0
@date => 27/01/2020
@objective => Training with bs4.
@situation => Under development.
"""

def showError(err):
    print(f"\n\n[!]ERROR => {err}")
    sys.exit(1)


def request(domain, userAgent = "", cookie = ""):
    payload = {"user-agent": userAgent, "cookie": cookie}
    try:
        http = requests.get(domain, headers=payload)
    except requests.ConnectionError as err:
        showError(err)
    print("\n[!]Please wait...\n")
    if http.status_code == 200:
        print(f"[+]HTTPCODE => {http.status_code} (OK)\n")
        print(http.text())
    elif http.status_code == 302:
        print(f"[!]HTTPCODE => {http.status_code} (REDIRECT)")
        o = input("[!]Do you want to follow the link? (y/n)")
        if o.lower() == "y":
            try:
                http = requests.get(domain, allow_redirects=True)
            except requests.ConnectionError as err:
                showError(err)
            print(f"\n{http.text()}")
        elif o.lower() == "n":
            print("[!]GOOD BYE")
            sys.exit(0)
        else:
            showError("Invalid option")
    elif http.status_code == 404:
        print(f"[-]HTTPCODE => {http.status_code} (NOT FOUND)")
        sys.exit(1)

if __name__ == "__main__":
    try:
        d = input("[!]DOMAIN => ")
        u = input("[!]USERAGENT => ")
        c = input("[!]COOKIE => ")
    except:
        showError("Aborted")
    request(d, u, c)
