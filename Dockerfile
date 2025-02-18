FROM python:3.10-alpine

ARG game_server_directory="/usr/src/GameServerSupervisor"

RUN mkdir -p $game_server_directory

WORKDIR $game_server_directory

COPY . $game_server_directory

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
