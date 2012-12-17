#!/bin/sh

#TARBALL_FILENAME="lg_cms-`date +'%F'`.tar.gz"
TARBALL_FILENAME="lg_cms-latest.tar.gz"

echo "Packaging into $TARBALL_FILENAME"

git archive HEAD | gzip > $TARBALL_FILENAME

echo URL will be [something like] http://${USER}.endpoint.com/tmp/$TARBALL_FILENAME

sha256sum $TARBALL_FILENAME # Update chef's lg_cms recipe with this hash.

scp $TARBALL_FILENAME central.endpoint.com:~/htdocs/tmp/
