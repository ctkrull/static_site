# Run your static site generator
python3 src/main.py

# Move into the public directory and start the server
cd public && python3 -m http.server 8888
