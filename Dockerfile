FROM python:3.9

# Set the working directory
WORKDIR /code

# Copy the project code and requirements.txt file
COPY . /code/

# Install project dependencies
RUN pip install -r requirements.txt
