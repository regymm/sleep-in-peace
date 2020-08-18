#!/usr/bin/env python3
# SiliTune, a CPU power manager, by petergu

import sys
import os
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

prj_name = "SleepInPeace"

cmd_get_window_pid = "xprop _NET_WM_PID | cut -d' ' -f3"
cmd_stop = "kill -STOP "
cmd_cont = "kill -CONT "

tmp_file = "/tmp/sleepinpeace.txt"

stopped_list = []

label_callback = None


def runresult(cmd, msg="Haha"):
    sts, out = subprocess.getstatusoutput(cmd)
    if sts != 0:
        print('Error:' + msg + '\nCommand:' + cmd + '\nMessage:' + out)
    return (sts, out)


def get_a_window_pid():
    return runresult(cmd_get_window_pid)[1]


def stop_a_window(pid):
    global stopped_list
    if(runresult(cmd_stop + str(pid))[0] == 0):
        stopped_list.append(pid)


def cont_a_window(pid):
    global stopped_list
    try:
        if(runresult(cmd_cont + str(pid))[0] == 0):
            stopped_list.remove(pid)
    except ValueError:
        pass


def resume_all():
    global stopped_list
    stopped_list_bak = [i for i in stopped_list]
    for i in stopped_list_bak:
        cont_a_window(i)


def pid2name(pid):
    return runresult('ps -p ' + str(pid) + ' -o comm=')[1]


def updatelabelandtmp():
    global stop_list
    global tmp_file
    global label_callback
    labeltext = "Paused windows:\n" + ''.join([str(pid) + '\t\t' + pid2name(pid) + '\n' for pid in stopped_list])
    print(labeltext)
    label_callback.setText(labeltext)
    with open(tmp_file, 'w') as f:
        f.write(labeltext)
        f.close()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = prj_name
        self.setWindowTitle(self.title)
        self.initui()
        self.show()

    def initui(self):
        vbox = QVBoxLayout()
        name_label = QLabel('Sleep In Peace v1.0\nUse taskbar icon to do pause or resume windows.')
        vbox.addWidget(name_label)
        list_label = QLabel('')
        global label_callback
        label_callback = list_label
        updatelabelandtmp()
        vbox.addWidget(list_label)
        self.setLayout(vbox)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None, body=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        menu.triggered.connect(self.actions)
        menu.addAction("Pause a window")
        menu.addAction("Resume a window")
        menu.addAction("Resume all paused")
        menu.addAction("Show")
        menu.addAction("Hide")
        menu.addAction("Exit")
        self.setContextMenu(menu)
        self.body = body

    def actions(self, q):
        text = q.text()
        print(text + " is triggered from system tray.")
        if text == 'Exit':
            QCoreApplication.exit()
        elif text == 'Pause a window':
            stop_a_window(get_a_window_pid())
            updatelabelandtmp()
        elif text == 'Resume a window':
            cont_a_window(get_a_window_pid())
            updatelabelandtmp()
        elif text == 'Resume all paused':
            resume_all()
            updatelabelandtmp()
        elif text == 'Show':
            self.body.show()
            on_front = 1
        elif text == 'Hide':
            self.body.hide()


if __name__ == '__main__':
    print(prj_name + " started running...")
    app = QApplication(sys.argv)
    ex = App()
    w = QWidget()
    trayIcon = SystemTrayIcon(QIcon("icon.png"), w, body=ex)
    trayIcon.show()
    app.exec_()
    print("Goodbye.")
    sys.exit(0)
