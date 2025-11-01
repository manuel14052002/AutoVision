FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    build-essential \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# ROS 2 Jazzy installation
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - && \
    echo "deb [arch=amd64,arm64,armhf] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2.list && \
    apt-get update && apt-get install -y ros-jazzy-desktop python3-rosdep && \
    rm -rf /var/lib/apt/lists/*

RUN rosdep init && rosdep update

RUN pip3 install --no-cache-dir numpy opencv-python open3d torch torchvision ultralytics

ENV ROS_DISTRO=jazzy
ENV ROS_ROOT=/opt/ros/jazzy
ENV ROS_PYTHON_VERSION=3

CMD ["bash"]
