==================
 Kubernetes Model
==================

We learned how to create a pod in the last chapter. But as I mentioned
there, we were not following the recommended way. In this chapter, we
will learn the canonical way of creating and managing Kubernetes
resources.

Resources
=========

In Kubernetes, every object is a "resource" and every resource is
managed using REST APIs. Kubernetes consistently follows REST model
across the board so if you know how to deal with one resource, you
pretty much know how to deal with all other resources. 

You will be using kubectl to manage the resources as we have seen in
the last chaper. It acts as REST client and issues REST requests to
the API server. The sub-commands that are of most interest are:

- create
- get
- apply
- delete

"create" creates resources. "get" either gets a single resource or
lists multiple resources. "apply" updates a resource and as a special
case, it also creates a resource if one doesn't exist. "delete"
deletes the resource.

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

Watch model
===========

So what happens when a resource is created? Or for that matter, when
an operation such as update or delete is done on a resource? As we
have seen above, all resource operations are done using REST APIs. The
APIs are implemented by API server. Let us see in detail what happens
when we create a Pod using above YAML::

     $ kubectl create -f testpod.yaml

The REST request to create a Pod resource reaches API server which
will perform validation and then persists the data in etcd. At this
point, API server doesn't do anything related to pod creation. Its job
is only to authenticate the request, validate the data, and then save
in etcd. But Kubernetes has a "watch" model where controllers can
"watch" for a given resource. So once a resource is persisted in etcd,
these watchers will be notified by API server and it is these
controllers who really carry out the business logic. In this sense,
all the (management) APIs in Kubernetes are asynchronous. The real
work happens asynchronously and not as part of processing the request
itself. 

In this specific case, "scheduler" will notice that a Pod resource has
been created. It will look for available nodes and schedules the Pod
on one of those nodes. Once a node is picked, it will update
"nodeName" field in the pod spec. So when the Pod resource is updated
with node name, yet another controller "kubelet" on the just picked
node notices that a Pod's node name is updated with its own node name
and that the containers of the Pod are not running yet. So it starts
containers and in turn updates the status of the Pod. 

This logic of watch + process + publish is known as "control loop" and
most of Kubernetes implementation is running control loops. 

Declarative Model
=================

Kubernetes follows what is known as "declarative model" when it comes
to defining resources. When we created the Pod definition above, we
are defining the "desired" state of the resource. We are not saying
"run these containers" but instead, we are defining a resource with
all the details and let the controllers do the rest. 

The control loop mentioned above will read the latest spec, check if
the current status in the cluster matches that spec. If not, they will
do the required work to bring the current status to the desired
status. So when we created a Pod resource, scheduler notices that
there is a Pod resource without "nodeName". So it jumps into action
and picks a node and updates "nodeName". When a Pod resource is
created, kubelet will also notice the new resource. But it will also
see that there is no "nodeName" field so there is nothing for it to
do. But once resource is updated with nodeName, all kubelets will
notice the change. But onloy the kubelet on the right node will start
containers. 

**Talk about stateless implementaiton of controllers. They are only
given name of the resource**.

Declarative model will become clear with another example. There is a
resource called "ReplicaSet" where you can define how many replicas
you want to run for a pod. Say, I created the resource asking for 3
replicas. But almost immediately, I changed my mind and udpated the
resource with 5 replicas. In a declarative model, ReplicaiSet
controller will watch for ReplicaSet resources and when it notices a
new resource, it will read the latest spec of that resource. Now, the
value it reads may be 3 or 5 depending on when it was notfied and load
on the system. If it read 5, it will check how many pods are
running. If there are not 5 replicas, it will start the remaining
number to bring up the replicas to 5. The controller doesn't even know
that number of replicas was 3 at some point and nor does it care. This
is the reason the resource model is known as "declarative". The user
is merely configuring what is the desired state. 

You should now be familiar with the core resource concepts and now
should be able to manage resources by creating the YAML definitions. 
