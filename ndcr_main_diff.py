# -*- coding: utf-8 -*-

import requests
import argparse
import os
import zipfile

from ndcr_mod import pout, plog, endmsg

def main_diff_args(args: list) -> "ArgumentParser":
    parser = argparse.ArgumentParser(prog = "diff",
        description="Get new servers. ")
    parser.add_argument("old_zip", type=str, nargs=1,
                        help="Path to old zip-file.")
    parser.add_argument("new_zip", type=str, nargs=1,
                        help="Path to new zip-file.")
    parser.add_argument("out_zip", type=str, nargs=1,
                        help="Path to out zip-file.")
    args = parser.parse_args(args[1:])
    return args

def main_diff(argv: list):
    args = main_diff_args(argv)
    
    zip_1 = os.path.abspath(args.old_zip[0])
    zip_2 = os.path.abspath(args.new_zip[0])
    zip_3 = os.path.abspath(args.out_zip[0])

    with zipfile.ZipFile(zip_1, mode="r") as zfd1, zipfile.ZipFile(zip_2, mode="r") as zfd2, zipfile.ZipFile(zip_3, mode="w") as zfd3:
        files_1 = zfd1.namelist()
        files_2 = zfd2.namelist()
        files_1_bs = [os.path.basename(file_i) for file_i in files_1]
        files_1_bs_set = set(files_1_bs)
        for file_i in files_2:
            file_i_bs = os.path.basename(file_i)
            if(file_i_bs not in files_1_bs_set):
                zfd3.writestr(file_i_bs, zfd2.open(file_i).read())
    
    pout(endmsg())
