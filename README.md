### WARNING: IN PROGRESS, DO NOT USE

# docker

Docker distribution, ideal for beginners and studios alike.

<br>

### Usage

For development, here's what needs to happen.

```bash
$ git clone https://github.com/getavalon/docker.git --recursive
$ cd docker
$ docker build -t avalon/docker:1.0 .
$ docker run -ti --name avalon-docker --rm avalon/docker:1.0
...
```

To access and run Avalon, we will need to expose the files to the network with Samba and start the Mongo server.

```bash
$ cd docker
$ sh samba.sh
$ sh mongo.sh
```

You can get the IP address to the shared files with:

```bash
$ docker inspect avalon-samba | grep IPAddress
```

Before running the Avalon you'll need to tell where to find the Mongo server. You can find the IP address with:

```bash
$ docker inspect avalon-mongo | grep IPAddress
```

To run Avalon you can use following:
```bash
$ cd \\[avalon-samba IP address]\Avalon
$ set AVALON_MONGO=mongodb://[avalon-mongo IP address]:27017
$ avalon
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
