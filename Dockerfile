FROM python:3.10-slim-buster

# We don't want to run our application as root if it is not
# strictly necessary, even in a container.
#
# Create a user and a group called 'app' to run the processes.
# A system user is sufficient and we do not need a home.
RUN adduser --system --group --no-create-home app

# Place the application components in a dir below the root dir
COPY . /app

# Make the directory the working directory for subsequent commands
WORKDIR /app

# Install from the requirements.txt we copied above
# Speeds docker build up by 10x, but should probably 
# Not be used in production
RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip

RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

# Hand everything over to the 'app' user
RUN chown -R app:app /app

# Subsequent commands, either in this Dockerfile or in a
# docker-compose.yml, will run as user 'app'
USER app

# This command will more than likely vary a bit depending on which 
# environment we when to launch in.
CMD ["gunicorn", \
     "--workers", "1", \
     "--bind", "0.0.0.0:5000", \ 
     "wsgi:app", \
     "--reload", \
     "--reload-extra-file", "/work/app/templates/"]
