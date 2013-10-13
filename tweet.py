import webapp2
import urllib
import tweepy
import random
import time

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
            text = 'As of {} GMT, {}'.format(time.strftime('%x, %H:%M'), random.choice(no_responses))
        else:
            text = 'As of {} GMT, {}'.format(time.strftime('%x, %H:%M'), random.choice(yes_responses))

        api.update_status(text)
        self.response.write('hai there<br>I just tweeted {}'.format(text))

app = webapp2.WSGIApplication([
    ('/tweet', TweetHandler),
], debug=True)