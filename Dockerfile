FROM nvcr.io/nvidia/tritonserver:24.01-py3

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y build-essential cmake
# RUN apt-get install -y python3.10 python3.10-dev python3.10-venv
COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY TensorRT-8.6.1.6 /TensorRT-8.6.1.6
WORKDIR /TensorRT-8.6.1.6/python
RUN python3 -m pip install tensorrt-8.6.1-cp310-none-linux_x86_64.whl
RUN python3 -m pip install opencv-python 
RUN apt install -y libgl1
RUN pip install "uvicorn[standard]"
RUN pip install open_clip_torch


ENTRYPOINT ["/bin/bash"]