FROM ubuntu:24.04

RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y tzdata
RUN apt update && \
    apt install -y git python3 python3-pip cmake

# Install Cyclone DDS from source
WORKDIR /opt
RUN git clone --depth 1 --branch 0.10.5 https://github.com/eclipse-cyclonedds/cyclonedds
RUN cd cyclonedds && \
    mkdir build && mkdir install && \
    cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=../install && \
    cmake --build . --target install

# Install Cyclone DDS Python
ENV CYCLONEDDS_HOME=/opt/cyclonedds/install
RUN python3 -m pip install cyclonedds==0.10.5 --break-system-packages

# Clone fork with modified Vehicle example to reproduce the issue
WORKDIR /opt
RUN git clone --depth 1 --branch danielflexion/0.10.5/issue_mixing_published_topics https://github.com/danielflexion/cyclonedds-python
WORKDIR /opt/cyclonedds-python/examples/vehicle
ENTRYPOINT ["python3", "main.py"]


