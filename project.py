#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import sys


"""
@author => OLM.
@version => 1.1
@date => 28/01/2020
@styleCode => PEP-8
@objective => Training with bs4.
@situation => final version 1.1.
"""


def showError(err):
    print(f"\n\n[!]ERROR => {err}")
    sys.exit(1)


def checkFields(obj):
    if len(obj) < 1:
        showError("The field cannot be empty")


def request(domain, userAgent, cookie):
    payload = {"user-agent": userAgent, "cookie": cookie}
    try:
        http = requests.get(domain, headers=payload)
    except Exception as err:
        showError(err)
    print("\n[!]Please wait...\n")
    if http.status_code == 200:
        print(f"[+]HTTPCODE => {http.status_code} (OK)\n")
        soup = BeautifulSoup(http.text, "html.parser")
        for link in soup.find_all("a"):
            print(link.get("href"))
    elif http.status_code == 302:
        print(f"[!]HTTPCODE => {http.status_code} (REDIRECT)")
        o = input("[!]Do you want to follow the redirect? (y/n)")
        if o.lower() == "y":
            try:
                http = requests.get(domain, allow_redirects=True)
            except Exception as err:
                showError(err)
            soup = BeautifulSoup(http.text, "html.parser")
            for link in soup.find_all("a"):
                print(link.get("href"))
        elif o.lower() == "n":
            print("[!]GOOD BYE")
            sys.exit(0)
        else:
            showError("Invalid option")
    elif http.status_code == 404:
        print(f"[-]HTTPCODE => {http.status_code} (NOT FOUND)")
        sys.exit(1)
    return 0


if __name__ == "__main__":
    try:
        d = input("[!]DOMAIN => ")
        checkFields(d)
        u = input("[!]USERAGENT => ")
        checkFields(u)
        c = input("[!]COOKIE => ")
        checkFields(c)
    except KeyboardInterrupt:
        showError("Aborted")
    request("http://" + d, u, c) if "http://" not in d else request(d, u, c)
