from flask import Flask
from threading import Thread



app = Flask('')

@app.route('/')
def a():
  return 'From Ahmed to the world (:'
def run():
  app.run(host='0.0.0.0', port=81)
def server():
  t = Thread(target=run)
  t.start()

