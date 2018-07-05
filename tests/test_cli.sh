# Test --backup and --restore
avalon --import batman
avalon --backup mybackup.zip
avalon --drop batman
avalon --restore mybackup.zip

# Cleanup
rm mybackup.zip
avalon --drop batman
