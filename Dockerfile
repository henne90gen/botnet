# Use an official Python runtime as a parent image
FROM botnet_base:latest

ARG BOT
ENV BOT_NAME=$BOT

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

ENV PYTHONPATH=$PYTHONPATH:/app

# Run app.py when the container launches
CMD ["sh", "-c", "python ./botnet/${BOT_NAME}/${BOT_NAME}_bot.py"]
