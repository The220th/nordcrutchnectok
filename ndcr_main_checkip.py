# -*- coding: utf-8 -*-

import requests
import argparse
import os
import requests

from ndcr_mod import pout, plog, endmsg, exe

def main_checkip_args(args: list) -> "ArgumentParser":
    parser = argparse.ArgumentParser(prog = "checkip",
        description="Request IP from sites {\"https://ifconfig.me\", \"https://ipinfo.io/ip\", \"https://ipecho.net/plain\"}. ")
    args = parser.parse_args(args[1:])
    return args

def main_checkip(argv: list):
    args = main_checkip_args(argv)
    SITES = ["https://ifconfig.me", "https://ipinfo.io/ip", "https://ipecho.net/plain"]

    for site_i in SITES:
        r = requests.get(site_i)
        ip = r.text
        pout(f"{ip} <-> {site_i}")
    
    pout(endmsg())

def main_checkip_legacy(argv: list):
    args = main_checkip_args(argv)
    
    command = f"curl ifconfig.me"
    anw = exe(command)
    #if(anw[1] != ""):
    #    errorExit(f"\n\n=====\nPROBLEM IN \"{command}\": {anw[1]}\n=====\n")
    ip1 = anw[0]

    command = f"curl ipinfo.io/ip"
    anw = exe(command)
    #if(anw[1] != ""):
    #    errorExit(f"\n\n=====\nPROBLEM IN \"{command}\": {anw[1]}\n=====\n")
    ip2 = anw[0]

    command = f"curl ipecho.net/plain"
    anw = exe(command)
    #if(anw[1] != ""):
    #    errorExit(f"\n\n=====\nPROBLEM IN \"{command}\": {anw[1]}\n=====\n")
    ip3 = anw[0]

    pout("Your ip: ")
    print(f"\tifconfig.me:       {ip1}")
    print(f"\tipinfo.io/ip:      {ip2}")
    print(f"\tiipecho.net/plain: {ip3}")

    pout("\n===FINISH===")