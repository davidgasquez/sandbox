#!/bin/env bash

git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
cd stable-diffusion-webui || exit
python3 -m venv venv
source venv/bin/activate

pip3 install --upgrade pip wheel
pip3 install --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/rocm5.6

pip3 install -r requirements.txt

python3 launch.py # --precision full --no-half
