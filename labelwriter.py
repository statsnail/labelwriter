#!/usr/bin/env python

# Module to interface a label writer that accepts Fingerprint on TCP port 9100
# 9100 also known as "RAW" print protocol
# Tested on OS X, Python 3.7, Intermec PC43D

# Template system uses ~{ } delimiter
# NS9405:2014 Standard is provided as Fingerprint code in NS9405.fp
# Other templates can be added later

# PCX images must be uploaded to printer prior to usage in templates

import socket
import sys
import time
from datetime import datetime, date, time

import os
from string import Template
from pathlib import Path
import re



BASE_DIR = Path(__file__).resolve().parent
GLOBAL_TEMPLATES_DIR = BASE_DIR.joinpath('templates')

crlf = "\r\n"
msg_ok = "\r\nOk\r\n"

def bencmsg(msg):
    message = msg+crlf
    return message.encode()

def zuludatetimenow():
    t = datetime.utcnow()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return s[0:-7]+'Z'

def zuluproddatenow():
    t = datetime.utcnow()
    s = t.strftime('%y%m%d')
    return s

def weightflat(weight):
    weightflat = str(weight).replace(',','').replace('.','').zfill(6)
    return weightflat


class TemplateClone(Template):
    delimiter = '~'
    pattern = r'''
    \~(?:
      (?P<escaped>\~) |   # Escape sequence of two delimiters
      \b\B(?P<named>)      |   # disable named
      {(?P<braced>[_a-z][_a-z0-9]*)}   |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
    '''

class TemplatesMixin:
    TEMPLATES_DIR = GLOBAL_TEMPLATES_DIR

    def _read_template(self, template_path):
        with open(os.path.join(self.TEMPLATES_DIR, template_path)) as template:
            return template.read()

    def render(self, template_path, **kwargs):
        return TemplateClone(
            self._read_template(template_path)
        ).substitute(**kwargs)

class LabelGenerator(TemplatesMixin):
    def generate(self, **kwargs):
        print('Label class ')
        labelbody = self.render('NS9405.fp', **kwargs)
        return labelbody

class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        MSGLEN = len(msg)
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        MSGLEN = 100 # Arbitrary max message length
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            print("bytes recvd:", len(chunk), chunk)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            if chunk == msg_ok.encode():
                print("Got OK, returning full message")
                return b''.join(chunks)
        return b''.join(chunks)


class Labelwriter:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._socket = MySocket()
        self._connected = False




        while not self._connected:
            try:
                self._socket.connect(self._ip, self._port)
                self._connected = True
                print("connected labelwriter successfully")
            except ConnectionRefusedError:
                print("unable to connect labelwriter, retrying does not work. fail, restart program")
                time.sleep(1)
                raise

    def print_label(self, **kwarg):
        kwarg_addons = {
            'proddate':zuluproddatenow(), # Generated
            'productiondatetime':zuludatetimenow(), # Generated
            'weightflat':weightflat(kwarg['weight']) # Generated
        }

        label_data = {**kwarg, **kwarg_addons}

        generator = LabelGenerator()
        labelbody = generator.generate(**label_data)

        #print('printing')
        #print(labelbody)
        self.send_template(labelbody)
        self.print_template()

    def send_single_command(self, command):
        print('cmd: '+command)
        self._socket.mysend(bencmsg(command))

    def beep(self):
        self.send_single_command("SOUND 850,10 : SOUND 950,10 ")

    def formfeed(self):
        self.send_single_command("FORMFEED")

    def send_template(self, template):
        self.send_single_command(template)

    def print_template(self):
        command = """
        LAYOUT RUN "tmp:LABEL1"
        PF
        PRINT KEY OFF
        KILL "tmp:LABEL1"
        LAYOUT RUN ""
        """
        self.send_single_command(command)

    def kill_template(self, labelid = "LABEL1"):
        print("killing template " +labelid)
        self.send_single_command("KILL \"tmp:"+labelid+"\"")

# Create and store the layout in tmp memory
def msgSetupLabelTemplate():
    retval = """
    INPUT ON
    LAYOUT INPUT "tmp:LABEL1"
    PP 100,250
    FT "Univers",9
    PT "My first label"
    PP 200,250
    FT "Univers",12
    PT VAR1$
    PP 300,250
    FT "Univers",18
    PT VAR2$
    LAYOUT END
    INPUT OFF
    """
    return retval

# Run the layout from tmp memory
def msgRunLabelTemplate(arg1, arg2):
    retval = """
    INPUT OFF
    FORMAT INPUT "#","@","&"
    INPUT ON
    LAYOUT RUN "tmp:LABEL1"
    #{0}&{1}&@
    PF
    LAYOUT RUN ""
    INPUT OFF
    """.format(arg1,arg2)
    return retval

def main():
    print("running labelwriter module standalone")
    mylabelwriter = Labelwriter('192.168.1.3', 9100)
    mylabelwriter.beep()

    kwarg_partial = {
        'friendlyname':'Common Periwinkle',
        'scientificname':'LITTORINA LITTOREA',
        'productinthirdlanguage':'Produit',
        'gtin':'7072773000092',
        'processingmethod':'N/A',
        'weight':'5,00',
        'grade':'N/A',
        'customer':'Acustomer',
        'batchno':'000001',
        'catchdate':'2019-09-17',
        'pcskg':'100-140 #/kg'
    }

    # Uncomment to print an actual label
    # mylabelwriter.print_label(**kwarg_partial)


if __name__ == '__main__':
    main()