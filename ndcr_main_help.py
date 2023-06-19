# -*- coding: utf-8 -*-

import requests
import argparse
import os

from ndcr_mod import pout, plog, endmsg

def main_help_args(args: list) -> "ArgumentParser":
    parser = argparse.ArgumentParser(prog = "help",
        description="Help text. ")
    args = parser.parse_args(args[1:])
    return args

def main_help(argv: list):
    args = main_help_args(argv)
    
    HELP_TEXT = """
nordcrutchnectok is wrapper over nordvpn.
It helps to find working servers and keep connections.

                Steps to set up nordvpn:
1. Download and install nordvpn.
2. Run:
sudo usermod -aG nordvpn $USER
sudo reboot now
sudo systemctl enable nordvpnd
sudo reboot now
3. Configure as needed:
nordvpn settings --help

                Steps to look modules help:

To look available modules run:
nordcrutchnectok

Call help with module:
nordcrutchnectok {module_name} --help

                Steps to begin:
Download list of servers:
nordcrutchnectok download {path_to_out_file.zip}

Init {connections_file}:
nordcrutchnectok initconns {path_to_servers.zip} {path_to_connection_file.json}

Connect:
nordcrutchnectok connect {path_to_out_connections.json}

Or keepconnect:
nordcrutchnectok keepconnect {path_to_out_connections.json}

Disconnect:
nordcrutchnectok disconnect {path_to_out_connections.json}

With each successful/unsuccessful connection, 
the server labels are updated accordingly in {connection_file}.
So it can be finded the bests servers. To use bests servers use flag "--mode".
nordcrutchnectok keepconnect {path_to_out_connections.json} --mode {0, 1, 2, 3}

                Steps to get fresh servers:

To find new/fresh servers, follow these steps:

Download servers:
nordcrutchnectok download {servers_old.zip}

Wait a few weeks and download servers again:
nordcrutchnectok download {servers_new.zip}

Get new servers {servers_fresh.zip}:
nordcrutchnectok diff {servers_old.zip} {servers_new.zip} {servers_fresh.zip}

"""
    pout(HELP_TEXT)

    pout(endmsg())