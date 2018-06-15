FROM ubuntu:16.04

#
# Setup Samba
#

RUN apt-get update && \
    apt-get install -y --force-yes \
        sudo \
        samba \
        apt-transport-https

RUN useradd -c 'Avalon User' -m -s /bin/bash avalon && \
    file="/etc/samba/smb.conf" && \
    sed -i 's|^;* *\(log file = \).*|   \1/dev/stdout|' $file && \
    sed -i 's|^;* *\(load printers = \).*|   \1no|' $file && \
    sed -i 's|^;* *\(printcap name = \).*|   \1/dev/null|' $file && \
    sed -i 's|^;* *\(printing = \).*|   \1bsd|' $file && \
    sed -i 's|^;* *\(unix password sync = \).*|   \1no|' $file && \
    sed -i 's|^;* *\(preserve case = \).*|   \1yes|' $file && \
    sed -i 's|^;* *\(short preserve case = \).*|   \1yes|' $file && \
    sed -i 's|^;* *\(default case = \).*|   \1lower|' $file && \
    sed -i '/Share Definitions/,$d' $file && \
    echo '   pam password change = yes' >>$file && \
    echo '   map to guest = bad user' >>$file && \
    echo '   usershare allow guests = yes' >>$file && \
    echo '   create mask = 0664' >>$file && \
    echo '   force create mode = 0664' >>$file && \
    echo '   directory mask = 0775' >>$file && \
    echo '   force directory mode = 0775' >>$file && \
    echo '   force user = avalon' >>$file && \
    echo '   force group = users' >>$file && \
    echo '   follow symlinks = yes' >>$file && \
    echo '   load printers = no' >>$file && \
    echo '   printing = bsd' >>$file && \
    echo '   printcap name = /dev/null' >>$file && \
    echo '   disable spoolss = yes' >>$file && \
    echo '   socket options = TCP_NODELAY' >>$file && \
    echo '   strict locking = no' >>$file && \
    echo '   vfs objects = recycle' >>$file && \
    echo '   recycle:keeptree = yes' >>$file && \
    echo '   recycle:versions = yes' >>$file && \
    echo '   min protocol = SMB2' >>$file && \
    echo '   [avalon]' >>$file && \
    echo '      path = /avalon' >>$file && \
    echo '      browsable = yes' >>$file && \
    echo '      read only = no' >>$file && \
    echo '      guest ok = yes' >>$file && \
    echo '      veto files = /._*/.apdisk/.AppleDouble/.DS_Store/.TemporaryItems/.Trashes/desktop.ini/ehthumbs.db/Network Trash Folder/Temporary Items/Thumbs.db/' >>$file && \
    echo '      delete veto files = yes' >>$file && \
    echo '      write list = all' >>$file && \
    echo '' >>$file

#
# Setup Mongo
#

# Add user and group first to make sure their IDs get assigned
# consistently, regardless of whatever dependencies get added
RUN groupadd -r mongodb && useradd -r -g mongodb mongodb && \
    mkdir /docker-entrypoint-initdb.d && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5 && \
    echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list && \
    apt-get update && \
    apt-get install -y \
        mongodb-org=3.6.4 \
        mongodb-org-server=3.6.4 \
        mongodb-org-shell=3.6.4 \
        mongodb-org-mongos=3.6.4 \
        mongodb-org-tools=3.6.4

RUN mkdir -p /data/db /data/configdb && \
	chown -R mongodb:mongodb /data/db /data/configdb

#
# Setup CGWire
#

RUN apt-get update && apt-get install --no-install-recommends -y \
    bzip2 \
    ffmpeg \
    git \
    nginx \
    postgresql \
    postgresql-client \
    python-pip \
    python-setuptools \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-venv \
    python3-wheel \
    redis-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/zou /var/log/zou /opt/zou/thumbnails

RUN git clone -b 0.6.6-build --single-branch --depth 1 https://github.com/cgwire/kitsu.git /opt/zou/kitsu

# setup.py will read requirements.txt in the current directory
WORKDIR /opt/zou/zou
RUN python3 -m venv /opt/zou/env && \
    # Python 2 needed for supervisord
    /opt/zou/env/bin/pip install --upgrade pip setuptools wheel && \
    /opt/zou/env/bin/pip install zou==0.6.4 && \
    rm -rf /root/.cache/pip/

WORKDIR /opt/zou

# Create database
USER postgres

RUN service postgresql start && \
    createuser root && createdb -T template0 -E UTF8 --owner root root && \
    createdb -T template0 -E UTF8 --owner root zoudb && \
    service postgresql stop

USER root

# Wait for the startup or shutdown to complete
RUN printf "pg_ctl_options = '-w'" > /etc/postgresql/9.5/main/pg_ctl.conf
RUN chmod 0644 /etc/postgresql/9.5/main/pg_ctl.conf && chown postgres:postgres /etc/postgresql/9.5/main/pg_ctl.conf

RUN mkdir -p /etc/zou
RUN echo "accesslog = \"/var/log/zou/gunicorn_access.log\"" > /etc/zou/gunicorn.conf
RUN echo "errorlog = \"/var/log/zou/gunicorn_error.log\"" >> /etc/zou/gunicorn.conf
RUN echo "workers = 3" >> /etc/zou/gunicorn.conf
RUN echo "worker_class = \"gevent\"" >> /etc/zou/gunicorn.conf
RUN echo "timeout = 600" >> /etc/zou/gunicorn.conf

RUN echo "accesslog = \"/var/log/zou/gunicorn_events_access.log\"" > /etc/zou/gunicorn-events.conf
RUN echo "errorlog = \"/var/log/zou/gunicorn_events_error.log\"" >> /etc/zou/gunicorn-events.conf
RUN echo "workers = 1" >> /etc/zou/gunicorn-events.conf
RUN echo "worker_class = \"geventwebsocket.gunicorn.workers.GeventWebSocketWorker\"" >> /etc/zou/gunicorn-events.conf

COPY ./nginx.conf /etc/nginx/sites-available/zou
RUN ln -s /etc/nginx/sites-available/zou /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default

# supervisor will manage services
RUN pip install supervisor
ADD supervisord.conf /etc/supervisord.conf

ENV DB_USERNAME=root DB_HOST=
RUN echo Initialising Zou... && \
    export LC_ALL=C.UTF-8 && \
    export LANG=C.UTF-8 && \
    service postgresql start && \
    service redis-server start && \
    . /opt/zou/env/bin/activate && \
    zou upgrade_db && \
    zou init_data && \
#    zou create_admin admin@example.com && \
    service postgresql stop && \
    service redis-server stop

# Mongo
EXPOSE 27017

# Samba
EXPOSE 137/udp 138/udp 139 445

# CGWire
EXPOSE 80

VOLUME /data/db /data/configdb
VOLUME /avalon

COPY volume /avalon

# Edit via e.g. docker run -e password=mypass getavalon:0.2
ENV password=default

ENTRYPOINT \
    bash -c 'echo -e "$password\n$password" | /usr/bin/smbpasswd -s -a "avalon"' && \
    . /usr/share/postgresql-common/init.d-functions && \
    create_socket_directory && \
    supervisord -c /etc/supervisord.conf
