#!/usr/bin/sh
# Construct a network
docker network create -d bridge my-network
# MYSQL server
# Pull mysql image from Docker Hub
docker pull mysql:5.7
# Run the mysql container
docker run -d --name mysql-server --network my-network -e MYSQL_ROOT_PASSWORD=secret mysql:5.7
# Flask server
# Build flask image
docker build -t flask-app .
# Run the flask server
docker run -p 5000:5000 --network my-network -v "$PWD":/app -d flask-app
