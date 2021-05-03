# set base image (host OS)
FROM python:slim

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN apt-get update && \
     apt-get install -y gcc && \
     pip install --upgrade -r requirements.txt && \
     apt-get purge -y gcc && apt-get -y autoremove && \
     rm -rf /var/lib/apt/lists/*
    
COPY src/ .  
# copy the content of the local src directory to the working directory

# command to run on container start
CMD [ "python","-u","pet.py" ] 