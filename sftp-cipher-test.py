#!/usr/bin/python

import paramiko
from os import urandom, unlink
from tempfile import NamedTemporaryFile
from time import time

from credenciales import host, port, username, password  # no lo subo a git

print "Creando archivo temporal..."
temporal = NamedTemporaryFile(delete=False)  # voy a borrarlo a mano al final
# tamanio = 1024*1024 * 10  # 10mb
tamanio = 1024*1024 * 100  # 100mb
# tamanio = 1024*1024 * 1024  # 1gb
temporal.write(urandom(tamanio))
print "Creado: %s" % temporal.name

print "Consultando Ciphers Disponibles..."
transport = paramiko.Transport((host, port))
transport.connect(username=username, password=password)
ciphers = transport.get_security_options()._get_ciphers()

for c in ciphers:
    print "Probando %s" % c

    transport = paramiko.Transport((host, port))
    transport.get_security_options().ciphers = [c, ]
    transport.connect(username=username, password=password)

    #print transport

    sftp = paramiko.SFTPClient.from_transport(transport)

    destino = '/tmp/%s' % c  #armo la ruta donde escribir

    try:
        inicio = time()
        sftp.put(temporal.name, destino)
        tiempo = time() - inicio
        print "La transferencia tomo ", tiempo
        sftp.remove(destino)
    except:
        pass

print "Borrando archivo temporal..."
unlink(temporal.name)
