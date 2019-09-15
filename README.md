# labelwriter

Module for interfacing with Labelwriter on TCP port 9100

TCP port 9100 accepts "RAW" protocol. In our case, the printer has been set up
to accept Fingerprint language on this port.

# Verified working with:
Tested on Intermec PC43D Icon with Ethernet module and Fingerprint on 9100

# Templates:
Now with template support. A label closely following Norsk Standard 9405:2014 is NS9405.fp.

# Fingerprint Code:
To learn more about Fingerprint code, read some manuals.
[Intermec Fingerprint Developer’s Guide](https://www.mediaform.de/fileadmin/support/handbuecher/etikettendrucker/intermec/Int_FP_PRM_8_70_10_0.pdf)
For fun and profit: You can "sniff" any labels printed through other programs on your Intermec PC43D, to reverse engineer the code used to make a given label.

# Example label:
![Example label](example.jpg?raw=true "Example label")