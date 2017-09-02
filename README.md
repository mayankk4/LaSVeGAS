# LaSVeGAS
Design doc (Privately shared):
https://docs.google.com/document/d/1OQABNMRc1sKBlmDgNly1RI8DmX0vEqEmCt6j4h7nEA4/edit#heading=h.7dzhdyi98xul


## Mac Setup
Install brew  

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install python and pip (We use Python 2.7)  

    brew install python
    sudo easy_install pip

Create a virtual environment within lasvegas/ (and call it venv)
http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvironments-ref

Activate the virtual environment

    source venv/bin/activate

## Setup for development (Inside virtual environment)
Install lint  

    pip install pep8
    pip install autopep8

Please autolint the files before checking in.

    autopep8 ./src/ --recursive --in-place --pep8-passes 2000 --verbose

Do not check in the client_secrets

    git update-index --assume-unchanged path/to/client_secrets.json

## Running the pipeline

Setup for Image generator

    pip install pillow
    ~~pip install cv2~~
    pip install numpy  

Setup for Audio generator

    ~~pip install pyttsx~~
    ~~pip install pyobjc~~
    pip install gTTS

Setup for video muxing - For this, we need to install ffmpeg since we simply invoke it using a subprocess.  

    sudo brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-libass --with-libquvi --with-libvorbis --with-libvpx --with-opus --with-x265 --with-frei0r  --with-libvo-aacenc --with-opencore-amr --with-openjpeg --with-rtmpdump --with-schroedinger --with-speex --with-theora --with-tools --with-openssl --with-rtmpdump  --with-faac --with-lame --with-x264 --with-xvid

Other required libs

	pip install --upgrade oauth2client
	pip install --upgrade google-api-python-client

## Running the pipeline for a single KV pair.

    time sh lasvegas_debug.sh
