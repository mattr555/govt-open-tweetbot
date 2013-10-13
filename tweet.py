import webapp2
import urllib
import tweepy
from google.appengine.api import memcache

def govt_open():
    u = urllib.urlopen('http://isthegovernmentopenyet.com').read()
    return not 'Nope' in u

no_responses = ['Nope', 'Nah', 'Not yet...', 'No.', 'Negatory']
yes_responses = ['YES!', 'Yup!', 'yeah', 'affirmative', 'Indeed', 'yessir', 'uh-huh']

class TweetHandler(webapp2.RequestHandler):
    def get(self):
        auth = tweepy.OAuthHandler('consumer-key', 'consumer-secret')
        auth.set_access_token('access-key', 'access-secret') 
        api = tweepy.API(auth)

        if not govt_open():
            c = memcache.get('next_no_response')
            if c is None:
                c = 0
            text = no_responses[c % len(no_responses)]
            c += 1
            memcache.set('next_no_response', c)
        else:
            c = memcache.get('next_yes_response')
            if c is None:
                c = 0
            text = yes_responses[c % len(yes_responses)]
            c += 1
            memcache.set('next_yes_response', c)

        api.update_status(text)
        self.response.write('hai there<br>I just tweeted {}'.format(text))

app = webapp2.WSGIApplication([
    ('/tweet', TweetHandler),
], debug=True)