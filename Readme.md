# How to run the app

## Build the Docker image
docker build -t unfaker-api .

## Run the container
docker run -d -p 8000:8000 --name unfaker-container unfaker-api

## Install chrome extension

- Open google chrome and go to `chrome://extensions/`;
- Enable developer mode
- Click "Load Unpacked" and select the folder `web/`

## See it in action

Open a X post and see a popup with our analysis.

