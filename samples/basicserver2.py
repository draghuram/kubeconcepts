
import os
from flask import Flask
   
app = Flask(__name__)
   
@app.route('/')
def hello_world():
    greeting = os.environ.get("GREETING", "Hello")
    print("greeting = {}".format(greeting))

    return '{}, World!'.format(greeting)
   
if __name__ == '__main__':
    app.run(host="0.0.0.0")
