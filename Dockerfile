FROM python:3.10-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn

# Copy the rest of the application code
COPY . /usr/src/app

# Specify the command to run on container start
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "event_management_system.wsgi:application"]

# Health check (optional)
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1
