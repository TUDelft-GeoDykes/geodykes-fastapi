#!/bin/bash

# This scripts exports all the environment variables from the .env file

# Check if the .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file does not exist."
    exit 1
fi

# Export all variables from the .env file
while IFS='=' read -r key value
do
  # Skip lines starting with # which are comments
  if [[ $key != \#* ]]; then
    export $key="$value"
    echo "Exported $key=$value"
  fi
done < ".env"

echo "All environment variables have been exported."
