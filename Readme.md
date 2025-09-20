# How to run the app

# Build the Docker image
docker build -t unfaker-api .

# Run the container
docker run -d -p 8000:8000 --name unfaker-container unfaker-api