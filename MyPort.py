# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：H18-1 -> MyPort
@IDE    ：PyCharm
@Author ：Lyle.Hou
@Date   ：2020/8/13 10:04
@Desc   ：
=================================================='''

# -*- coding:utf-8 -*-
import serial
import time


class SerialPort():

    def __init__(self, PortName, BaudRate, TimeOut=6):
        try:
            self.port = serial.Serial(PortName, baudrate=BaudRate, timeout=TimeOut)
            self.port_name = self.port.port
        except:
            raise RuntimeError("Open serial port error: %s", PortName)

    def close(self):
        if self.port.isOpen():
            self.port.flush()
            self.port.close()

    def sendcmd(self, cmd):
        if self.port.is_open:
            self.port.flushInput()
            self.port.flushOutput()
            print(str(time.strftime("\n%Y-%m-%d %H:%M:%S", time.localtime())), '    ', cmd)
            self.port.write(cmd.encode('utf-8'))
        else:
            raise RuntimeError("Cmd send error, port not open: %s", self.port.name)

    def sendcmd_bybyte(self, cmd, interval=0.020):
        if self.port.is_open:
            self.port.flushInput()
            self.port.flushOutput()
            print(str(time.strftime("\n%Y-%m-%d %H:%M:%S", time.localtime())), '    ', cmd)
            for sc in cmd:
                self.port.write(sc.encode('utf-8'))
                time.sleep(interval)
            self.port.write("\n".encode('utf-8'))
        else:
            raise RuntimeError("Cmd send error, port not open: %s", self.port.name)

    def readResponse(self, terminator='> ', nextline_check=True):
        res = self.read_until(terminator, self.port.timeout, nextline_check)
        if terminator in res:
            return res
        else:
            # pass
            print("timeout")
            raise RuntimeError("Error: timeout %s", res)

    def send_read(self, cmd, terminator='> ', nextline_check=True):
        self.read_existing()
        self.sendcmd(cmd)
        return self.readResponse(terminator, nextline_check)

    def send_read_bybyte(self, cmd, interval=0.020, terminator='> ', nextline_check=True):
        if self.port.is_open:
            self.read_existing()
            self.port.flushInput()
            self.port.flushOutput()
            print(str(time.strftime("\n%Y-%m-%d %H:%M:%S", time.localtime())), '    ', cmd)

            for sc in cmd:
                self.port.write(sc.encode('utf-8'))
                time.sleep(interval)
            self.port.write("\n".encode('utf-8'))
        else:
            raise RuntimeError("Cmd send error, port not open: %s", self.port.name)
        return self.readResponse(terminator, nextline_check)

    def read_until(self, terminator, timeout, nextline_check=True):
        """\
        Read until a termination sequence is found ('\n' by default), the size
        is exceeded or until timeout occurs.
        """
        timeout_happen = False
        line = ""
        begin = time.time()
        while True:
            c = self.port.read_all().decode('utf-8')
            if c:
                line += c
                if line.rfind(terminator) > 0:
                    # print(line.rfind(terminator))
                    if nextline_check:
                        if line.split('\n')[
                            -1].strip() == ']':  # ensure after terminator: > is located at end of response, ]
                            break
                    else:
                        break
                time.sleep(0.005)
            if time.time() - begin > timeout:
                timeout_happen = True
                break
        print(str(time.strftime("\n%Y-%m-%d %H:%M:%S", time.localtime())), '    ', line)
        if timeout_happen:
            print("timeout /n")
            raise RuntimeError("Error: timeout %s", line)
        return line

    def read_existing(self):
        # res = self.port.read(self.port.in_waiting)
        res = self.port.read_all().decode('utf-8')
        # if res != "":
        print(str(time.strftime("\n%Y-%m-%d %H:%M:%S", time.localtime())), '    ', res)
        return res

    def setTimeout(self, timeOut=6):
        self.port.timeout = timeOut

    def write(self, cmd):
        self.port.write(cmd.encode('utf-8'))

    def flashout(self):
        self.port.flushInput()
        self.port.flushOutput()

    def write_read(self,cmd,timesleep):
        self.port.write(cmd.encode('utf-8'))
        time.sleep(timesleep)
        res = self.port.read_all().decode('utf-8')
        print(str(time.strftime("\n%Y-%m-%d %H:%M:%S", time.localtime())), '    ', res)
        return res