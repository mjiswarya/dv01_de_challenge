FROM ubuntu:latest
LABEL authors="iswaryamogalapalli"

# Set the working directory in the container to /app
WORKDIR /dv01_de_challenge

# Add the current directory contents into the container at /app
ADD . /dv01_de_challenge
RUN apt-get update && \
    apt-get install -y python3-pip
# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 800 available to the world outside this container
EXPOSE 800

# Run CSVParquetHandler.py when the container launches
CMD ["python3", "./CSVParquetHandler.py", "&&", "python3", "./CSVHandler.py"]