#!/bin/bash

# Optional: Set Flask environment variables 
export FLASK_APP=app.py  # Assuming your main Flask file is named app.py
export FLASK_ENV=local  

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
npm ci

if [ "$FLASK_ENV" == "local" ]; then
    echo "[ENTRYPOINT] Local environment detected. Running 'npm run build:css -- --watch'"
    npm run build:css -- --watch
else
    echo "[ENTRYPOINT] Environment is not local."
    
    # Build the CSS files
    echo "[ENTRYPOINT] Build the tailwind CSS files.."
    RUN npm run build:css
fi

echo "[ENTRYPOINT] Checking Flask version..."
flask --version

echo "[ENTRYPOINT] Starting the Flask server..."
cd /var/www/app
flask run --host=0.0.0.0