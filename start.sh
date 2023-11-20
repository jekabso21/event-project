#!/bin/bash

echo "Starting the script..."

cd server

echo "Updating pip..."

placeholder_path_to_python -m pip install --upgrade pip

echo "Installing dependencies..."

placeholder_path_to_python -m pip install mariadb pytz fastapi cryptography uvicorn

echo "Running uvicorn server..."

uvicorn api:app --host 0.0.0.0 --port 3800 &

cd ..
cd client

echo "Installing npm dependencies..."

echo 'Password' | sudo -S npm install --legacy-peer-deps

echo "Building npm project..."

npm build

echo "Serving npm build..."

serve -s build &

echo "Script execution finished."