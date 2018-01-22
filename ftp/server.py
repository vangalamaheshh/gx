#!/usr/bin/env python
#vim: syntax=python tabstop=4 expandtab

import logging
import os
from pyftpdlib.servers import FTPServer
from modules.apiauth import APIAuth
from modules.gcphandler import GCPHandler

authorizer = APIAuth()
handler = GCPHandler
handler.authorizer = authorizer
handler.permit_foreign_addresses = True
handler.masquerade_address = os.environ["PUBLIC_IP"]
handler.passive_ports = range(60000, 60999)

logging.basicConfig(filename='/var/log/pyftpd.log', level=logging.INFO)

server = FTPServer(('0.0.0.0', 21), handler)
server.serve_forever()
