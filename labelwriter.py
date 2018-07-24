#!/usr/bin/env python

# Module to interface a label writer that accepts Fingerprint on TCP port 9100
# 9100 also known as "RAW" print protocol
# Tested on OS X, Python 3.7, Intermec PC43D

import socket
import sys
import time
from datetime import datetime, date, time

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

    def print_label(self, data):
        print('weight', data['weight'])
        weightflat = str(data['weight']).replace(',','').replace('.','').zfill(6)
        print('weightflat', weightflat)

        data['productiondatetime'] = zuludatetimenow()
        data['proddate'] = zuluproddatenow()
        data['weightflat'] = weightflat
        print(data)

        labeltemplate = """
    INPUT OFF
    VERBOFF
    INPUT ON
    LAYOUT INPUT "tmp:LABEL1"
    PP104,41:AN7
    DIR4
    NASC 8
    FT "Univers",18,0,99
    PT "{friendlyname}"
    PP166,41:FT "Univers"
    FONTSIZE 10
    FONTSLANT 0
    PT "{scientificname}"
    PP74,41:PT "Produktnavn / Product name / {productinthirdlanguage}"
    PP237,1200:AN1
    DIR2
    PL1181,6
    PP200,41:AN7
    DIR4
    PT "Production method:"
    PP24,41:PT "GTIN: {gtin}"
    PP256,41:PT "Size:"
    PP348,214:PT "{processingmethod}"
    PP460,41:PT "Catch date:"
    PP501,41:PT "Prod date:"

    PP556,41:FONTSIZE 12
    PT "Net weight:"
    PP606,122:FONTSIZE 19
    PT "{weight} kg"
    PP680,41:FONTSIZE 19
    PT "{customer}"
    PP259,462:BARSET "CODE128C",2,1,4,112
    PB CHR$(128);"0{gtin}10{batchno}"
    PP369,571:FONTSIZE 11
    PT "(01) 0{gtin} (10) {batchno}"

    PP436,594:BARSET "CODE128C",2,1,4,112
    PB CHR$(128); "11{proddate}3102{weightflat}"
    PP546,700:PT "(11) {proddate} (3102) {weightflat}"

    PP612,550:BARSET "CODE128C",2,1,4,112
    PB CHR$(128);"00370333500011222549"
    PP723,667:PT "(00) 3 7033350 001122254 9"

    PP256,214:FONTSIZE 10
    PT "{grade}"
    PP348,41:PT "Treatment:"
    PP395,41:PT "Preservation:"
    PP395,214:PT "Alive"
    PP460,214:PT "{catchdate}"
    PP501,214:PT "{productiondatetime}"
    PP200,328:PT "Handpicked"
    PP200,578:PT "Origin:"
    PP200,712:PT "FAO 27 IIa, Norwegian Sea"
    PP166,578:PT "Batch no:"
    PP166,712:PT "{batchno}"
    PP25,578:PT "Exp.:"
    PP25,649:PT "Statsnail AS"
    PP60,649:PT "7165 Oksvoll, NORWAY"
    PP300,41:PT "pcs/kg:"
    PP300,214:PT "{pcskg}"

    PRPOS 0,985
    PRIMAGE "SNAIL150X125.PCX"

    PRPOS 125,990
    PRIMAGE "EFTA150X81.PCX"
    LAYOUT END
    VERBOFF
    """.format(**data)
        self.send_template(labeltemplate)
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

    data = {'friendlyname':'Common Periwinkle', 'scientificname':'LITTORINA LITTOREA',
    'productinthirdlanguage':'Produit', 'gtin':'7072773000030', 'processingmethod':'Climbed',
    'batchno':'000001', 'grade':'Super Jumbo', 'catchdate':'2018-05-10', 'weight':'5,01', 'pcskg':'100-141 #/kg', 'customer':'thalassa'}
    mylabelwriter.print_label(data)

if __name__ == '__main__':
    main()