FROM python:3.9.19-bookworm

# Install necessary tools
RUN apt-get update && apt-get install -y vim npm

RUN mkdir -p /var/www

WORKDIR /var/www

# Copies your project files into web folder
COPY . .

# Copy the files into the container at the root directory
COPY ./docker/entrypoint.sh /entrypoint.sh
COPY ./docker/requirements.txt /requirements.txt

# Install the python libraries
RUN pip install -r /requirements.txt

# Install the npm libraries
RUN npm install -D tailwindcss postcss autoprefixer


RUN chmod +x /entrypoint.sh && chmod +x /requirements.txt

ENTRYPOINT ["/entrypoint.sh"]
