### WARNING: IN PROGRESS, DO NOT USE

### Avalon on Docker

Avalon on Docker, ideal for beginners and studios alike.

> NOTE: This currently *only* works on [Docker Toolbox](https://github.com/docker/toolbox#installation-and-documentation), *not* Docker for Windows

<br>

### Usage on Windows

Avalon consists of three components:

1. Some **files** for integrating with Maya and friends
2. A **database** for storing production data such as assets, shot lengths and more
3. A **production tracking system** for visually managing assets, tasks and more

Each of these are served via Docker images.

With Docker available on your system, copy/paste the following commands into Docker Quickstart to start the Avalon components.

```bash
docker run --name avalon-files -d --rm \
    -p 445:445 \
    avalon/files:0.4 \
    -s "Avalon;/avalon;yes;no;yes;all;none;all" \
    -u "avalon;default"
docker run --name avalon-database -d --rm \
    -v avalon-database:/data/db \
    -p 27017:27017 \
    avalon/database:0.4
docker run --name avalon-tracker -d --rm \
    -v avalon-tracker:/var/lib/postgresql \
    -v avalon-tracker:/opt/zou/zou/thumbnails \
    -p 80:80 \
    avalon/tracker:0.4
```

Finally, from `cmd.exe` run the following to map Avalon files to a drive, such as `A:\`

```bash
net use /delete a:
net use a: \\192.168.99.100\avalon /user:avalon default
```

<details>
 <summary>Trouble?</summary>
  <br>
  <ul>
    <li>On Windows and OSX, find your IP via <code>docker-machine ip</code></li>
    <li>On Linux, exclude mapping of ports to the host and access the container IP directly</li>
    <li>If you encounter <code>The network name cannot be found</code> ensure you run the above in <code>cmd.exe</code> and not <code>Docker Quickstart</code>, <code>bash</code> or <code>MSYS2</code> etc.</li>
  </ul>
</details>

<br>

### Configuration

Change the username and password combination for `A:\` by swapping `-u "avalon;default"` for a combination of your choice.

To stop all containers, run the following.

```bash
docker kill avalon-files avalon-database avalon-tracker
```

To remove all changes to Avalon and start anew, run the following command.

```bash
docker volume rm avalon-database avalon-tracker
```

<br>

### Development

This repository contains all of Avalon as Git submodules. To extend Avalon, you typically edit each repository individually, and then point the submodules in this repository to your latest change.

```bash
git clone https://github.com/getavalon/docker.git --recursive
cd docker
docker build . -t avalon/files -f Dockerfile-files
docker build . -t avalon/database -f Dockerfile-database
docker build . -t avalon/tracker -f Dockerfile-tracker
```

See the [Usage](#usage) instructions, though you may want to remove `-d` and `-ti` so as to witness logs and more easily kill containers.
