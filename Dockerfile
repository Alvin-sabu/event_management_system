FROM python:3.10-slim

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
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

# Remove gcc to save space
RUN apt-get purge -y --auto-remove gcc

# Clean up cached files
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . /usr/src/app

# Specify the command to run on container start
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "event_management_system.wsgi:application"]
