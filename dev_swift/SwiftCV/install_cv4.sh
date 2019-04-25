OPENCV_VERSION='4.1.0'

sudo apt-fast -y update
sudo apt-fast install -y build-essential cmake zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libopenexr-dev libgdal-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev libtbb-dev libeigen3-dev python-dev python-tk python-numpy python3-dev python3-tk python3-numpy unzip wget libopenblas-dev libopenblas-base liblapacke-dev libatlas-base-dev liblapack-dev libblas-dev
sudo ln -s /usr/include/lapacke.h /usr/include/x86_64-linux-gnu # corrected path for the library

mkdir -p ~/download
pushd ~/download

wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip
unzip -q ${OPENCV_VERSION}.zip
rm ${OPENCV_VERSION}.zip
mv opencv-${OPENCV_VERSION} OpenCV
cd OpenCV
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=Release -D OPENCV_GENERATE_PKGCONFIG=YES -D WITH_QT=OFF -D WITH_OPENGL=ON -D FORCE_VTK=ON -D WITH_TBB=ON -D WITH_GDAL=ON -D WITH_XINE=ON -D ENABLE_PRECOMPILED_HEADERS=OFF ..
make -j4
sudo make install
sudo ldconfig
popd

