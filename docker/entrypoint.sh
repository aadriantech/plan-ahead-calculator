#!/bin/bash

# Optional: Set Flask environment variables 
export FLASK_APP=app.py  # Assuming your main Flask file is named app.py
export FLASK_ENV=local

# print environment variables
printenv | sort

INIT_FLAG_FILE=".tailwind_initialized" 

# Check if Tailwind CSS is initialized if not, create the necessary tailwind config files
if [ -f "$INIT_FLAG_FILE" ]; then
    echo "[ENTRYPOINT] Tailwind CSS appears to be already initialized. Skipping."
else
    echo "[ENTRYPOINT] Initializing Tailwind CSS..."
    npx tailwindcss init

    echo "[ENTRYPOINT] Creating postcss.config.js"
    cat > /var/www/app/postcss.config.js << EOF
module.exports = {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
EOF

    echo "[ENTRYPOINT] Update tailwind config js file.."
    cat > /var/www/app/tailwind.config.js << EOF
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF

    echo "[ENTRYPOINT] Creating main.css"
    mkdir -p /var/www/app/static/styles  # Create the styles directory if it doesn't exist
    cat > /var/www/app/static/styles/main.css << EOF
/* static/styles/main.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF

# Install the npm libraries
npm install -D tailwindcss postcss autoprefixer

    touch "$INIT_FLAG_FILE" 
fi

# Check and update if necessary npm libraries using NPM ci
echo "[ENTRYPOINT] check NPM libraries based on package lock file"
npm ci

if [ "$FLASK_ENV" == "local" ]; then
    echo "[ENTRYPOINT] Local environment detected."

else
    echo "[ENTRYPOINT] Environment is not local."
fi

# Build the CSS files
echo "[ENTRYPOINT] Build the tailwind CSS files.."
npx tailwindcss -i /var/www/app/static/styles/main.css -o /var/www/app/static/styles/output.css
TAILWIND_OUTPUT_FILE="/var/www/app/static/styles/output.css"

# Timeout settings
MAX_WAIT_SECONDS=30  # Maximum time to wait for the CSS file
CHECK_INTERVAL=5     # Interval between checks (in seconds)

# Loop until the file exists or the timeout is reached
COUNTER=0
while [ ! -f "$TAILWIND_OUTPUT_FILE" ] && [ $COUNTER -lt $MAX_WAIT_SECONDS ]; do
    echo "[ENTRYPOINT] CSS file not found. Waiting for $CHECK_INTERVAL seconds..."
    sleep $CHECK_INTERVAL
    COUNTER=$((COUNTER + CHECK_INTERVAL)) 
done

echo "[ENTRYPOINT] Checking Flask version..."
flask --version

# Check if the file appeared within the timeout
if [ -f "$TAILWIND_OUTPUT_FILE" ]; then
    echo "[ENTRYPOINT] CSS file found, Starting the Flask server..."
    cd /var/www/app
    flask run --host=0.0.0.0
else
    echo "[ENTRYPOINT] Timeout waiting for output CSS file. Exiting."
    # You might want to exit with an error code if appropriate: 
    exit 1
fi

