FROM ubuntu:latest

MAINTAINER "AlirezaKm" "alirezakm@riseup.net"

# Define Arguments
ARG TOKEN
ARG WEB_HOOK
ARG DOMAIN
ARG PORT

# Update Repositories
RUN apt-get update

# Speed up package installation
RUN apt-get install -y apt-utils

# Install required packages
RUN apt-get install -y pngquant parallel jpegoptim file python3 python3-pip

# "Setup tapnesh"

# Copy files into container
COPY tapnesh.sh /bin/tapnesh

# Make tapnesh executable
RUN chmod +x /bin/tapnesh

# "Setup Telegram Bot"

# Create a Directory for application
RUN mkdir /application

# Change current directory to /application
WORKDIR /application

# Copy Requirements into container
COPY ./TelegramBot/requirements.txt .

# Install python libraries
RUN pip3 install -r ./requirementes.txt

# Copy bot.py into container
COPY ./TelegramBot/*.py /application/

# Run BOT
CMD python3 ./bot.py $TOKEN $WEB_HOOK $PORT $DOMAIN