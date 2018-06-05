### WARNING: IN PROGRESS, DO NOT USE

# docker

Avalon on [Docker Toolbox](https://github.com/docker/toolbox#installation-and-documentation), ideal for beginners and studios alike.

<br>

### Usage

With Docker available on your system, run the following command.

```bash
$ docker run --rm -v $(pwd):/work -w /work appropriate/curl -O https://raw.githubusercontent.com/getavalon/docker/master/docker-compose.yml && docker rm $(docker ps -aq --filter name=getavalon) 2> /dev/null && docker-compose up -d
```

<br>

### Resources

Next we'll mount Avalon's resources to a local drive, such as `A:\` on Windows and `/mnt/avalon` on Linux and OSX.

```bash
$ net use a: \\192.168.99.100\avalon
```

<br>

### Development

For development [Git](https://git-scm.com/) is required.

```bash
$ git clone https://github.com/getavalon/docker.git --recursive
$ cd docker
$ docker build . -t avalon/latest
$ docker run -ti --rm -p 27017:27017 -p 445:445 -p 139:139 avalon/latest
```

Once the Docker container is running, you now have a Mongo database running. This means you can modify the code in the ```docker``` repository without restart or rebuilding the container.
