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
# From Docker Quickstart
docker run --name avalon-files -d --rm \
    -p 445:445 \
    avalon/files \
    -s "Avalon;/avalon;yes;yes;yes;all;none;all" \
    -u "avalon;default"
docker run --name avalon-database -d --rm \
    -v avalon-database:/data/db \
    -p 27017:27017 \
    avalon/database
docker run --name avalon-tracker -d --rm \
    -v avalon-tracker:/var/lib/postgresql \
    -v avalon-tracker:/opt/zou/zou/thumbnails \
    -p 80:80 \
    avalon/tracker
```

Finally, from `cmd.exe` run the following to map Avalon files to a drive, such as `A:\`

```cmd
:: From cmd.exe
net use /delete a:
net use a: \\192.168.99.100\avalon /user:avalon default
```

Now you are ready to create a project and populate it with assets.

1. Double-click `A:\terminal.bat`
2. Type `avalon --help` to ensure the installation was successful
3. Go to [Tutorials](https://getavalon.github.io/2.0/tutorials/) for more

<br>

### Troubleshooting

Click on any of the below problems for potential causes and solutions.

<details>
 <summary>1. The network name cannot be found</summary>
  <br>
  <ul>
    <li>On Windows and OSX, find your IP via <code>docker-machine ip</code></li>
    <li>On Linux, exclude mapping of ports to the host and access the container IP directly</li>
    <li>If you encounter <code>The network name cannot be found</code> ensure you run the above in <code>cmd.exe</code> and not <code>Docker Quickstart</code>, <code>bash</code> or <code>MSYS2</code> etc.</li>
  </ul>
</details>

<details>
    <summary>2. Couldn't connect to mongodb</summary>
    <br>
    If you are having trouble running <code>avalon</code> due to not being able to connect with the database, odds are the Windows firewall is preventing the two from speaking.<br>
    <br>
    Run the following snippet from a <code>cmd.exe</code> with administrator privileges.
    <br>
    <pre>netsh advfirewall firewall add rule name="Avalon Database" dir=in action=allow protocol=TCP localport=27017
    </pre>
</details>

<br>

Can't find your problem? Submit a [bug report](../../issues)

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

To use your local copy of this repository for `A:\`, mount the repository into the `files` container.

```bash
docker kill avalon-files
docker run --name avalon-files -d --rm \
    -p 445:445 \
    -v $(pwd)/volume:/avalon \
    avalon/files \
    -s "Avalon;/avalon;yes;yes;yes;all;none;all" \
    -u "avalon;default"
```

See the [Usage](#usage) instructions, though you may want to remove `-d` and `-ti` so as to witness logs and more easily kill containers.

#### Testing

From `terminal.bat` run nose like so.

```bash
python -m nose tests
```
