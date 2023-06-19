# -*- coding: utf-8 -*-

import requests
import argparse
import os

from ndcr_mod import pout, plog, endmsg

def main_download_args(args: list) -> "ArgumentParser":
    parser = argparse.ArgumentParser(prog = "download",
        description="Download ovpn.zip. ")
    parser.add_argument("out_zip_file", type=str, nargs=1,
                        help="Path to output zip-file.")
    args = parser.parse_args(args[1:])
    return args

def main_download(argv: list):
    args = main_download_args(argv)
    
    out_file = os.path.abspath(args.out_zip_file[0])
    url = "https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip"
    plog(f"Getting \"ovpn.zip\" from \"{url}\"...")
    r = requests.get(url)
    plog(f"Saving to \"{out_file}\"...")
    with open(out_file, "wb") as fd:
        fd.write(r.content)
        fd.flush()
    pout(endmsg())