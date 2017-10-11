# PiGreeter
Short python project which should enable a raspberry Pi with a camera to recognize and greet people as they come into work in the morning.

## How to install OpenCV on a Raspberry Pi
Inspired by https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
### Step 1 - Install dependencies
#### Build essentials
OpenCV uses CMAKE to generates its makefiles.
```
sudo apt-get install build-essential cmake pkg-config
```
#### Image codecs
```
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
```
#### Video codecs
```
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
```
#### GTK
```
sudo apt-get install libgtk2.0-dev libgtk-3-dev
```
#### Other
These libs will optimise some of opencv operations.
```
sudo apt-get install libatlas-base-dev gfortran
```
#### Python headers
```
sudo apt-get install python2.7-dev python3-dev
```
### Step 2 - Download OpenCV
Move to the directory of your choice and download the source code of both OpenCV and OpenCV-contrib.
```
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
unzip opencv.zip
unzip opencv_contrib.zip
```

### Step 3 - Compiling
Switch to the virtual environment of your choice. Move to the directory of OpenCV your just created by unzipping
```
cd opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    -D BUILD_EXAMPLES=ON ..    
make
```
### Step 4 - Installation
Still in the same directory.
```
sudo make install
sudo ldconfig
```

You can verify your installation using the ls command
```
ls -l /usr/local/lib/python3.5/site-packages/
total 1852
-rw-r--r-- 1 root staff 1895932 Mar 20 21:51 cv2.cpython-34m.so
```
