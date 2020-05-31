============
 Containers
============

Kubernetes is a *container orchestration platform* so containers are
at the heart of the technology.

Overview
========

Containers are *isolated* groups of processes running on a single
host. They run directly on a host without any intermediate layer as
opposed to `Virtual Machines`_ which require a `Hypervisor`_ to be
present. This is also the reason why containers are referred to as
a "light-weight" solution to deploy applications.

The most important point to note is the fact that container processes
run directly on the host. As can be seen in the following picture
(*source: docker.com*), there is no intermediate layer between kernel
and applications, as is the case with virtualization such as `vmware`_
and `VirtualBox`_. 

.. image:: images/containers.png
  :target: docker.com

So if the container processes run directly on the host, what stops
them from seeing each other or even affecting each other? That is
where the isolation aspects of the kernel comes in. Kernel has
mechanisms to isolate or sandbox a process (or a group of processes)
to the point that the processes behave as though they are running on a
dedicated host. This is  despite the fact that they are just normal
processes on the host and they can be seen from the host just like any
other processes (given sufficient permissions).

So Containerization is essentially creating an isolated environment
around a process or group of processes, limiting them in terms of what
they can see and what they can do.

Finally, it is important to understand that all containers share same
running kernel. There is no isolation there and that is another big
difference between `Virtual Machines`_ and containers. A side
effect of sharing the kernel is that if the container uses a
kernel module or does something with a kernel module, there is no way
to isolate it from other containers (with some exceptions, see `Kata
Containers`_). 

Container building blocks
=========================

There are three kernel features - *namespaces*, *cgroups*, and
*chroot*, that work together to make containers possible. Docker and
other container tools mainly use these features to build container
solutions.

chroot
------

*chroot* is a system call that changes the root directory of a
process. Once that happens, the process will only be able to access
files that are reachable from the new root directory.

Namespaces
----------

Namespaces allow partitioning of virtual system resources such as PIDs
and mounted file systems.

Here are some examples:

PID
    Isolates process ID ranges so that processes in different
    namespaces can have same PID. 

User
    Isolates UID and GID numbers. Especially useful to run as root
    inside the container. 

UTS
    Provides isolation for host name and domain name.

Control groups (cgroups)
------------------------

Control groups allow partitioning of physical system resources such as
CPU and memory.

They also allow limiting physical resources to a group of
processes. For example, if you want to limit a process to 100MB of
main memory even though the host has much larger memory, you can
easily do that using cgroups. 

Docker
======

Containers existed in one form or another for very long
time. E.g. `Solaris Zones`_, `lxc`_. But `Docker`_ brought the
technology to mainstream due to following reasons:

- Defined a simple and portable image format
- Made it easy to build new images
- Made sharing images a breeze (`Docker Hub`_)

Google has been using containers for long time. In fact, the initial
code for cgroups has been donated by Google. Since then, namespaces
were added to the mix and then "lxc" came along as a container
solution.

But the real popularity in the wide developer world started after
Docker came into the picture. The main reasons are the portable image
format and APIs.

For a good understanding of Docker, please see `Docker Concepts`_.

In the next chapter, we will see a simple example of how to work with
Docker containers.

.. _Hypervisor: https://en.wikipedia.org/wiki/Hypervisor
.. _Virtual Machines: https://en.wikipedia.org/wiki/Virtual_machine
.. _VirtualBox: https://www.virtualbox.org/
.. _vmware: https://www.vmware.com/solutions/virtualization.html
.. _Docker Concepts: https://docs.docker.com/get-started/overview/
.. _Docker: https://www.docker.com/
.. _Docker Hub: https://hub.docker.com/
.. _Kata Containers: https://katacontainers.io/
.. _Solaris Zones: https://en.wikipedia.org/wiki/Solaris_Containers
.. _lxc: https://en.wikipedia.org/wiki/LXC
