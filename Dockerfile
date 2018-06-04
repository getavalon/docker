FROM ubuntu:trusty

#
# Setup Samba
#

RUN apt-get update && \
    apt-get install -y --force-yes \
        samba \
        apt-transport-https

RUN useradd -c 'Samba User' -m -s /bin/bash smbuser && \
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
    echo '   force user = smbuser' >>$file && \
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

# Mongo
EXPOSE 27017

# Samba
EXPOSE 137/udp 138/udp 139 445

VOLUME /data/db /data/configdb
VOLUME /avalon

COPY volume /avalon

ENTRYPOINT \
    /usr/sbin/smbd -D && \
    /usr/bin/mongod --bind_ip_all
