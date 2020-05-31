======================
Containers - Practical
======================

This section will continue the discussion of containers by focusing on
practical aspects of how to build images and run them.

We will start with a simple HTTP server and use it to demonstrate
Container and Kubernetes concepts throughout the guide.

Here is a very basic example taken from `Flask Quickstart`_:

.. code-block:: python

   from flask import Flask
   
   app = Flask(__name__)
   
   @app.route('/')
   def hello_world():
       return 'Hello, World!'
   
   if __name__ == '__main__':
       app.run(host="0.0.0.0")

As can be seen, the server is very simple and implements a single end
point. You can run the server as follows (command output is not
shown):

.. code-block:: bash

  $ python3 -m venv ~/venv/flask
  $ export PATH=~/venv/flask/bin:$PATH
  $ pip install flask
  $ python basicserver.py

The end point can be verified with *curl*.

.. code-block:: bash

  $ curl http://localhost:5000
  Hello, World!

So our little HTTP server is up and responding to requests. Note that
the server is running directly on the host.

As a next step, we will build a Docker image and run the server in a
container (instead of directly running on the host). Here are the
contents of ``Dockerfile``::

   FROM python:3

   RUN mkdir /opt/app && \
       python3 -m venv /opt/venv && \
       /opt/venv/bin/pip install flask
   
   COPY basicserver.py /opt/app
   
   EXPOSE 5000/tcp
   
   CMD ["/opt/venv/bin/python", "/opt/app/basicserver.py"]

You usually build images from existing images as we are doing here. We
are using ``python:3`` as the base image on top of which we install
our application and configure some options. In this case, we are
installing `Flask`_ and copying our application code. The "EXPOSE" 
directive indicates that the process in the container listens on
port 5000. Finally, we specify the command to execute when some one
"runs" the container. 

Once we have a Dockerfile, we can build the container image and then
"run" it.

.. code-block:: bash

  # Build the container with name "basicserver" and tag "0.42" 
  # This command must be run in the same directory that contains
  # "Dockerfile".
  $ docker build -t basicserver:0.42 .

We are now ready to "run" the container.

.. code-block:: bash

  $ docker run -p 5000:5000 --rm -it basicserver:0.42

"-p" option is to map the container port 5000 on to the host (so that
we can access it directly on "localhost"). You can map to any
available port, not just 5000. For information about other options,
check `Docker Run`_ reference.

At this point, the HTTP server is running and we can access it using
"curl" just like before.

.. code-block:: bash

  $ curl http://localhost:5000
  Hello, World!

Note that the way we access the server hasn't changed but we are now
running it in a "container" instead of directly on a host. Imagine you
have a machine that has no Python or Flask installed. You can still
run the container using Docker and use the application. This is
possible because all the required components of the server
(e.g. Python and Flask) are packaged in the container image.

It is interesting to note that a container image corresponds to an
"executable" file such as ELF binary and a "container" corresponds to a
running process. Just like running a process involves taking an
executable file and creating a "process", running a container takes an
image and creates a "container".

You don't need to build images yourself in order to use containers. In
many cases, you will be able to use images that are already available
at `Docker Hub`_.

Use Cases
=========

There are many different scenarios where you can use containers. Here
are couple of main ones:

Microservices
    Microservices are services that implement a small and well defined
    interface. They are typically accessed using REST. Containers are
    a perfect fit run microservices.

Tools
    If you want to run a tool but don't want to install it on your
    machine, containers are the way to go. For example, I usually run
    `Jekyll`_ locally as follows, to check that my blog looks ok (`my
    blog`_ is built using `Jekyll`_).

.. code-block:: bash

    $ docker run -it --rm --volume=$(pwd):/srv/jekyll -it -p \4000:4000
        jekyll/jekyll jekyll s 

Conclusion
==========

This concludes the discussion about containers in general and Docker
in particular. If you want to explore further, here are some useful
resources: 

- `Container image spec`_
- `Container runtime spec`_
- `Docker Concepts`_
  
At this point, we have a Docker image for a simple and basic HTTP
server and we have seen how it can be run as a Docker container. In
the next chapter, we will see how we can deploy the same server in
Kubernetes.

.. _Flask: https://flask.palletsprojects.com/en/1.1.x/
.. _Docker Run: https://docs.docker.com/engine/reference/run/
.. _Docker Hub: https://hub.docker.com/
.. _Jekyll: https://jekyllrb.com/
.. _Container image spec: https://github.com/opencontainers/image-spec   
.. _Container runtime spec: https://github.com/opencontainers/runtime-spec
.. _Docker Concepts: https://docs.docker.com/get-started/overview/
.. _Flask Quickstart: https://flask.palletsprojects.com/en/1.1.x/quickstart/
.. _my blog: https://draghuram.github.io
