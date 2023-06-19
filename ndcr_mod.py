 
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import datetime
import json
import argparse

class GL:
    INF = "nordtun" # "nordlynx" for wireguard
    LOG_FILE = None
    WHERE_PING = "8.8.8.8"

def pout(msg : str):
    print(msg)
    sys.stdout.flush()

def plog(log_msg: str):
    out = get_time() + " " + log_msg
    pout(out)
    if(GL.LOG_FILE != None):
        with open(GL.LOG_FILE, "a", encoding="utf-8") as fd:
            fd.write(pout)
            fd.write("\n")
            fd.flush()

def endmsg() -> str:
    return "\n" + "="*10 + "DONE!" + "="*10

def exe(command: str, debug: bool = True, std_out_fd = subprocess.PIPE, std_err_fd = subprocess.DEVNULL, stdin_msg: str = None) -> tuple:
    '''
    Аргумент command - команда для выполнения в терминале. Например: "ls -lai ."
    if(std_out_fd or std_err_fd) == subprocess.DEVNULL   |=>    No output enywhere
    if(std_out_fd or std_err_fd) == subprocess.PIPE      |=>    All output to return
    if(std_out_fd or std_err_fd) == open(path, "w")      |=>    All output to file path
    Возвращает кортеж, где элементы:
        0 - строка stdout
        1 - строка stderr
        2 - returncode
    '''
    _ENCODING = "utf-8"

    if(debug):
        #pout(f"> " + " ".join(command))
        if(stdin_msg != None):
            pout(f"> {command}, with stdin=\"{stdin_msg}\"")
        else:
            pout(f"> {command}")

    #proc = subprocess.run(command, shell=True, capture_output=True, input=stdin_msg.encode("utf-8"))
    if(stdin_msg == None):
        proc = subprocess.run(command, shell=True, stdout=std_out_fd, stderr=std_err_fd)
    else:
        proc = subprocess.run(command, shell=True, stdout=std_out_fd, stderr=std_err_fd, input=stdin_msg.encode("utf-8"))
    
    #return (proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8"))

    res_stdout = proc.stdout.decode("utf-8") if proc.stdout != None else None
    res_errout = proc.stderr.decode("utf-8") if proc.stderr != None else None
    return (res_stdout, res_errout, proc.returncode)

def is_int(x : str):
    try:
        tempVal = int(x)
        return True
    except:
        return False

def errorExit(msg : str, prefix = "\nError: "):
    print(prefix + msg)
    exit()

def get_time() -> str:
    time_stamp = datetime.datetime.now().strftime("[%y.%m.%d %H:%M:%S.%f]")
    return time_stamp

def save_json(d: dict, json_save_path: str):
    with open(json_save_path, "w", encoding="utf-8") as fd:
        dump_str = json.dumps(d)
        fd.write(dump_str)
        fd.flush()

def load_json(json_path: str) -> dict:
    with open(json_path, "r", encoding="utf-8") as fd:
        json_text = fd.read()
        res = json.loads(json_text)
    return res

def get_infs() -> str:
    #return exe("ip link show")[0]
    return exe("ip addr")[0]
