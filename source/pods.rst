
======
 Pods
======

In the last two chapters, we have built a good foundation of
Kubernetes core concepts. Now we can start with different resources
and controllers supported by Kubernetes. In this chapter, we will
learn about Pods.

We have already seen that Pods are the smallest deployable units in
Kubernetes and in fact, the only way to run any workload in the
cluster. All other resources are abstract in the sense that they
control how Pod run and how it is accessed but the real work is done
by Pods. 

Let us refer to the very simple Pod spec we used in the last chapter::

    apiVersion: v1
    kind: Pod
    metadata:
      name: basicserver
    spec:
      containers:
      - image: basicserver:0.42
        name: basicserver

Now, what if we want to pass some run time information to the Pod? Let
us modify our basic server to accept a command line target, like
so::

    import sys
    from flask import Flask
       
    app = Flask(__name__)
       
    @app.route('/')
    def hello_world():
        try:
            target = sys.argv[1]
        except:
            target = "World"
    
        return 'Hello, {}!'.format(target)
       
    if __name__ == '__main__':
        app.run(host="0.0.0.0")

Our server will say Hello to whatever target is passed on the
command line. Save it in a file called ``basicserver2.py``. We
need a new Docker image containing the changes. Here is a slightly
modified Dockerfile::

    FROM python:3
    
    RUN mkdir /opt/app && \
        python3 -m venv /opt/venv && \
        /opt/venv/bin/pip install flask
    
    COPY basicserver.py /opt/app
    COPY basicserver2.py /opt/app
    
    EXPOSE 5000/tcp
    
    CMD ["/opt/venv/bin/python", "/opt/app/basicserver.py"]

Notice the extra line that copies basicserver2.py. Also note that we
haven't made any changes to "CMD" which is deliberate. In order to run
``basicserver2.py``, we need to pass the command and arguments
explicitly. Now, build the Docker image::

    $ docker build -t basicserver:0.43 .

Here is a slight modified version of the pod spec that uses the new
image::

    apiVersion: v1
    kind: Pod
    metadata:
      name: basicserver2
    spec:
      containers:
      - image: basicserver:0.43
        args:
        - /opt/venv/bin/python
        - /opt/app/basicserver2.py
        - Universe
        name: basicserver

Notice the extra "args" field. We are passing command and arguments,
including the target "Universe". Now, create the pod as before::

    $ kubectl create -f pod2.yaml
    $ kubectl port-forward testpod 5000:5000
    Forwarding from 127.0.0.1:5000 -> 5000
    Forwarding from [::1]:5000 -> 5000

And verify::

  $ curl http://localhost:5000
  Hello, Universe!

So we saw how we can pass command and arguments in the Pod spec. 

There is another way to pass run time information and that is by way
of environment variables. Again, let us use same example but this
time, we will get the greeting from an env variable. Most of these
samples are obviously contrived but nevertheless, they convey the
concepts. 

Here is another version of basic server::

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

Save the file as ``basicserver3.py`` and build the Docker image after
adding the following line::

    COPY basicserver3.py /opt/app

Build the Docker image::

    $ docker build -t basicserver:0.44 .

And here is the new Pod spec::

    apiVersion: v1
    kind: Pod
    metadata:
      name: basicserver3
    spec:
      containers:
      - image: basicserver:0.44
        args:
        - /opt/venv/bin/python
        - /opt/app/basicserver2.py
        - Universe
        name: basicserver
        env:
        - name: GREETING
          value: Hi

Multiple Containers
===================

As I mentioned before, a Pod can be comprised of one or more
containers. In general, a Pod models a logical host and multiple
containers model a group of co-operative processes. They can all reach
each other at "localhost". They share network and port name
space. All the containers see same volumes (which are storage
abstractions as we will see later). 

Another useful feature is the ability to have "init" containers. As
the name suggests, these containers can run some init logic for entire
Pod before other containers start running. For example, a pod that
backups an application can use an init container to dump the
application data to a file which then can be backed up by the main
container. 

Replica Set
===========













Services
========

Till now, we have been able to issue HTTP request to basic server only
by port forwarding to the localhost. But that is not how servers are
accessed in general. The Kubernetes abstraction to expose a network
service is called "Service". In fact, that is the name of the resource
one would create in order to access a network service.

Let us define a service to access the basic server.











    
    
    




- labels
- service
- replica sets
- deployments
- CSI - use Minio as example
- Authentication
- community
- links
- tips and tricks (logs, describe)



