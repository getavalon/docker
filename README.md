### WARNING: IN PROGRESS, DO NOT USE

# docker

Avalon on [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/), ideal for beginners and studios alike.

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

Use the overrides to mount your local development directory in place of the deployed version.

```bash
$ docker-compose -f docker-compose.yml -f docker-compose-dev.yml up
```
