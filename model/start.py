# -*- encoding: utf-8 -*-
'''
@File    :   start.py
@Time    :   2021/02/25 13:06:37
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
'''

# here put the import lib
from re import A
from typing import Tuple
from PyQt5.QtCore import QThread, pyqtSignal, QProcess,QStringListModel
import urllib3
import os
import json
import subprocess
from threading import Thread
from queue import Queue
import time

global DL_STEAMCMD_STATUS,msg

DL_STEAMCMD_STATUS = False
msg = Queue(20)

class STMDL(Thread):
    def __init__(self):
        'This is init fun'
        Thread.__init__(self)
        self.daemon = True
        self.dir = os.getcwd()
        if "\\" in self.dir:
            self.dir = self.dir.replace("\\", "/")

    def download(self):
        command = self.dir+'/steamcmd/steamcmd.exe'
        print(command)
        steam_init_log = subprocess.Popen(command,stdout=subprocess.PIPE)
        #steam_init_log.communicate()
        for line in iter(steam_init_log.stdout.readline, b''):
            #line_out = line.decode("GBK")
            #print(line_out)
            if not subprocess.Popen.poll(steam_init_log) is None:
                if line == "":
                    break
        steam_init_log.stdout.close()
        with open("config.json") as fa:
            get_json = json.loads(fa.read())
        get_json["steamcmd"]["fullfile"] = 1
        with open("config.json","w") as fb:
            fb.write(json.dumps(get_json,indent=4))
        print("下载完成")

    def run(self):
        self.download()
        
class FORESTDL(Thread):
    def __init__(self):
        'This is init fun'
        Thread.__init__(self)
        self.daemon = True
        self.dir = os.getcwd()
        if "\\" in self.dir:
            self.dir = self.dir.replace("\\", "/")

    def download(self):
        command = self.dir+'/steamcmd/steamcmd.exe +login anonymous +force_install_dir ' + self.dir + '/ThrForestDedicatedServer +app_update 556450 validate  +quit'
        print(command)
        steam_init_log = subprocess.Popen(command,stdout=subprocess.PIPE)
        #steam_init_log.communicate()
        for line in iter(steam_init_log.stdout.readline, b''):
            #line_out = line.decode("GBK")
            #print(line_out)
            if not subprocess.Popen.poll(steam_init_log) is None:
                if line == "":
                    break
        steam_init_log.stdout.close()
        with open("config.json") as fa:
            get_json = json.loads(fa.read())
        get_json["theforest"]["fullfile"] = 1
        with open("config.json","w") as fb:
            fb.write(json.dumps(get_json,indent=4))
        print("下载完成")

    def run(self):
        self.download()


class START(QThread):
    trg = pyqtSignal(str)
    initt = pyqtSignal(str)

    def __init__(self) -> None:
        QThread.__init__(self)
        self.dir = os.getcwd()
        if "\\" in self.dir:
            self.dir = self.dir.replace("\\", "/")

    def makedir(self):
        self.trg.emit("准备创建文运行件目录")
        if not os.path.isdir("steamcmd"):
            self.trg.emit("准备创建steamcmd目录")
            os.mkdir(self.dir + "/steamcmd")
            self.trg.emit("创建steamcmd目录成功")
        if not os.path.isdir("ThrForestDedicatedServer"):
            self.trg.emit("准备创建ThrForestDedicatedServer目录")
            os.mkdir(self.dir + "/ThrForestDedicatedServer")
            self.trg.emit("创建ThrForestDedicatedServer目录成功")
            
    def dl_steamcmd(self):
        self.trg.emit("准备下载steamcmd.exe文件")
        if not os.path.exists(self.dir + "/steamcmd/steamcmd.exe"):
            with open("config.json") as fp:
                dl_url = json.loads(fp.read())["steamcmd"]["url"]
            http_pool = urllib3.PoolManager()
            get_data = http_pool.request("GET", dl_url)
            with open(self.dir + "/steamcmd/steamcmd.exe", "wb") as f:
                f.write(get_data.data)
            self.trg.emit("steamcmd.exe下载完毕")
        else:
            self.trg.emit("steamcmd.exe文件存在")

    def stm_test(self):
        self.trg.emit("开始初始化steamcmd")
        ak = QProcess()
        #ak.setProcessChannelMode(QProcess.ForwardedChannels)
        a = ak.start(self.dir+'/steamcmd/steamcmd.exe +' +
                     'login anonymous +force_install_dir ' + self.dir + '/ThrForestDedicatedServer')
        print(a)
        self.trg.emit("steamcmd初始化完毕")
        
    def steam_dl(self):
        self.trg.emit("开始初始化steamcmd")
        stmdl = STMDL()
        stmdl.start()
        while True:
            with open("config.json") as fp:
                dl_ok = json.loads(fp.read())["steamcmd"]["fullfile"]
            if dl_ok == 0:
                time.sleep(2)
                self.trg.emit("文件下载中……")
            else:
                break
        self.trg.emit("steamcmd文件下载完成")
        
    def theforest_dl(self):
        self.trg.emit("开始初始化TheForest服务端文件")
        forestdl = FORESTDL()
        forestdl.start()
        while True:
            with open("config.json") as fp:
                dl_ok = json.loads(fp.read())["theforest"]["fullfile"]
            if dl_ok == 0:
                time.sleep(2)
                self.trg.emit("文件下载中……")
            else:
                break
        self.trg.emit("theforest文件下载完成")
        

    def run(self):
        self.makedir()
        self.dl_steamcmd()
        # self.initt.emit("ok")
        #self.steamcmd_init()
        #self.stm_test()
        self.steam_dl()
        self.theforest_dl()
