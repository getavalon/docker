# Test --backup and --restore
avalon --import batman
avalon --backup mybackup.zip
avalon --drop avalon
avalon --restore mybackup.zip
