# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：PYQT -> demo2
@IDE    ：PyCharm
@Author ：Lyle.Hou
@Date   ：2020/6/20 17:07
@Desc   ：
=================================================='''
import os.path
import time
from tkinter import *
import threading
import tkinter.messagebox as mb
from tkinter import ttk
import serial
import serial.tools.list_ports
import re

spec_up = 0.575
spec_lo = 0.510
link_times = 3
path = os.path.join(os.path.expanduser("~"), 'Desktop')+'\\test_log'
# path = os.path.join(os.path.expanduser('~'),'Desktop') + '/test_log'


if os.path.exists(path):
    pass
else:
    os.mkdir(path)

def mic_test(result):
    if len(result) != 64:
        return False
    i = 4
    m = 8
    value = 0
    for a in range(15):
        ok1 = result[i - 4:i]
        ok2 = result[i:i + 4]
        if ok1 == ok2:
            value += 1
        else:
            value += 0
        i += 4
    for a in range(7):
        ok1 = result[m - 8:m]
        ok2 = result[m:m + 8]
        if ok1 == ok2:
            value += 1
        else:
            value += 0
        m += 8
    if value >= 11:
        final = False
    else:
        final = True
    return final

def data_dispose(value):
    result = True
    for item in value:
        con_loc1 = item.find('concha')
        con_loc2 = item.find('tragus')
        concha_con = float(item[con_loc1 + 9:con_loc2 - 3])
        tragus_con = float(item[con_loc2 + 9:con_loc2 + 14])
        # print concha_con
        # print tragus_con
        if spec_lo > concha_con or concha_con > spec_up or spec_lo > tragus_con or tragus_con > spec_up:
            result = False
    return result

def write_log(file_name,text,results):
    path1 = os.path.join(os.path.expanduser("~"), 'Desktop') + '\\test_log\\{}'. \
        format(str(time.strftime("%Y-%m-%d", time.localtime())))
    if os.path.exists(path1):
        pass
    else:
        os.mkdir(path1)
    file_path = path1+'\\{}.txt'.format(file_name)
    file_path1 = path1+'\\{}-Result.csv'.format(str(time.strftime("%Y-%m-%d", time.localtime())))
    if os.path.isfile(file_path1):
        pass
    else:
        with open(file_path1,'w') as f:
            f.write('Test Time,SN,Link Check,Read SN,Close 5V Check,Open Tunnel,MIC3 Test,Optical Sensor Test,Gcal Test,'
                    'Close Tunnel,Result\n')
    # print file_path
    with open(file_path,'w') as f:
        f.write(text)
    with open(file_path1,'a') as f1:
        f1.write('{},'.format(str(time.strftime("%H:%M:%S",time.localtime()))))
        for result in results:
            f1.write(result+',')
        f1.write('\n')

def gg():
    tt  = int(time.strftime("%Y",time.localtime()))
    tt1  = int(time.strftime("%m",time.localtime()))
    if tt > 2020 or tt1 > 10:
        return False
    return True

class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master = master
        self.port_name = StringVar(self.master)
        self.auto_choose_port()
        if gg() == False:
            if os.path.isfile('gg.gg'):
                pass
            else:
                self.UI()
                return
        self.spec_up = IntVar(self.master)
        self.spec_up.set(value=spec_up)
        self.spec_lo = IntVar(self.master)
        self.spec_lo.set(value=spec_lo)
        self.link_times = IntVar(self.master)
        self.link_times.set(value=3)
        self.result = StringVar(self.master)
        self.widgets()

    def widgets(self):
        F1 = Frame(self.master,heigh =50,)
        F2 = Frame(self.master,heigh =150,)
        l1 = Label(F1,textvariable= self.port_name,heigh = 1,font = ('等线',9),fg = 'red').pack(pady = 5,side = 'left')
        self.show_SN = Text(F2,heigh = 1,width = 14 ,bg = 'GhostWhite',font = ('等线',21),pady = 5,relief = 'groove')
        bu2 = Button(F2 ,width = 8 , text = 'Settig',relief = 'groove',command = self.set_up ).pack(side = 'left',padx= 20,)#flat, groove, raised, ridge, solid, or sunken
        self.show_SN.pack(side = 'left',padx = 120)
        F1.pack(fill=BOTH)
        F2.pack(fill=BOTH)
        self.test_widget()
        F2 = Frame(self.master, heigh=100,)
        self.result_lab = Label(F2,textvariable=self.result,width =34,heigh =2,font = ('等线',21),bg ='green')
        self.result_lab.pack(side = 'top',pady = 5)
        self.go_but = Button(F2,text = 'Start',width = 15,heigh = 2,command = self.begin)
        self.go_but.pack(side = 'bottom',pady = 5)
        F2.pack(fill=BOTH)
        F3 = Frame(self.master,height = 60,)
        self.showlog_widght(F3)
        F3.pack(fill = BOTH)

    def set_up(self):
        self.F5 = Frame(master=self.master, heigh=120, width=350, borderwidth=3, relief='groove')
        lb = Label(self.F5 ,text = 'Password:')
        lb .place(x= 20, y = 20)
        self.en1 = Entry(self.F5,show = '*',state= 'normal')
        self.en1.place(x = 120,y = 20,)
        b1 = Button(master=self.F5, text='确认', width=10,command = self.set_up2 ).place(x=50, y=60)
        b2 = Button(master=self.F5, text='取消', width=10, command=lambda: self.F5.destroy()).place(x=200, y=60)
        self.F5.place(x=200, y=00,)

    def set_up2(self):
        if self.en1.get() == 'luxshare':
            self.F5.destroy()
            F6 = Frame(master=self.master, heigh=220, width=400, borderwidth=3, relief='groove')
            b1 = Button(master=F6, text='确认', width=10,command = lambda : self.port_choose(F6) ).place(x=80, y=175)
            l1 = Label(F6,text = 'Check Link times:').place(x= 10,y=145)
            l2 = Label(F6,text = 'Sensor Lower:').place(x= 10,y=110)
            l3 = Label(F6,text = 'Sensor Upper:').place(x= 200,y=110)
            en1 = Entry(F6,width = 8,textvariable = self.spec_lo )
            en2 = Entry(F6,width = 8,textvariable = self.spec_up)
            en3 = Entry(F6,width = 8,textvariable = self.link_times)
            en3.place(x= 150,y = 145)
            en1.place(x= 110,y = 110)
            en2.place(x= 300,y = 110)
            b2 = Button(master=F6, text='取消', width=10, command=lambda: F6.destroy()).place(x=220, y=175)
            self.lb11 = Listbox(master=F6, heigh=4, width=35, selectmode='BROWSE')
            self.auto_choose_port()
            for i in self.ports:
                self.lb11.insert(END,i)
            self.lb11.place(x=50,y=10)
            F6.place(x=160, y=00, )
        else:
            m1 = mb.Message(self.master,message = 'Wrong Passwod ').show()

    def test_widget(self):
        columns = ('NO','Item','Lower','Upper','Result')
        self.sheet1 = ttk.Treeview(self.master,height = 9 ,show = 'headings',columns = columns,)
        for i in columns:
            if i  == 'NO':
                self.sheet1.column(i,width = 70,anchor = 'center')
                self.sheet1.heading(i,text = str(i))
            else:
                self.sheet1.column(i, width=150, anchor='center')
                self.sheet1.heading(i, text=str(i))
        self.sheet1.insert('',index=0,value = ('1','Link Check','NA','NA',))
        self.sheet1.insert('',index=1,value = ('2','Read SN','NA','NA',))
        self.sheet1.insert('',index=2,value = ('3','Close 5V Check','NA','NA',))
        # self.sheet1.insert('',index=3,value = ('4','MIC1 Test','NA','NA',))
        # self.sheet1.insert('',index=4,value = ('5','MIC2 Test','NA','NA',))
        self.sheet1.insert('',index=5,value = ('4','Open Tunnel','NA','NA',))
        self.sheet1.insert('',index=6,value = ('5','MIC3 Test','NA','NA',))
        self.sheet1.insert('',index=7,value = ('6','Optical Sensor Test',spec_lo,spec_up,))
        self.sheet1.insert('',index=8,value = ('7','Gcal Test','8575','8900',))
        self.sheet1.insert('',index=9,value = ('8','Close Tunnel','NA','NA',))
        self.sheet1.pack(fill=BOTH,pady = 5 )

    def auto_choose_port(self):
        ports = list(serial.tools.list_ports.comports())
        for item in ports[::-1]:
            if '/dev/cu.Bluetoot' in str(item):
                ports.remove(item)
            elif '端口' in str(item):
                ports.remove(item)
            elif 'COM' not in str(item):
                ports.remove(item)
        self.ports = ports
        # print(self.ports)

        if len(self.ports) == 0:
            self.term = None
            self.port_name.set(value = 'Serial Port is:None')
        else:
            try:
                port = str(self.ports[0])
                i = port.find('-')
                port1 = port[:i - 1]
                # print(port1)
                self.term = serial.Serial(port=port1,baudrate=921600,timeout=0.55)
                self.port_name.set(value='Serial Port is: {}'.format(self.term.port))
            except Exception:
                # print 'ioo'
                self.term = None
                self.port_name.set(value='Serial Port is:None')

    def UI(self):
        aa = 'Your usage time has expired, please contact the development team for the activation code!'
        L1 = Label(self.master,text = aa,fg = 'red').pack(pady = 15)
        L1 = Label(self.master,text = 'Please enter the activation code!').pack(pady = 10)
        self.e1 = Entry(self.master,show='*')
        self.e1.pack(pady = 10)
        self.bb1 = Button(self.master,text = '确认',command = self.sure)
        self.bb1.pack(pady = 5)

    def sure(self):
        if self.e1.get() == '343600':
            with open('gg.gg','w') as f:
                pass
        self.master.quit()

    def showlog_widght(self, master):
        L3 = Label(master, text='Luxshare-ICT', bg='#6A5ACD', fg='white', anchor='e', font=('黑体', 16))
        L3.place(x=0, y=0, relx=0.70, rely=1, relheight=1, relwidth=0.3, anchor='sw', bordermode='inside')
        L4 = Label(master, text='Author:电子开发应用二课，Lyle.Hou      version:2.1  ', bg='#6A5ACD', fg='white',
                   anchor='w', font=('黑体', 11))
        L4.place(x=0, y=0, relx=0.0, rely=1, relheight=1, relwidth=0.7, anchor='sw', bordermode='inside')

    def port_choose(self, master):
        global link_times,spec_lo,spec_up
        if self.lb11.get(0) == '':
            pass
        else:
            port = self.lb11.get('active')
            i = port.find('-')
            port1 = port[:i - 1]
            # print(port)
            # print(self.term.port)
            if self.term == None:
                self.term = serial.Serial(port=port,baudrate=921600,timeout=0.5)
                self.port_name.set(value='Serial Port is: {}'.format(self.term.port))
            else:
                if port == self.term.port:
                    # print(self.term)
                    # print('一样')
                    pass
                else:
                    # close_port(self.term)
                    self.term.close()
                    self.term = serial.Serial(port,baudrate=921600,timeout=0.5)
                    self.port_name.set(value='Serial Port is: {}'.format(self.term.port))
        spec_lo = self.spec_lo.get()
        spec_up = self.spec_up.get()
        link_times = self.link_times.get()
        # self.sheet1.set('', item='I007',column=6, value=('7', 'Optical Sensor Test', spec_lo, spec_up,))
        self.sheet1.set(item='I007',column=3,value=spec_up)
        self.sheet1.set(item='I007',column=2,value=spec_lo)
        master.destroy()

    def begin(self):
        if gg() == False:
            if os.path.isfile('gg.gg'):
                pass
            else:
                self.master.quit()
                return
        th1 = threading.Thread(target=self.begin1,)
        th1.start()

    def begin1(self):
        self.show_SN.delete(0.0,'end')
        self.result_lab.config(bg = 'yellow')
        self.result.set(value='TESTING')
        self.go_but.config(state = 'disabled')
        for i in self.sheet1.get_children():
            self.sheet1.set(item=i, column=4, value='')
        if self.term != None:
            try:
                text = ''
                results = []
                self.term.flushOutput()
                self.term.flushInput()
                # self.term.write('[bhr]\n'.encode('utf-8'))
                # time.sleep(0.2)
                for i in range(link_times+3):
                    self.term.write('[bls]'.encode('utf-8'))
                    time.sleep(0.01)
                    # self.term.write('[bls]'.encode('utf-8'))
                    # time.sleep(0.05)
                    value1 = self.term.read(100).decode('utf-8')
                    text+=value1
                    self.term.flushInput()
                    self.term.flushOutput()
                    print (value1)
                    if '<bls-1-0>' in value1:
                        self.sheet1.set(item='I001',column=4,value='PASS')
                        side = 'L'
                        results.append('PASS')
                        break
                    elif '<bls-0-1>' in value1:
                        self.sheet1.set(item='I001', column=4, value='PASS')
                        side = 'R'
                        results.append('PASS')
                        break
                    else:
                        if i == link_times+3-1:
                            self.sheet1.set(item='I001', column=4, value='FAIL')
                            results.append('FAIL')
                            self.result.set(value='FAIL')
                            self.result_lab.config(bg = 'red')
                            self.go_but.config(state= 'normal')
                            results.insert(0, 'None')
                            write_log('None',text,results)
                            return
                self.term.write('[dut-{}-bfsn]'.format(side).encode('utf-8'))
                time.sleep(0.05)
                self.term.write('[bout-0]'.encode('utf-8'))
                time.sleep(0.5)
                self.term.write('[ttim-01]'.encode('utf-8'))
                time.sleep(0.05)
                self.term.write('[len-b-1]'.encode('utf-8'))
                time.sleep(0.05)
                self.term.write('[tunnel-{}-0]'.format(side).encode('utf-8'))
                time.sleep(0.2)
                value2 = self.term.read(2100).decode('utf-8')
                text += value2
                self.term.flushInput()
                self.term.flushOutput()
                print(value2)
                SN_loc = re.compile(r'<dut-(.*?)>',re.S)
                SN = re.search(SN_loc,value2).group()
                if len(SN) == 29:
                    self.show_SN.insert('0.0',SN[-13:-1])
                    self.sheet1.set(item='I002', column=4, value='PASS')
                    results.append('PASS')
                else:
                    self.show_SN.insert('0.0', 'None')
                    self.sheet1.set(item='I002', column=4, value='FAIL')
                    results.append('FAIL')
                    self.result.set(value='FAIL')
                    self.result_lab.config(bg='red')
                    self.go_but.config(state='normal')
                    self.term.write('ft tunnel close'.encode('utf-8'))
                    time.sleep(0.5)
                    self.term.write('[sr]'.encode('utf-8'))
                    time.sleep(0.5)
                    results.insert(0, 'None')
                    write_log('None',text,results)
                    return
                if 'TUNNEL: OPEN' in value2:
                    self.sheet1.set(item='I003',column=4,value='PASS')
                    self.sheet1.set(item='I004',column=4,value='PASS')
                    results.append('PASS')
                    results.append('PASS')
                else:
                    self.term.write('[sr]'.format(side).encode('utf-8'))
                    time.sleep(0.1)
                    self.sheet1.set(item='I003',column=4,value='FAIL')
                    self.sheet1.set(item='I004',column=4,value='FAIL')
                    results.append('FAIL')
                    results.append('FAIL')
                    self.result.set(value='FAIL')
                    self.result_lab.config(bg='red')
                    self.go_but.config(state='normal')
                    results.insert(0, SN[-13:-1])
                    write_log(SN[-13:-1],text,results)
                    return
                self.term.write('audio init\n'.encode('utf-8'))
                time.sleep(0.1)
                self.term.write('audio record 48000 50 1 mic3\n'.encode('utf-8'))
                time.sleep(0.3)
                self.term.write('audio stop\n'.encode('utf-8'))
                time.sleep(0.1)
                self.term.write('audio dump\n'.encode('utf-8'))
                time.sleep(0.1)
                self.term.write('ft upload 0 2\n'.encode('utf-8'))
                time.sleep(0.1)
                self.term.write('0020\n'.encode('utf-8'))
                time.sleep(0.1)
                self.term.write('syscfg add Gcal 2\n'.encode('utf-8'))
                time.sleep(0.1)
                self.term.write('ft reset\n'.encode('utf-8'))
                time.sleep(0.8)
                self.term.write('[sr]\n'.encode('utf-8'))
                time.sleep(0.3)
                value6 = self.term.read(5000).decode('utf-8')
                text+=value6
                self.term.flushInput()
                self.term.flushOutput()
                print (value6)
                linkside3 = value6.find('> audio:ok begin')
                # linkside2 = value4.find('> audio:ok done')
                link3 = value6[linkside3 + 18:linkside3 + 18 + 64]
                mic3_result = mic_test(link3)
                if mic3_result:
                    self.sheet1.set(item='I005', column=4, value='PASS')
                    results.append('PASS')
                else:
                    self.term.write('ft tunnel close'.format(side).encode('utf-8'))
                    time.sleep(0.5)
                    self.term.write('[sr]'.format(side).encode('utf-8'))
                    time.sleep(0.1)
                    self.sheet1.set(item='I005', column=4, value='FAIL')
                    results.append('FAIL')
                    self.result.set(value='FAIL')
                    self.result_lab.config(bg='red')
                    self.go_but.config(state='normal')
                    results.insert(0, SN[-13:-1])
                    write_log(SN[-13:-1],text,results)
                    return
                self.term.write('[tunnel-{}-0]\n'.format(side).encode('utf-8'))
                time.sleep(0.2)
                self.term.write('rep "beryl pdtemp" 2 500\n'.encode('utf-8'))
                time.sleep(1)
                value7 = self.term.read(5000).decode('utf-8')
                self.term.flushInput()
                self.term.flushOutput()
                data_loc = re.compile(r'> beryl:ok(.*?)\n', re.S)
                print (value7)
                value = re.findall(data_loc, value7)
                print (value)
                data = data_dispose(value)
                text+=value7
                if data:
                    self.sheet1.set(item='I006', column=4, value='PASS')
                    results.append('PASS')
                else:
                    self.sheet1.set(item='I006', column=4, value='FAIL')
                    results.append('FAIL')
                    self.result.set(value='FAIL')
                    self.result_lab.config(bg='red')
                    self.go_but.config(state='normal')
                    self.term.write('ft tunnel close'.format(side).encode('utf-8'))
                    time.sleep(0.5)
                    self.term.write('[sr]'.format(side).encode('utf-8'))
                    time.sleep(0.1)
                    results.insert(0, SN[-13:-1])
                    write_log(SN[-13:-1],text,results)
                    return
                self.term.write('audio init\n'.encode('utf-8'))
                time.sleep(0.1)
                self.term.write('audio hp_cal\n'.encode('utf-8'))
                time.sleep(0.3)
                self.term.write('audio stop\n'.encode('utf-8'))
                time.sleep(0.1)
                value8 = self.term.read(5000).decode('utf-8')
                text+=value8
                self.term.flushInput()
                self.term.flushOutput()
                print (value8)
                side8 = value8.find('audio hp_cal')
                try:
                    Gcal =  int(value8[side8+19:side8+23])
                except Exception:
                    self.sheet1.set(item='I007', column=4, value='FAIL')
                    results.append('FAIL')
                    self.result.set(value='FAIL')
                    self.result_lab.config(bg='red')
                    self.go_but.config(state='normal')
                    self.term.write('ft tunnel close'.format(side).encode('utf-8'))
                    time.sleep(0.5)
                    self.term.write('[sr]'.format(side).encode('utf-8'))
                    time.sleep(0.1)
                    results.insert(0, SN[-13:-1])
                    write_log(SN[-13:-1],text,results)
                    return
                else:
                    if 8575 < Gcal <8900:
                        self.sheet1.set(item='I007', column=4, value='PASS')
                        results.append('PASS')
                    else:
                        self.sheet1.set(item='I007', column=4, value='FAIL')
                        results.append('FAIL')
                        self.result.set(value='FAIL')
                        self.result_lab.config(bg='red')
                        self.go_but.config(state='normal')
                        self.term.write('ft tunnel close'.format(side).encode('utf-8'))
                        time.sleep(0.5)
                        self.term.write('[sr]'.format(side).encode('utf-8'))
                        time.sleep(0.1)
                        results.insert(0, SN[-13:-1])
                        write_log(SN[-13:-1],text,results)
                        return
                self.term.write('ft tunnel close\n'.encode('utf-8'))
                time.sleep(0.1)
                value9 = self.term.read(500).decode('utf-8')
                print (value9)
                text+=value9
                self.term.flushInput()
                self.term.flushOutput()
                if 'ft tunnel close' in value9:
                    self.sheet1.set(item = 'I008',column= 4,value = 'PASS')
                    results.append('PASS')
                else:
                    self.sheet1.set(item='I008', column=4, value='FAIL')
                    results.append('FAIL')
                    self.result.set(value='FAIL')
                    self.result_lab.config(bg='red')
                    self.go_but.config(state='normal')
                    results.insert(0, SN[-13:-1])
                    write_log(SN,text,results)
                    return
                results.insert(0,SN[-13:-1])
                results.append('PASS')
                print(results)
                self.result.set(value='PASS')
                self.result_lab.config(bg = 'green')
                self.go_but.config(state='normal')
                write_log(SN[-13:-1], text, results)
            except Exception:
                self.result.set(value='FAIL')
                self.result_lab.config(bg='red')
                self.go_but.config(state='normal')
        else:
            time.sleep(0.5)
            self.result.set(value='Serial Port Disconnected')
            self.result_lab.config(bg = 'red')
            self.go_but.config(state='normal')



if __name__ == '__main__':
    window = Tk()
    window.title('Golden Finger Test2')
    window.geometry('660x500')
    window.resizable(width= 0,height=0)
    app = Application(master=window)
    window.mainloop()
