# labelwriter

Module for interfacing with Labelwriter on TCP port 9100

TCP port 9100 accepts "RAW" protocol. In our case, the printer has been set up
to accept Fingerprint language on this port.

Now with template support. A label closely following Norsk Standard 9405:2014 is NS9405.fp. Too sad nobody else seems to be using it in the EU - yet.

# Verified working with
Tested on Intermec PC43D Icon with Ethernet module and Fingerprint on 9100

# Fingerprint Code
To learn more about Fingerprint code, read some manuals.
[Intermec Fingerprint Developer’s Guide](https://www.mediaform.de/fileadmin/support/handbuecher/etikettendrucker/intermec/Int_FP_PRM_8_70_10_0.pdf)
For fun and profit: You can "sniff" any labels printed through other programs on your Intermec PC43D, to reverse engineer the code used to make a given label.

# Example label
![Example label](example.jpg?raw=true "Example label")

# Projects for later
* Make fully modular and simple labelwriter interface that anybody can use
* Make visual label developer, so that we can make labels using a visual interface, or code them and see the results in realtime
* Add some error-handling...