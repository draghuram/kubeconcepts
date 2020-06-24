
import os
import sys
from flask import Flask
   
app = Flask(__name__)
   
@app.route('/')
def hello_world():
    try:
        target = sys.argv[1]
    except:
        target = "World"

    greeting = os.environ.get("GREETING", "Hello")

    return '{}, {}!'.format(greeting, target)
   
if __name__ == '__main__':
    app.run(host="0.0.0.0")
