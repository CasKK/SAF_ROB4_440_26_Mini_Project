FROM ros:humble

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-pandas \
    && rm -rf /var/lib/apt/lists/*

# install additional ROS packages
RUN apt-get update && apt-get install -y \
    ros-humble-std-msgs \
    ros-humble-ament-index-python \
    && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1
ENV ROS_DOMAIN_ID=7

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc

WORKDIR /ros2_ws
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]