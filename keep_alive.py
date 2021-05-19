from flask import Flask, render_template, redirect
from threading import Thread
app = Flask('')

@app.route('/')
def main():
  return 'wooooo bot is ready hehehe'
    
def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()