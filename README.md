### WARNING: IN PROGRESS, DO NOT USE

# docker

Docker distribution, ideal for beginners and studios alike.

<br>

### Usage

For development, here's what needs to happen.

```bash
$ git clone https://github.com/getavalon/docker.git
$ cd docker
$ docker build -t avalon/docker:1.0 .
$ docker run -ti --name avalon-docker --rm avalon/docker:1.0
...
```

To access and run Avalon, we will need to expose the files to the network with samba.

```bash
$ cd docker
$ sh samba.sh
```

You can get the IP Address to the shared files with:

```bash
docker inspect avalon-samba | grep IPAddress
```

<br>

### Deployment

Uploads can be made automatically, but a manual start is fine.

```bash
$ docker upload avalon/docker:1.0
```

<br>

### End-user usage

Users won't need any of the above, just..

```bash
$ docker run -d --name avalon-docker avalon/docker:1.0
```
