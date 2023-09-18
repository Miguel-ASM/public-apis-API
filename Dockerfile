# Use the official Python image from Docker Hub as the base image
FROM python:3.10

# Set environment variables to prevent buffering of Python output and ensure Python output is sent straight to terminal without being buffered
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH ./

# Create and set the working directory in the container
WORKDIR /srv

# Copy the Pipfile and Pipfile.lock to the container
COPY requirements.txt /srv/

# Install project dependencies using Pipenv
RUN pip install -r requirements.txt