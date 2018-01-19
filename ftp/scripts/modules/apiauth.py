#!/usr/bin/env python
#vim: syntax=python tabstop=2 expandtab

from authorizers import DummyAuthorizer
import os
from pyftpdlib._compat import unicode
from tornado.httpclient import HTTPRequest, AsyncHTTPClient

class APIAuth(DummyAuthorizer):
  read_perms = "el"
  write_perms = "adfmwMT"

  def __init__(self):
    self.user_table = {}

  def add_user(self, username, password, homedir, perm='el',
                 msg_login="Login successful.", msg_quit="Goodbye."):
    if self.has_user(username):
      raise ValueError('user %r already exists' % username)
    if not isinstance(homedir, unicode):
      homedir = homedir.decode('utf8')
    if not os.path.isdir(homedir):
      raise ValueError('no such directory: %r' % homedir)
    homedir = os.path.realpath(homedir)
    self._check_permissions(username, perm)
    dic = {
      'pwd': str(password),
      'home': homedir,
      'perm': perm,
      'operms': {},
      'msg_login': str(msg_login),
      'msg_quit': str(msg_quit)
    }
    self.user_table[username] = dic

  def add_anonymous(self, homedir, **kwargs):
    raise NotImplementedError

  def remove_user(self, username):
    """Remove a user from the virtual users table."""
    del self.user_table[username]

  def override_perm(self, username, directory, perm, recursive=False):
    raise NotImplementedError

  def validate_authentication(self, username, password, handler):
    msg = "Authentication failed."
    
