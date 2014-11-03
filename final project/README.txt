
These are all my files for my final project for Comp 116 - Computer Security at Tufts University. They include:

1) Victor Ansart Comp116 Final Paper.pdf	---a PDF containing my final paper on the compromising emissions emanating from electronics

2) Victor Ansart FM receiver.grc		---a GNU Radio Companion file that contains the blocks making up the FM receiver. This file can be run from GNU Radio Companion or compiled into a python script.

3) FM receiver block diagram.png		---a picture of the block diagram of the FM receiver that is in the above .grc file

4) Victor_FM_Receiver.py			---a python script compile from the .grc file that runs the FM receiver

5) FM receiver screenshot.png		---a screenshot of the FM receiver running using an RTL-SDR

6) Victor Ansart AM receiver.grc		---a GNU Radio Companion file that contains the blocks making up the AM receiver. This file can be run from GNU Radio Companion or compiled into a python script.

7) AM receiver block diagram.png		---a picture of the block diagram of the AM receiver that is in the above .grc file

8) Victor_AM_Receiver.py			---a python script compile from the .grc file that runs the AM receiver

9) AM receiver screenshot.png		---a screenshot of the AM receiver running using an RTL-SDR


NOTE: The RTL-SDR libraries were very difficult to compile in Ubuntu, so I did all my work in Kali Linux which had all the tools needed for RTL-SDR's pre-installed! The .grc should open up using GNU Radio Companion in Kali and python scripts should work as well as long as they are opened up in Kali. A software defined radio (specifically an RTL-SDR) should be plugged in prior to running the code in order to receive a signal. Otherwise, the receivers will open up, but only noise will be displayed. 



written by Victor Ansart 2013

