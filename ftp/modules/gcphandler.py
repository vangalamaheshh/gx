#!/usr/bin/env python
#vim: syntax=python tabstop=2 expandtab

from pyftpdlib.handlers import FTPHandler
from google.cloud import storage
import os

class GCPHandler(FTPHandler):
  def on_file_received(self, file):
    storage_client = storage.Client.from_service_account_json(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    bucket = storage_client.get_bucket(os.environ["FTP_BUCKET"])
    blob = bucket.blob(file[5:]) # strip leading /tmp/
    blob.upload_from_filename(file)
    os.remove(file)

