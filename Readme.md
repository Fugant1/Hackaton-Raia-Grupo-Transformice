# Unfaker
Unfaker is a Chrome extension and API designed to detect fake news in social media posts (currently integrated with X/Twitter).
It uses machine learning models and automated analysis to flag potentially misleading content and provide users with insights before they engage with it.

# Tech Stack
1. FastAPI for the backend
2. Docker for containerization
3. Chrome Extension for client-side integration
4. ML/NLP models for fake news detection

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

# Acknowledgments
This project was originally developed during the Hackaton Raia - Grupo Transformice.
