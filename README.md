# LaSVeGAS

Design doc (Privately shared):
https://docs.google.com/document/d/1OQABNMRc1sKBlmDgNly1RI8DmX0vEqEmCt6j4h7nEA4/edit#heading=h.7dzhdyi98xul


===================================================
## Mac Setup
===================================================
Install brew  
    
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install python and pip  

    brew install python
    sudo easy_install pip

Create a virtual environment within lasvegas/  
http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvironments-ref


===================================================
## Setup for video generator
===================================================

install pil  

    sudo pip install pillow

install cv2, numpy  



===================================================
## Running the pipeline for a single KV pair.
===================================================
This assumes that test-data/ is correctly setup.  

    time sh lasvegas_tool.sh 
