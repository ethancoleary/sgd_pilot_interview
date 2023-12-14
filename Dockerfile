# Base Image
FROM python:3.10

# Maintainer
LABEL maintainer="Sebastian Fest <sebastian.fest@nhh.no>"

# Set working directory
WORKDIR /app

# Install wait-for-it package
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y wait-for-it

# Python Interpreter Flags
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencies installation
COPY ./requirements_base.txt /app/requirements.txt
RUN pip install --upgrade --quiet pip && pip install --no-cache-dir --quiet -r /app/requirements.txt

# Copy project
COPY . /app/

# Alter entrypoint script
COPY ./compose/local/entrypoint.sh /app/compose/local/entrypoint.sh
RUN sed -i 's/\r$//g' /app/compose/local/entrypoint.sh
RUN chmod +x /app/compose/local/entrypoint.sh

# Specify network port
EXPOSE 8080