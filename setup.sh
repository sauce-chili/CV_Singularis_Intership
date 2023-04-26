#!/bin/bash

echo "Start building project..."

if [[ -z "${VIRTUAL_ENV}" ]]; then
  echo "Create new virtual environment"
  python3 -m venv venv
  source venv/bin/activate
else
  echo "Virtual environment already active"
fi

echo "Installing dependencies..."

pip3 install -r requirements.txt

echo "Build completed."