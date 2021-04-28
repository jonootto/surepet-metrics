# set base image (host OS)
FROM python:slim

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY src/ .
# install dependencies
RUN pip install --upgrade -r requirements.txt
# copy the content of the local src directory to the working directory

# command to run on container start
CMD [ "python","-u","pet.py" ] 