'''

  wp.py - Wordpress Posting Classes

  (c) 2010 Eric Finster

'''

from renderer import WPRenderer

from plasTeX.TeX import TeX

from wordpresslib import WordPressPost
from wordpresslib import WordPressClient

def findImageNodes(node):
    """Recursively find subnodes which are image inclusions
    
    Arguments:
    - `node`:
    """
    # I don't think this guy will have any important subnodes . . .
    if node.nodeName == 'includegraphics':
        return [node]

    img_nds = []
    for n in node.childNodes:
        img_nds += findImageNodes(n)

    return img_nds

class WordPressLatexPost(WordPressPost):
    """Encapsulate a LaTeX Post to Wordpress
    """
    
    def __init__(self, latex):
        """
        
        Arguments:
        - `latex`:
        """
        WordPressPost.__init__(self)

        self._tex = TeX()
        self._renderer = WPRenderer()

        self._tex.input(latex)
        self._document = self._tex.parse()

        # Before rendering, let's pass through and extract the images
        self.images = findImageNodes(self._document)
        
    def render(self):
        """Render this post
        """
        # Have to encode the unicode string to print it correctly.
        self.description = self._renderer.render(self._document).encode('utf-8')
        self.title = self._document.userdata['title'].textContent.encode('utf-8')
        self.tags = self._document.userdata['tags'].textContent.encode('utf-8')

        #I don't know much about categories yet . . .
        #self.category = [document.userdata['category'].textContent.encode('utf-8')]

class WordPressLatexClient(WordPressClient):
    """Override the post method to provide tags, etc.
    """
    
    def newPost(self, post, publish):
        """Make a LaTeX post
        
        Arguments:
        - `post`:
        - `publish`:
        """
        #
        #  The post will not be rendered yet.  We need to post all the images first, and then
        #  render with the correct references.  Let's see if we can do that now.
        #

        for img in post.images:
            img_url = self.newMediaObject(str(img.attributes['file']))
            print "Adding new media object at: " + str(img_url)

            # Now set some tag so that we can remember later
            img.attributes['url'] = img_url
        
        #
        #  With the images taken care of, we're ready to render the post
        #

        post.render()

        blogContent = {
            'title' : post.title,
            'description' : post.description,
            'mt_keywords' : post.tags
            }
		
        # add categories
        i = 0
        categories = []
        for cat in post.categories:
            if i == 0:
                categories.append({'categoryId' : cat, 'isPrimary' : 1})
            else:
                categories.append({'categoryId' : cat, 'isPrimary' : 0})
            i += 1
		
        # insert new post
        idNewPost = int(self._server.metaWeblog.newPost(self.blogId, self.user, self.password, blogContent, 0))
		
        # set categories for new post
        self.setPostCategories(idNewPost, categories)
		
        # publish post if publish set at True 
        if publish:
            self.publishPost(idNewPost)
			
        return idNewPost
