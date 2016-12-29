# LaSVeGAS
Design doc (Privately shared):
https://docs.google.com/document/d/1OQABNMRc1sKBlmDgNly1RI8DmX0vEqEmCt6j4h7nEA4/edit#heading=h.7dzhdyi98xul


## Mac Setup
Install brew  

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install python and pip (We use Python 2.7)  

    brew install python
    sudo easy_install pip

Create a virtual environment within lasvegas/  
http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvironments-ref

Install lint  

    source venv/bin/activate
    pip install pep8
    pip install autopep8

## Setup for video generator
install pil  

    sudo pip install pillow

install cv2, numpy  

## Setup for Audio generator

    pip install pyttsx
    pip install pyobjc
    pip install gTTS

# Setup for Uploader

    git update-index --assume-unchanged path/to/client_secrets.json

# Setup for video muxing
For this, we need to install ffmpeg since we simply invoke it using a subprocess.  

    brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-libass --with-libquvi --with-libvorbis --with-libvpx --with-opus --with-x265 --with-frei0r  --with-libvo-aacenc --with-opencore-amr --with-openjpeg --with-rtmpdump --with-schroedinger --with-speex --with-theora --with-tools --with-openssl --with-rtmpdump  --with-faac --with-lame --with-x264 --with-xvid

## Submitting  
Please autolint the files before checking in.

    autopep8 ./src/ --recursive --in-place --pep8-passes 2000 --verbose


## Running the pipeline for a single KV pair.
This assumes that test-data/ is correctly setup.  

    time sh lasvegas_tool.sh
