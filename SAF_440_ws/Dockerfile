FROM ros:humble

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-pandas \
    && rm -rf /var/lib/apt/lists/*

# Optional: install additional ROS packages if needed
RUN apt-get update && apt-get install -y \
    ros-humble-std-msgs \
    ros-humble-ament-index-python \
    && rm -rf /var/lib/apt/lists/*

# # Create workspace
# WORKDIR /ros2_ws

# # Copy your package into the container
# COPY . /ros2_ws

# # Source ROS automatically
# SHELL ["/bin/bash", "-c"]

# # Build workspace if this is a ROS2 package
# RUN source /opt/ros/humble/setup.bash && \
#     if [ -f "/ros2_ws/src/package.xml" ]; then \
#         colcon build; \
#     fi

# # Source workspace on container startup
# RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc && \
#     echo "if [ -f /ros2_ws/install/setup.bash ]; then source /ros2_ws/install/setup.bash; fi" >> ~/.bashrc

# # Default command
# CMD ["/bin/bash"]

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