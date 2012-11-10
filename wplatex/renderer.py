'''

  renderer.py - Wordpress Rendering Classes

  (c) 2010 Eric Finster

'''

from plasTeX.TeX import TeX
from plasTeX.Renderers import Renderer, Renderable, mixin, unmix
from plasTeX.DOM import Node
from plasTeX import TeXDocument, Macro

class WPRenderable(Renderable):
    """Mixin class for rendering WordPress posts
    """
    
    def __unicode__(self, ):
        """Return a unicode representation of this node
        """
        r = Node.renderer
        
        # If we don't have childNodes, then we're done
        if not self.hasChildNodes():
            return u''
        
        # At the very top level, only render the DOCUMENT_LEVEL node
        if self.nodeType == Node.DOCUMENT_NODE:
            childNodes = [x for x in self.childNodes 
                            if x.level == Node.DOCUMENT_LEVEL]
        else:
            childNodes = self.childNodes

        # Render all child nodes
        s = []
        for child in childNodes:

            # Short circuit text nodes
            if child.nodeType == Node.TEXT_NODE:
                s.append(r.textDefault(child))
                continue

            names = [child.nodeName]

            # Locate the rendering callable, and call it with the 
            # current object (i.e. `child`) as its argument.
            func = r.find(names, r.default)
            val = func(child)

            # Append the resultant unicode object to the output
            s.append(val)

        return u''.join(s)

    @property
    def filename(self):
        # Don't generate any files at all
        return None

#
#  Here is the main rendering implementation
#

class WPRenderer(Renderer):
    """Renderer for Wordpress Blog Post
    """

    renderableClass = WPRenderable

    aliases = {
        'superscript': 'active::^',
        'subscript': 'active::_',
        'dollar': '$',
        'percent': '%',
        'opencurly': '{',
        'closecurly': '}',
        'underscore': '_',
        'ampersand': '&',
        'hashmark': '#',
        'space': ' ',
        'tilde': 'active::~',
        'at': '@',
        'backslash': '\\',
    }

    def __init__(self, *args, **kwargs):
        """Initialize the Renderer
        """
        Renderer.__init__(self, *args, **kwargs)
        
        # Load dictionary with methods
        for key in vars(type(self)):
            if key.startswith('do__'):
                self[self.aliases[key[4:]]] = getattr(self, key)
            elif key.startswith('do_'):
                self[key[3:]] = getattr(self, key)

    def render(self, document, postProcess = None):
        """Render this to unicode
        
        Arguments:
        - `document`:
        """

        # Mix in required methods and members
        mixin(Node, type(self).renderableClass)
        Node.renderer = self

        result = unicode(document)

        # Remove mixins
        del Node.renderer
        unmix(Node, type(self).renderableClass)

        return result

    def default(self, node):
        """ Rendering method for all non-text nodes """
        # Handle characters like \&, \$, \%, etc.
        if len(node.nodeName) == 1 and node.nodeName not in string.letters:
            return self.textDefault(node.nodeName)
            
        # default is to use the latex source
        return unicode(node.source)

    def textDefault(self, node):
        return unicode(node)

    def do_document(self, node):
        """Render the top level document
        
        Arguments:
        - `node`:
        """
        return u'\n%s' % unicode(node)

    def do_par(self, node):
        """Render a paragraph
        
        Arguments:
        - `node`:
        """
        return u'<p>\n%s\n' % unicode(node)

    def do_displaymath(self, node):
        """Process the displaymath environment
        
        Arguments:
        - `node`:
        """
        return u'<p align=center>$latex \displaystyle %s &fg=000000$</p>\n' % unicode(node)

    def do_equation(self, node):
        """Process the equation environment
        
        Arguments:
        - `node`:
        """
        return u'<p align=center>$latex \displaystyle %s &fg=000000$</p>\n' % unicode(node)

    def do_math(self, node):
        """Render math equations
        
        Arguments:
        - `node`:
        """
        return u'$latex {%s}&fg=000000$' % unicode(node)

    def do_center(self, node):
        return u'<p align=center> %s </p>' % unicode(node)
    
    def do_emph(self, node):
        """Handle emphasis tags
        
        Arguments:
        - `node`:
        """
        return u'<em>%s</em>' % unicode(node)

    def do_verb(self, node):
        """Handle verbatim elements
        
        Arguments:
        - `node`:
        """
        return u'<tt>%s</tt>' % unicode(node)

    def do_verbatim(self, node):
        """Render the verbatim environment
        
        Arguments:
        - `node`:
        """
        return u'<pre>%s</pre>' % unicode(node)

    def do_noindent(self, node):
        """Stub to skip rendering
        
        Arguments:
        - `node`:
        """
        return u''


    def do_lstlisting(self, node):
        """Encode Source code blocks
        
        Arguments:
        - `node`:
        """
        return u'[sourcecode language=Python]%s[/sourcecode]' % unicode(node)


    def do_includegraphics(self, node):
        """Process images
        
        Arguments:
        - `node`:
        """
        try:
            # Hopefully we have found a url for this guy when the post is rendered
            return u'<a href="%s"><img src="%s" /></a>' % (node.attributes['url'], node.attributes['url'])
        except KeyError:
            # Otherwise put the file name, which will probably give us a broken link
            return u'<img src="%s" />' % node.attributes['file']

    def do_href(self, node):
        """Render a link
        
        Arguments:
        - `node`:
        """
        return u'<a href="%s">%s</a>' % (node.attributes['url'], node.textContent)

    def do_maketitle(self, node):
        """Render the maketitle command
        
        Arguments:
        - `node`:
        """
        # We don't want anything here
        return u''

    def do__superscript(self, node):
        return u'^{%s}' % unicode(node)
    
    def do__subscript(self, node):
        return u'_{%s}' % unicode(node)

    def do__dollar(self, node):
        """Process latex symbol $
        
        Arguments:
        - `node`:
        """
        return u'$'
