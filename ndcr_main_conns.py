# -*- coding: utf-8 -*-

import requests
import argparse
import os
import json
import zipfile

from ndcr_mod import pout, plog, load_json, save_json, endmsg

def mark_conns(conns_path: str, server_name: str, success: bool):
    d = load_json(conns_path)
    d[server_name][1] = d[server_name][1] + 1
    if(success):
        d[server_name][0] = d[server_name][0] + 1
    d = save_json(d, conns_path)

def main_initconns_args(args: list) -> "ArgumentParser":
    parser = argparse.ArgumentParser(prog = "initconns",
        description="Init connection file from zip with servers. ")
    parser.add_argument("in_zip_file", type=str, nargs=1,
                        help="Path to input zip-file.")
    parser.add_argument("out_file", type=str, nargs=1,
                        help="Path to output connection file.")
    args = parser.parse_args(args[1:])
    return args

def get_all_servers_from_zip(path_to_zip: str) -> list:
    with zipfile.ZipFile(path_to_zip, mode="r") as zfd:
        a = zfd.namelist()
    a = [os.path.basename(file_i) for file_i in a]
    a = [file_i[:file_i.find(".")] for file_i in a]
    res = sorted(list(set(a)))
    return res

def main_initconns(argv: list):
    """
    conns = json
    {
        "server_i": [successful_connection, all_tryings]
    }
    """
    args = main_initconns_args(argv)

    in_zip_file = os.path.abspath(args.in_zip_file[0])
    out_file = os.path.abspath(args.out_file[0])
    
    servers = get_all_servers_from_zip(in_zip_file)
    d = {}
    for server_i in servers:
        d[server_i] = [0, 0]
    save_json(d, out_file)

    pout(endmsg())



def main_mergeconns_args(args: list) -> "ArgumentParser":
    parser = argparse.ArgumentParser(prog = "mergeconns",
        description="Merge connection files. ")
    parser.add_argument("connection_file_1", type=str, nargs=1,
                        help="Path to connection file 1.")
    parser.add_argument("connection_file_2", type=str, nargs=1,
                        help="Path to connection file 2.")
    parser.add_argument("out_file", type=str, nargs=1,
                        help="Path to output connection file.")
    args = parser.parse_args(args[1:])
    return args

def main_mergeconns(argv: list):
    args = main_mergeconns_args(argv)

    in_file_1 = os.path.abspath(args.connection_file_1[0])
    in_file_2 = os.path.abspath(args.connection_file_2[0])
    out_file = os.path.abspath(args.out_file[0])

    d1, d2 = load_json(in_file_1), load_json(in_file_2)

    d2_keys = list(d2.keys())
    for d2_key_i in d2_keys:
        if d2_key_i in d1:
            d1[d2_key_i] = [d1[d2_key_i][0] + d2[d2_key_i][0], d1[d2_key_i][1] + d2[d2_key_i][1]]
        else:
            d1[d2_key_i] = d2[d2_key_i]
    
    save_json(d1, out_file)

    pout(endmsg())



def main_topconns_args(args: list) -> "ArgumentParser":
    parser = argparse.ArgumentParser(prog = "topconns",
        description="Show top of the best connections. ")
    parser.add_argument("connection_file", type=str, nargs=1,
                        help="Path to connection file 1.")
    parser.add_argument("--reverse", default=False, action='store_true',
                        help="Revers top of connections.")
    parser.add_argument("--only_success", default=False, action='store_true',
                        help="Consider only successfully connecting")
    args = parser.parse_args(args[1:])
    return args

def lower_topconns(conn_file: str, if_reverse: bool, only_success: bool):
    d = load_json(conn_file)
    if_reverse = not if_reverse
    
    if(only_success == True):
        fu = lambda item: item[1][0]
    else:
        fu = lambda item: item[1][0] / item[1][1] if item[1][1] != 0 else 0

    d = dict(sorted(d.items(), key=fu, reverse=if_reverse))
    return d

def main_topconns(argv: list):
    args = main_topconns_args(argv)

    conn_file = os.path.abspath(args.connection_file[0])
    if_reverse = args.reverse
    only_success = args.only_success

    d = lower_topconns(conn_file, if_reverse, only_success)

    for i, d_i in enumerate(d):
        rate = d[d_i][0]/d[d_i][1] if d[d_i][1] != 0 else 0
        pout(f"{i+1}: {d_i}=[success={d[d_i][0]}, all={d[d_i][1]}, rate={rate}]")
    
    pout(endmsg())
