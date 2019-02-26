FROM python:3.7-alpine

# Install bash
RUN apk add --no-cache bash

# Go grab our repo
RUN apk add --update git && \
    git clone https://github.com/Ductapemaster/raspi_datalogger.git /app/raspi_datalogger && \
    rm -rf raspi_datalogger/.git && \
    apk del git && \
    rm -rf /var/cache/apk/*

# Install python requirements
RUN pip install -r /app/raspi_datalogger/requirements.txt

# Copy our credentials file into the container
COPY secrets.py /app/raspi_datalogger/secrets.py
COPY settings.py /app/raspi_datalogger/settings.py

# Set up logging dir
VOLUME /var/log

# Set up working directory
WORKDIR /app/raspi_datalogger

# Run it!
CMD ["python", "webserver.py"]
