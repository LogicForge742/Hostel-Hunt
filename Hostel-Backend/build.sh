#!/usr/bin/env bash
# exit on error
set-o errexit


echo "Installing dependancies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"


# If you have database migrations, uncomment these:
#echo "Running database migrations..."
#flask db upgrade