=========
 Example
=========

We will start with a simple HTTP server and use it to demonstrate
Kubernetes concepts throughout.

Here is a very basic Flask server taken from:

https://flask.palletsprojects.com/en/1.1.x/quickstart/

.. code-block:: python

   from flask import Flask
   
   app = Flask(__name__)
   
   @app.route('/')
   def hello_world():
       return 'Hello, World!'
   
   if __name__ == '__main__':
       app.run(host="0.0.0.0")

As can be seen, the server is very simple and implements a single end
point. Run the server as follows:

.. code-block:: bash

  $ python3 -m venv ~/venv/flask
  $ export PATH=~/venv/flask/bin:$PATH
  $ pip install flask
  $ python basicserver.py

It can be invoked as follows:

.. code-block:: bash

  $ curl http://localhost:5000
  Hello, World!

As a next step, we will build a Docker image and run the server in a
container (instead of directly running on the host):

.. code-block::

   FROM python:3

   RUN mkdir /opt/app && \
       python3 -m venv /opt/venv && \
       /opt/venv/bin/pip install flask
   
   COPY basicserver.py /opt/app
   
   EXPOSE 5000/tcp
   
   CMD ["/opt/venv/bin/python", "/opt/app/basicserver.py"]

.. code-block:: bash

  $ docker build -t basicserver:0.42 .
  $ docker run -p 5000:5000 --rm -it basicserver:0.42
    ...

  $ curl http://localhost:5000
  Hello, World!

At this point, we have a Docker image for a simple and basic HTTP
server and we have seen how it can be run as a Docker container. In
the next chapter, we will see how we can deploy the same server in
Kubernetes.



   


