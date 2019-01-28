#clone MaskedRCNN path
git clone https://github.com/matterport/Mask_RCNN.git

#Install Mask_RCNN
pip install -r requirements.txt
python setup.py install


#install pycocotools
pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI


