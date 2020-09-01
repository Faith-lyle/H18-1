# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：H18-1 -> uploadData
@IDE    ：PyCharm
@Author ：Lyle.Hou
@Date   ：2020/8/25 16:22
@Desc   ：
=================================================='''
import os
import shutil
import socket
import time
from tkinter import *
import threading

Close = False


def UploadingData():  # 上传文件主方法
    # path1为本地电脑前一天的测试log文件夹
    path1 = os.path.join(os.path.expanduser("~"), 'Desktop') + '/test_log/' + str(
        time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400)))
    # path11为本地电脑当天的测试log文件夹
    path11 = os.path.join(os.path.expanduser("~"), 'Desktop') + '/test_log/' + str(
        time.strftime("%Y-%m-%d", time.localtime(time.time())))
    # url为网络地址
    url = r'\\10.102.170.16\Data'
    # hostname为本机IP地址
    hostname = socket.gethostname()
    # IP为hostname把.替换成-的字符串
    ip = socket.gethostbyname(hostname).replace('.', '-')
    # 检查网盘是否存在当前IP的文件夹
    if not os.path.exists(url + '/' + ip):
        # 在网盘中创建当前IP的文件夹
        os.mkdir(url + '/' + ip)
    # 判断本地桌面下是否存在当前和前一天的文件夹
    if os.path.exists(path1) and os.path.exists(path11):
        path2 = url + '/' + ip + '/' + str(time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400)))
        path3 = url + '/' + ip + '/' + str(time.strftime("%Y-%m-%d", time.localtime(time.time())))
        # 判断网盘是否存在昨天的文件夹夹
        if os.path.exists(path2):
            # 删除文件夹
            shutil.rmtree(path2)
        # 复制文件夹
        shutil.copytree(path1, path2)
        # 判断网盘是否存在今天的文件夹夹
        if os.path.exists(path3):
            # 删除文件夹
            shutil.rmtree(path3)
        # 复制文件夹
        shutil.copytree(path11, path3)


class Applicaton(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.Total = IntVar(master=self.master)
        self.Total.set(value=0)
        self.Succesful = IntVar(master=self.master)
        self.Succesful.set(value=0)
        self.Failure = IntVar(master=self.master)
        self.Failure.set(value=0)
        self.widgets()
        self.SendData()

    def widgets(self):
        F1 = Frame(master=self.master)
        F1.pack()
        Label(master=F1, text="自动上传数据软件", font=("黑体", 15), fg="red").pack(fill=BOTH, pady=10)
        F2 = Frame(master=self.master)
        Label(master=F2, text="Total:", ).grid(sticky='W', column=0, row=0, padx=0, pady=10)
        Label(master=F2, textvariable=self.Total, ).grid(column=1, row=0, padx=10, pady=10)
        Label(master=F2, text="Succesful:", fg="green").grid(sticky='W', column=0, row=1, padx=0, pady=10)
        Label(master=F2, textvariable=self.Succesful, fg="green").grid(column=1, row=1, padx=10, pady=10)
        Label(master=F2, text="Failure:", fg='red').grid(sticky='W', column=0, row=2, padx=0, pady=10)
        Label(master=F2, textvariable=self.Failure, fg='red').grid(column=1, row=2, padx=10, pady=10)
        self.T1 = Text(master=F2, height=9, width=40, state='normal', font=('黑体', 9))
        self.T1.grid(column=2, row=0, padx=10, pady=10, rowspan=3)
        F2.pack()
        F3 = Frame(master=self.master)
        Label(master=F3, text=r'文件上传地址为：\\10.102.170.16\Data', fg='DarkViolet').grid(column=0, row=0, padx=10, pady=0,
                                                                                     columnspan=4)
        self.B1 = Button(master=F3, text="自动上次", command=self.SendData)
        self.B1.grid(column=0, row=1, padx=10, pady=15, ipady=10)
        Button(master=F3, text="停止上传", command=self.StopUpload).grid(column=1, row=1, padx=15, pady=15, ipady=10)
        Button(master=F3, text="手动上传", command=self.SendDataOne).grid(column=2, row=1, padx=15, pady=15, ipady=10)
        Button(master=F3, text="清除计数", command=self.ClearDispaly).grid(column=3, row=1, padx=15, pady=15, ipady=10)

        F3.pack()

    def SendData(self):
        global Close
        Close = False
        self.B1.config(state='disabled')
        th1 = threading.Thread(target=self.SendData1)
        th1.start()
        self.T1.insert(END, "** {},已开启自动上传模式\n".format(str(time.strftime("%Y-%m-%d %H:%M", time.localtime()))))

    def SendDataOne(self):
        try:
            UploadingData()
        except:
            self.Total.set(value=self.Total.get() + 1)
            self.Failure.set(value=self.Failure.get() + 1)
            self.T1.insert(END, "** {},手动上传数据失败\n".format(str(time.strftime("%Y:%m:%d %H:%M", time.localtime()))))
        else:
            self.Total.set(value=self.Total.get() + 1)
            self.Succesful.set(value=self.Succesful.get() + 1)
            self.T1.insert(END, "** {},手动上传数据成功\n".format(str(time.strftime("%Y-%m-%d %H:%M", time.localtime()))))

    def SendData1(self):
        while True:
            if Close == True:
                break
            if str(time.strftime("%H:%M", time.localtime())) == "07:30":
                try:
                    UploadingData()
                except:
                    self.Total.set(value=self.Total.get() + 1)
                    self.Failure.set(value=self.Failure.get() + 1)
                    self.T1.insert(END,
                                   "** {},自动上传数据失败\n".format(str(time.strftime("%Y:%m:%d %H:%M", time.localtime()))))
                    time.sleep(20)
                    continue
                else:
                    self.Total.set(value=self.Total.get() + 1)
                    self.Succesful.set(value=self.Succesful.get() + 1)
                    self.T1.insert(END,
                                   "** {},自动上传数据成功\n".format(str(time.strftime("%Y-%m-%d %H:%M", time.localtime()))))
                    time.sleep(60)

    def ClearDispaly(self):
        self.T1.delete(0.0, END)
        self.Total.set(value=0)
        self.Failure.set(value=0)
        self.Succesful.set(value=0)
        self.T1.insert(END, "** {},清除计数成功\n".format(str(time.strftime("%Y-%m-%d %H:%M", time.localtime()))))

    def StopUpload(self):
        global Close
        Close = True
        self.B1.config(state='normal')
        self.T1.insert(END, '** {},已停止自动上传数据\n'.format(str(time.strftime("%Y-%m-%d %H:%M", time.localtime()))))


if __name__ == '__main__':
    def on_close():
        global Close
        Close = True
        windows.destroy()


    windows = Tk()
    windows.title("自动上传数据软件V1.1")
    windows.geometry("430x320")
    windows.protocol('WM_DELETE_WINDOW', on_close)
    windows.resizable(width=0, height=0)
    App = Applicaton(windows)
    windows.mainloop()
