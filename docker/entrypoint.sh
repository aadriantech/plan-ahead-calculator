#!/bin/bash

# Optional: Set Flask environment variables 
export FLASK_APP=app.py  # Assuming your main Flask file is named app.py
export FLASK_ENV=development  # Set to 'production' for live deployment


INIT_FLAG_FILE=".tailwind_initialized"  # File to indicate initialization

# Check if the initialization flag file exists
if [ -f "$INIT_FLAG_FILE" ]; then
    echo "[ENTRYPOINT] Tailwind CSS appears to be already initialized. Skipping."
else
    echo "[ENTRYPOINT] Initializing Tailwind CSS..."
    npx tailwindcss init -p

    # Create the initialization flag file 
    touch "$INIT_FLAG_FILE" 
    echo "Tailwind CSS initialization completed."
fi

echo "[ENTRYPOINT] check flask version.."
flask --version

echo "[ENTRYPOINT] Starting the flask server.."
cd /var/www/app
flask run --host=0.0.0.0 
