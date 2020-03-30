FROM ubuntu:18.04

# Get the env_var PORT if set, if not set default value to 8080 
ENV PORT=8080
ENV LC_ALL=C
# Expose is only use to declare the internal port that is going to be
# used by the container. It might be useful for other developers, containers or apps.
EXPOSE ${PORT}

# Updates system, installs only compulsory dependencies
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install gcc python3 python3-pip python3-dev build-essential -y \
    # && pip install --upgrade numpy pystan pandas falcon gunicorn pymongo pmdarima fbprophet \
    && pip3 install --upgrade setuptools pyephem fbprophet pandas falcon gunicorn pymongo pmdarima \
    && mkdir prediction_microservice

# Copy app files to the container
COPY prediction_microservice /prediction_microservice

# Starts the app and starts mongo daemon in the back (--fork) and specifying log file and database folder.
CMD gunicorn -w 1 -b 0.0.0.0:8080 -t 6000 prediction_microservice.app