# -*- coding: utf-8 -*-

import requests
import argparse
import os
import random
import time
import subprocess

from ndcr_mod import GL, pout, plog, errorExit, exe, load_json, save_json, get_infs, endmsg

from ndcr_main_conns import lower_topconns, mark_conns

def main_connect_add_args(parser: "parser") -> "parser":
    # if changed, then change connection_args in main_keepconnect
    parser.add_argument("connections_file", type=str, nargs=1,
                        help="Path to connections file.")
    parser.add_argument("--mode", type=int, choices=[0,1,2], default=0, required=False,
                        help="modes: 0 - connect to random server, " +
                                    "1 - connect to bests servers, " + 
                                    "2 - connect to bests servers (consider only successfull connection), " + 
                                    "3 - just connect (not consider {connections_file}). Default is 0.")
    parser.add_argument("--trying_connect", type=int, default=3, required=False,
                        help="Number of attempts in case of a failed connection before trying another server. Default is 3.")
    parser.add_argument("--tunneling_inf", type=str, default=None, required=False,
                       help="Specified interface.")
    parser.add_argument("--delay_before_ping", type=int, default=5, required=False,
                        help="Delay (seconds) before start ping if connection is successful. Default is 5 (seconds).")
    return parser

def main_connect_args(args: list) -> "ArgumentParser":
    parser = argparse.ArgumentParser(prog = "connect",
        description="Connect to servers. ")

    parser = main_connect_add_args(parser)

    args = parser.parse_args(args[1:])
    return args

def ifping() -> bool:
    anw = exe(f"ping -c 10 -I {GL.INF} {GL.WHERE_PING}", debug=False, std_err_fd=subprocess.PIPE)
    if(anw[1] != ""):
        return False
    if(anw[0].find(", 0% packet loss") != -1):
        return True
    else:
        return False

def try_one_connect(server_name: str) -> True or False or None:
    """
    @return True if connect success
            False if connect fail
            None if the server is not configured for this type of connection
    """
    for pta_i in range(GL.connect_PleaseTryAgain_number):
        command = f"nordvpn connect {server_name}"
        r = exe(command)
        if(r[0].find("nordvpnd.sock not found") != -1): # r[2] == 1
            # ('\r\rWhoops! /run/nordvpn/nordvpnd.sock not found.\n', '', 1)
            # deamon not started
            errorExit("nordvpnd not started. Start it: \"> sudo systemctl start nordvpnd\"")
        if(r[0].find("ermission denied") != -1): # r[2] == 1
            # ("\r\rWhoops! Permission denied accessing /run/nordvpn/nordvpnd.sock.\nRun 'usermod -aG nordvpn $USER' 
            # to fix this issue and log out of OS afterwards for this to take an effect.\n", '', 1)
            errorExit(f"Problem with user permissions: \n{r[0]} \n\n\n\t\t\tFix it and restart system. \n")
        elif(r[0].find("e couldn") != -1 and r[0].find("t connect you to") != -1): # r[2] == 1
            # ("...Connecting to COUNTRY #NNN (SERVER_NAME.nordvpn.com)...
            # Whoops! We couldn't connect you to 'SERVER_NAME'. Please try again. If the problem persists, contact our customer support.", "", 1)
            # 
            pout(f"\"Please try again\" error ({server_name}) ({pta_i+1}). ")
        elif(r[0].find("he specified server is not available") != -1 and r[0].find("not support your connection settings") != -1): # r[2] == 1
            # ('...The specified server is not available at the moment or does not support your connection settings...', '', 1)
            pout(f"\"Not support your connection settings\" error ({server_name}). ")
            return None
        elif(r[0].find("he specified server does not exist") != -1): # r[2] == 1
            # ('...The specified server does not exist...', '', 1)
            pout(f"Server {server_name} does not exist. ")
            return None
        elif(r[0].find("ou are connected to") != -1): # r[2] == 0
            # ('...Connecting to COUNTRY #NNN (SERVER_NAME.nordvpn.com)...
            # You are connected to COUNTRY #NNN (SERVER_NAME.nordvpn.com)!...', '', 0)
            time.sleep(GL.connect_delay_before_ping)
            PINGED = ifping()
            if(PINGED == False):
                pout(f"Server {server_name} is not working. Disconnecting... ")
                r = exe("nordvpn disconnect")
                if(r[2] != 0):
                    plog(f"ERROR WHILE DISCONNECTING! \n{r}\n")
                return False
            else:
                return True
        elif(r[0].find("ou are not logged in")): # r[2] == 1
            # ('\r-\r \r\r-\r \rYou are not logged in.\n', '', 1)
            pout(f"\"You are not logged in\" error! Login again by executing \"> nordvpn login\". ")
            if(GL.do_end_arg):
                try:
                    plog(f"Executing command end: \"{args.do_end}\": ")
                    r = exe(args.do_end, std_err_fd=subprocess.PIPE)
                    pout(f"Output: \n{r}\n\n")
                except:
                    pout(f"Error while executing command!!!")
            while(True):
                pout(f"Exit and disconnect manually by CTRL+C. Bye")
                time.sleep(999*99)
        else:
            pout(f"(ndcr_main_connect.try_one_connect) Failed successully. Another branch. Unknown error")
            return None

    return False

def main_connect(argv: list):
    args = main_connect_args(argv)

    main_disconnect([])
    
    conn_file = os.path.abspath(args.connections_file[0])
    mode = args.mode
    GL.connect_PleaseTryAgain_number = args.trying_connect
    if(GL.connect_PleaseTryAgain_number <= 0):
        errorExit(f"trying_connect={args.trying_connect} cannot be less 1. ")
    GL.connect_delay_before_ping = args.delay_before_ping
    if(GL.connect_delay_before_ping <= 0):
        errorExit(f"delay_before_ping={args.delay_before_ping} cannot be less 1. ")
    if(args.tunneling_inf != None):
        GL.INF = args.tunneling_inf

    if(mode == 0):
        d = load_json(conn_file)
        buff = list(d.items())
        random.shuffle(buff)
        servers = dict(buff)
    if(mode == 1):
        servers = lower_topconns(conn_file, False, False)
    if(mode == 2):
        servers = lower_topconns(conn_file, False, True)
    if(mode == 3):
        servers = {"": [0, 0]}

    infs_before = get_infs()
    whileTrue, gi, gi_var = True, 0, None
    keep_connect_fuffix = ""
    while(whileTrue):
        for server_i in servers:
            gi += 1
            if(GL.keepconnect_gi != None):
                keep_connect_fuffix = f"{GL.keepconnect_gi}|"
            pout("")
            plog(f"\n({keep_connect_fuffix}{gi}) Connecting to \"{server_i}\"...")
            is_success = try_one_connect(server_i)
            if(is_success != None):
                if(mode != 3):
                    mark_conns(conn_file, server_i, is_success)
            if(is_success == True):
                gi_var = server_i
                whileTrue = False
                break
            else:
                pout(f"Cannot connect to \"{server_i}\", trying another one...")
    infs_after = get_infs()
    pout(f"Interfaces before: \n{infs_before} \n\nInterfaces after: \n {infs_after}\n")
    plog(f"{'='*10}Connected to \"{server_i}\"!{'='*10}")
    pout(endmsg())



def main_disconnect_args(args: list) -> "ArgumentParser":
    parser = argparse.ArgumentParser(prog = "disconnect",
        description="Disconnect from server. ")
    args = parser.parse_args(args[1:])
    return args

def main_disconnect(argv: list):
    plog("Disconnecting...")
    args = main_disconnect_args(argv)

    infs_before = get_infs()

    r = exe("nordvpn disconnect")
    if(r[2] != 0):
        plog(f"ERROR WHILE DISCONNECTING! \n{r}\n")

    infs_after = get_infs()
    pout(f"Interfaces before: \n{infs_before} \n\nInterfaces after: \n {infs_after}\n")

    pout(endmsg())



def main_keepconnect_args(args: list) -> "ArgumentParser":
    parser = argparse.ArgumentParser(prog = "keepconnect",
        description="Keep connection to servers, if connection is lost.")

    parser = main_connect_add_args(parser)

    parser.add_argument("--do_before", type=str, default=None, required=False,
                       help="Execute this command before reset connection.")
    parser.add_argument("--do_after", type=str, default=None, required=False,
                       help="Execute this command after the connection is established.")
    parser.add_argument("--do_end", type=str, default=None, required=False,
                       help="Execute this command before reset connection.")

    args = parser.parse_args(args[1:])
    return args

def ifkeepping(deep: int = 0) -> bool:
    MAX_DEEP = 5
    anw = exe(f"ping -c 10 -I {GL.INF} {GL.WHERE_PING}", debug=False, std_err_fd=subprocess.PIPE)
    if(anw[1] != ""):
        if(deep < MAX_DEEP):
            time.sleep(5)
            return ifkeepping(deep+1)
        else:
            return False
    if(anw[0].find(", 100% packet loss") != -1):
        if(deep < MAX_DEEP):
            time.sleep(5)
            return ifkeepping(deep+1)
        else:
            return False
    else:
        return True

def main_keepconnect(argv: list):
    args = main_keepconnect_args(argv)

    GL.keepconnect_gi = 0

    connect_args = ["connect", args.connections_file[0], "--mode", str(args.mode),
    "--trying_connect", str(args.trying_connect),
    "--delay_before_ping", str(args.delay_before_ping)]
    if(args.tunneling_inf != None):
        connect_args.append("--tunneling_inf")
        connect_args.append(args.tunneling_inf)
    
    if(args.do_end != None):
        GL.do_end_arg = args.do_end

    plog("KEEPCONNECT STARTING... \n")
    time.sleep(5)

    while(True):
        if(args.do_before != None):
            plog(f"Executing command before: \"{args.do_before}\": ")
            r = exe(args.do_before, std_err_fd=subprocess.PIPE)
            pout(f"Output: \n{r}")

        GL.keepconnect_gi += 1
        pout("\n")
        plog(f"keepconnect {GL.keepconnect_gi}: ")

        main_connect(connect_args)

        if(args.do_after != None):
            plog(f"Executing command after: \"{args.do_after}\": ")
            r = exe(args.do_after, std_err_fd=subprocess.PIPE)
            pout(f"Output: \n{r}\n\n")

        while(True):
            PINGED = ifkeepping()
            if(PINGED == False):
                break
            time.sleep(5)
        plog(f"({GL.keepconnect_gi}) Connection is broken. Connecting again...")
        
        if(args.do_end != None):
            plog(f"Executing command end: \"{args.do_end}\": ")
            r = exe(args.do_end, std_err_fd=subprocess.PIPE)
            pout(f"Output: \n{r}\n\n")
        
        # main_disconnect([])
    
    pout(endmsg()) # =)
