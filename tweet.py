import webapp2
import urllib
import random
import tweepy

def govt_open():
	u = urllib.urlopen('http://isthegovernmentopenyet.com').read()
	return not 'Nope' in u

no_responses = ['Nope', 'Nah', 'Not yet...', 'No.', 'Negatory']

class TweetHandler(webapp2.RequestHandler):
	def get(self):
		auth = tweepy.OAuthHandler('consumer-key', 'consumer-secret')
		auth.set_access_token('access-key', 'access-secret') 
		api = tweepy.API(auth)

		if not govt_open():
			text = random.choice(no_responses)
		else:
			text = 'YES!'

		api.update_status(text)
		self.response.write('hai there<br>I just tweeted {}'.format(text))

app = webapp2.WSGIApplication([
    ('/tweet', TweetHandler),
], debug=True)