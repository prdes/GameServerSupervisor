FROM python:3.10-alpine

ARG supervisor_dir="/usr/src/GameServerSupervisor"

RUN mkdir -p $supervisor_dir

WORKDIR $supervisor_dir

COPY . $supervisor_dir

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
