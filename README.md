# docker

Docker distribution, ideal for beginners and studios alike.

<br>

### Usage

For development, here's what needs to happen.

```bash
$ git clone https://github.com/getavalon/docker.git
$ cd docker
$ docker build -t avalon/docker:1.0 .
$ docker run -ti --rm avalon/docker:1.0
...
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
$ docker run -d avalon/docker:1.0
```