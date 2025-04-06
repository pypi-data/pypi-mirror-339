#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/17 13:14
# @Author  : 兵
# @email    : 1747193328@qq.com
import os
import subprocess
import threading
import time
from collections.abc import Iterable
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QApplication
from loguru import logger
from qfluentwidgets import StateToolTip
from NepTrainKit.version import UPDATE_EXE, UPDATE_FILE, NepTrainKit_EXE

from NepTrainKit.core import   Config


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 调用原始函数
        end_time = time.time()  # 记录结束时间
        logger.debug(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper





import os

def check_path_type(path):
    """
    判断路径是文件夹还是文件，即使路径不存在。

    参数:
        path (str): 路径字符串。

    返回:
        str: "folder"（文件夹）、"file"（文件）或 "unknown"（未知或不存在）。
    """
    if os.path.isdir(path):
        return "folder"
    elif os.path.isfile(path):
        return "file"
    else:
        # 如果路径不存在，进一步检查是否有文件扩展名
        if os.path.splitext(path)[1]:  # 如果有扩展名，可能是文件
            return "file"
        else:  # 否则可能是文件夹
            return "folder"


def call_path_dialog(self, title, dialog_type="file", default_filename="", file_filter="", selected_filter=""):
    dialog_map = {
        "file": lambda: QFileDialog.getSaveFileName(self, title, os.path.join(Config.get_path(), default_filename), file_filter, selected_filter),
        "select": lambda: QFileDialog.getOpenFileName(self, title, Config.get_path(), file_filter),
        "selects": lambda: QFileDialog.getOpenFileNames(self, title, Config.get_path(), file_filter),
        "directory": lambda: QFileDialog.getExistingDirectory(self, title, Config.get_path())
    }

    dialog_func = dialog_map.get(dialog_type)
    if not dialog_func:
        return None

    path = dialog_func()

    if isinstance(path, tuple):
        path = path[0]  # 处理 `getSaveFileName` 和 `getOpenFileName` 返回的 tuple
    elif isinstance(path, list):
        if not path:
            return None
        path = path[0]  # `getOpenFileNames` 返回 list

    if not path:
        return None

    # 提取目录并保存到配置
    if check_path_type(path)=="file":
        last_dir = os.path.dirname(path)
    else:
        last_dir = path

    Config.set("setting", "last_path", last_dir)
    return path

def unzip( ):

    cmd = f"ping -n 3 127.0.0.1&{UPDATE_EXE} {UPDATE_FILE}&ping -n 2 127.0.0.1&start {NepTrainKit_EXE}"

    subprocess.Popen(cmd, shell=True)
    if QApplication.instance():
        QApplication.instance().exit()
    else:
        quit()


class LoadingThread(QThread):
    progressSignal = Signal(int)
    def __init__(self,parent=None,show_tip=True,title='running'):
        super(LoadingThread,self).__init__(parent)
        self.show_tip=show_tip
        self.title=title
        self._parent=parent
    def run(self ):
        result = self.func()
        if isinstance(result, Iterable):
            for i,_ in enumerate(result):
                self.progressSignal.emit(i)
    def start_work(self,func,*args,**kwargs):
        if self.show_tip:
            self.tip = StateToolTip(self.title, 'Please wait patiently~~', self._parent)
            self.tip.show()
            self.finished.connect(self.__finished_work)
            self.tip.closedSignal.connect(self.quit)
        else:
            self.tip=None
        self.func=lambda : func(*args,**kwargs)
        self.start()
    def __finished_work(self ):
        if self.tip:
            self.tip.setContent('任务完成啦 😆')
            self.tip.setState(True)
    def stop_work(self ):
        self.terminate()