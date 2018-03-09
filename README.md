# LaSVeGAS
[Design doc](https://docs.google.com/document/d/1OQABNMRc1sKBlmDgNly1RI8DmX0vEqEmCt6j4h7nEA4/edit#heading=h.7dzhdyi98xul) (Privately shared)

## Setup for Running the pipeline
Install python and pip (We use Python 2.7)  

### Setup for Image generator

    pip install pillow
    pip install numpy  

### Setup for Audio generator

    pip install gTTS

### Setup for video muxing
For this, we need to install ffmpeg and melt since we simply invoke it using a subprocess. ffmpeg is used to attach audio to the images while melt is used to concat the videos.

    sudo apt-get install ffmpeg
    sudo apt-get install melt

### Setup for Uploading to youtube

    pip install --upgrade oauth2client
    pip install --upgrade google-api-python-client


## Running the pipeline for a single KV pair

    time sh lasvegas_debug.sh


## Additional Setup for programming

Install lint  

    pip install pep8
    pip install autopep8

Please autolint the files before checking in.

    autopep8 ./src/ --recursive --in-place --pep8-passes 2000 --verbose

Do not check in the client_secrets

    git update-index --assume-unchanged path/to/client_secrets.json
