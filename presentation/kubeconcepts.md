
# Kubernetes Concepts

*Raghuram Devarakonda, June 25, 2020*

Note:
The contents of this file are meant to be presented as slides using
reveal.js (https://github.com/hakimel/reveal.js/) framework. So don't
modify the file if the changes cannot be displayed as slides.

---

## Agenda

- Containers

---

## Containers - Overview

- They run directly on a host without any intermediate layer (such as
  Hypervisor).
    - light-weight

- Containers are *isolated* groups of processes running on a single
  host.

- All containers share the kernel.

Note: Understanding containers is important as Kubernetes is
essentially a "container orchestration solution".

---

## Containers

<img src="containers.png" alt="drawing" style="width:700px;"/>

Note: This picture captures many important details about
containers. Incidentally, I don't like those images that show Docker
as a layer between Kernel and containers. There is no such Docker
layer. Docker simply sets up few things initially and starts the
container process. Once that is done, Docker is out of the way and has
no more role in the running of containers.

Note: Show the demo of basic http server Flask app, Dockerfile. Run on
the host as well as using Docker. Invoke the API using curl.

After the demo, talk about the issues that Kubernetes solves.

- What happens if a container goes down?
- How to run multiple copies and load balance?
- How do different containers can talk to each other (networking)?
- How to run containers on multiple machines?

And then mention that Kubernetes solves these issues.

---

## Kubernetes - Intro

- A container orchestration platform.

- Kubernetes is a cluster solution.

  - Manages multiple hosts and can seamlessly run workloads on any
    host. 

---

## Kubernetes Components

<img src="kubearch.png" alt="drawing" style="width:700px;"/>

---

## Control Plane

- Components that run on master nodes.

- They include:

  - API Server
  - Scheduler
  - Controller Manager

---

## Node Components

- They run on every node in the cluster.

- They include:
  - kubelet
  - kube-proxy

---

## Minikube

- An excellent option to install clusters locally.

- It can install using:
  - Docker
  - VirtualBox
  - Directly on host
  
Note: Show a quick demo of minikube.

---

## Kubectl

- A very powerful command line client for Kubernetes.

- It has many sub-commands but most important are the ones that deal
  with CRUD of resources.
  
Note: Very important to master kubectl. Show how to run basic server
pod and access it. Mention that we are not following recommended way.

---

## Resources

- Kubernetes implements REST APIs to manage all the objects.

- kubectl has sub-commands to manage the lifecycle of the resources.
  - create
  - get
  - apply
  - delete

---

## Creating a resource

    apiVersion: v1
    kind: Pod
    metadata:
      name: basicserver
    spec:
      containers:
      - image: basicserver:0.42
        name: basicserver

Note: Need YAML familiarity though JSON works as well. Mention about
API groups. Talk about "generateName". Mention that you will talk
about "status" shortly.

---

## Watch model

- Kubernetes APIs are asynchronous.

- All components in the cluster (e.g. Scheduler, kubelet) "watch" for
  changes and react to it.
  
- All controllers run control-loops
  - Watch, Reconcile, Publish

---

## Declarative Model

- Users define resources with "desired" state. It is the job of
  controllers to bring the cluster to that state.
  
- When controllers are notified of the resource changes, they are only
  given resource name.
  - They won't know what operation just happened to that resource.
  
Note: Talk about scheduler and kubelet processing of Pod creation. Use
ReplicaSet example to explain declarative model.

---

## Pods

- Model a "logical" host running multiple processes.
  - Pods are ephemeral.

- Specifying Environment variables

- Passing Command line arguments

- Init containers

Note: You will never create pods directly. But instead use higher
level constructs such as Deployments.

Env variables: Also mention how to pass metadata such as Pod name.

---

## Replica Sets

- Gurantees availability of a given number of identical pods.

- Spec
  - Pod selector
  - Number of replicas
  - Pod template
  
- Use Deployments instead of directly dealing with ReplicaSets.

- "Horizontal Pod Autoscaler" resource can be created to scale a
  ReplicaSet automatically.

Note: Number of replicas can easily be changed by updating
".spec.replicas".

---

## Deployments

---

## Services

---

## Auto Scaling

- 

## Storage

- Persistent Volumes

- Volume Snapshots

---

## Secrets and Configmaps

---

## Container Storage Interface (CSI)

---

## Labels and Annotations

---

## Authentication

---

## Authorization

---

## Community

- SIGs (sig-storage, sig-apps)

- Workgroups (e.g. data protection work group)

- Periodic zoom meetings

- KubeCon - North America/Europe

---

## Links

---

## Conclusion

---

