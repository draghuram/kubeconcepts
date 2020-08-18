===========
 Resources
===========

We learned how to create a pod in the last chapter. But as I mentioned
there, we were not following the recommended way. In this chapter, we
will learn the canonical way of creating and managing Kubernetes
resources.

Overview
========

In Kubernetes, every object is a "resource" and every resource is
managed using REST APIs. Kubernetes consistently follows REST model
across the board so if you know how to deal with one resource, you
pretty much know how to deal with all other resources. 

You will be using `kubectl`_ to manage the resources as we have seen
in the last chaper. It acts as REST client and issues REST requests to
the API server. The sub-commands that are of most interest are:

create
    Creates resources.

get
    Gets a single resource or lists multiple resources.

apply
    Updates a resource and as a special case, it also creates a
    resource if one doesn't exist.

delete
    Deletes a resource.

People typically use "apply" almost all the time whether they are
creating a new resource or updating an existing one. This works in
majority of cases but there are occassions when you want to make sure
that you are creating a new resource. In these cases, explicitly use
"create". 

To create or update a resource, you need to supply request data and
Kubernetes follows a standard format for such input. Let us try to
create a "Pod" resource that runs the basic HTTP server from the
previous chapters. This is the same Pod we created before, using the
following command::

    $ kubectl run --image basicserver:0.42 testpod
    pod/testpod created

But this time, we will create the Pod resource using "kubectl create"
by building what is simply called "spec". It can be built using YAML
or JSON format but YAML is more prevalent so that is what we will use
here. It helps to know YAML format for making sense of many examples
in this guide so I suggest that you visit YAML page and understand
few core concepts. 

Here is the spec for the same Pod we created before::

    apiVersion: v1
    kind: Pod
    metadata:
      name: basicserver
    spec:
      containers:
      - image: basicserver:0.42
        name: basicserver

The very simple spec above demonstrates many things about Kubernetes
resources. Let us see what each line means.

- Every resource has a field "apiVersion". This is usually a
  combination of "apiGroup" and version. In this particular case, we
  only see a version "v1" but no group since Pods belong to "core"
  group. 

  Here is an example of "apiVersion for a "Job" resource:
  ``apiVersion: batch/v1``.

- Every resource type is identified by "Kind". 

The combination of "apiGroup", "version", and "Kind" uniquely
identifies every resource that Kubernetes supports. "apiGroup"
combines related funcitonality into a group that can be enabled or
disabled as per the need. This combination is what allows seamless
versioning of resources. You will frequently see new APIs move from
"v1alpha" to "v1beta" to eventually "v1".

Now, we come to "metadata" field. Metadata is the list of properties
that are common across all the resources. The most important of these
is the "name" which is a required field. Note that unlike other APIs,
Kubernetes uses name field as the ID. There is indeed a field called
UUID that is set when a resource is created. But you will see that
name itself is used as ID in most cases. For example, to get a
resource, you will pass name. I always found this a bit odd. So people
try to make the name itself unique. Kubernetes supports this
workaround by auto generating random names (with a given prefix). 

The other interesting metadata are "labels" and "annotations". Both
are key value pairs but have different purposes. 

We finally come to "spec" that really defines a resource. 

Spec is the real data that defines the resource. As can be expected,
it varies depending on the type of the resource. So in order to create
a resource, you need to know the schema of the spec. The easiest way
is to google for some samples and then modify them. But you can also
check the reference page which lists specs for all the resources
supported by Kubernetes. 

In the case of pod, the most important piece of information is what
containers are going to be part of it. Note that a Pod can have one or
more containers. In the example above, we have only one container. For
each container, we need to pass image and a "name".

There are many other fields that can be passed in a spec. A complete
reference can be found here. In the next chapter that covers Pods, we
will learn many more typical fields that are frequently used. The
intent of this chapter is to introduce Kubernetes model so we will not
spend more time on Pods.

.. _kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl/
