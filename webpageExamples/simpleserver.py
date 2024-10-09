import http.server
import socketserver
import os

# Define the directory containing your HTML file
web_dir = '/home/drakosfire/Projects/Script-Experiments/webpageExamples'
os.chdir(web_dir)  # Change the current working directory to serve the file

# Define the server port (can be any available port, here we use 8000)
PORT = 8000

# Create a simple HTTP request handler
Handler = http.server.SimpleHTTPRequestHandler

# Start the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
