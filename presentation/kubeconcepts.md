
# Kubernetes Concepts

*Raghuram Devarakonda, June 25, 2020*

Note:
The contents of this file are meant to be presented as slides using
reveal.js (https://github.com/hakimel/reveal.js/) framework. So don't
modify the file if the changes cannot be displayed as slides.

---

## Agenda

- Containers
- Architecture
- Resources
- Conclusion

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

- kubectl has sub-commands to manage the life cycle of the resources.
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
      labels:
          component: webserver
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

## Custom Resources

- Custom Resource Definition (CRD)

- Custom Controllers
  - Combination of Custom resources and Custom controllers is known as
    an "Operator".

- Kubebuilder/Operator SDK

- KubeDR
  - https://github.com/catalogicsoftware/kubedr

Note: Take BackupLocation as an example and provide a complete
walk-through. 

---

## Pods

- Model a "logical" host running multiple processes.
  - Pods are ephemeral.

- Defining Environment variables

- Passing Command line arguments

- Init containers

Note: You will never create pods directly. But instead use higher
level constructs such as Deployments.

---

## Replica Sets

- Guarantees availability of a given number of identical pods.

- Use Deployments instead of directly dealing with ReplicaSets.

- "Horizontal Pod Autoscaler" resource can be created to scale a
  ReplicaSet automatically.

Note: Number of replicas can easily be changed by updating
".spec.replicas".

---

## Deployments

- The main use case of a Deployment is automated updates to the Pod. 

- An example is updating the container image in the Pod.

- It is also possible to rollback the updates.

---

## Namespaces

- Namespaces define "virtual" clusters.

- Resource names need to be unique only within a namespace.

- Not all resources can be created in a namespace.
  - Such resources are known as "Cluster-scoped"
    (e.g. "CustomResourceDefinition"). 

---

## Services

- An abstraction to expose applications running in a set of pods as a
  network service.
  
- Kubernetes creates a DNS name for each service so they can be
  reached by using its name within the cluster.
 
- Types
  - ClusterIP, NodePort, ...

---

## Auto Scaling

- Horizontal Pod Autoscaler

- Cluster Autoscaler

---

## Storage - Persistent Volumes

- Can be created statically or Kubernetes can create on demand.
  - Supported types: "Filesystem", "Block"

- A PV is requested by a Pod using *PersistentVolumeClaim* resource.

- StorageClasses help with dynamic provisioning of persistent
  volumes.
  
- Volume providers are available for all well known storage and cloud
  offerings.

---

## Container Storage Interface (CSI)

- Early on, storage providers were part of Kubernetes code base.
  - They are known as "in-tree" providers.
  
- CSI spec has been defined to make development of volume providers
  more flexible.
  
- Volume Snapshots
  - Only available with CSI drivers.

---

## Authentication

- Kubernetes has no resource abstracting users.
  - There is no way to tell which user created what resources.
  
- Supported authentication mechanisms:
  - Service accounts
  - Open ID connect
  - Authentication Proxies

---

## Authorization

- Supports RBAC (Role Based Access Control)

- Resources
  - Role/ClusterRole
  - RoleBinding/ClusterRoleBinding

---

## Other Resources...

- Secrets and Configmaps

- DaemonSets

- StatefulSets

- Jobs/CronJobs

---

## Kubernetes Distros

- There are many Kubernetes distributions available.
  - e.g. Rancher
  
- Managed solutions
 - GKE (Google), EKS (Amazon), AKS (Azure), DigitalOcean

---

## Advantages

- Cloud native

- Cloud agnostic

- Portable

---

## Ongoing Work

- Multi-tenancy
  - Hierarchical namespaces
  
- Container Object Storage Interface (COSI)

---

## Community

- SIGs (sig-storage, sig-apps)

- Workgroups (e.g. data protection work group)

- Periodic zoom meetings

- KubeCon - North America/Europe

---

## Links

- https://kubernetes.io/docs/concepts/

- https://kubernetes.io/docs/tasks/

- https://kubeconcepts.readthedocs.io/en/latest/index.html

---

## Conclusion

- Kubernetes has changed the way we architect and deploy applications.

- It is an important tool in building distributed and cloud native
  systems.

---

