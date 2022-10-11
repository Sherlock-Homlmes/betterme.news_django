FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt update && apt install -y python3-opencv
RUN pip install opencv-python
#RUN systemctl stop redis
#RUN systemctl stop postgresql
COPY . /code/