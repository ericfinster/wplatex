'''

  wpblogentry.py - plasTeX python class file for wpblogenty.cls

  (c) 2010 Eric Finster

'''

from plasTeX.Base import Command

from article import *

class tags(Command):
    args = 'self'
    def invoke(self, tex):
        Command.invoke(self, tex)
        if not self.ownerDocument.userdata.has_key('tags'):
            self.ownerDocument.userdata['tags'] = self

class category(Command):
    args = 'self'
    def invoke(self, tex):
        Command.invoke(self, tex)
        if not self.ownerDocument.userdata.has_key('category'):
            self.ownerDocument.userdata['category'] = self

