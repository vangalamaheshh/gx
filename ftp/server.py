#!/usr/bin/env python
#vim: syntax=python tabstop=4 expandtab

import logging

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from modules.apiauth import APIAuth

authorizer = APIAuth()
handler = FTPHandler
handler.authorizer = authorizer
handler.permit_foreign_addresses = True
handler.passive_ports = range(60000, 65000)

logging.basicConfig(filename='/var/log/pyftpd.log', level=logging.INFO)

server = FTPServer(('0.0.0.0', 21), handler)
server.serve_forever()
