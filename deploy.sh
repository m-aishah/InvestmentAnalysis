#!/bin/bash

# Navigate to your application directory
cd ~/investment_app || exit

# Pull the latest changes from the GitHub repository
git pull origin main

# Install any Python dependencies
pip3 install -r requirements.txt

# Run your data access script
python3 data/data_access.py

# Run your main application
python3 src/main.py

echo "Deployment completed successfully!"
