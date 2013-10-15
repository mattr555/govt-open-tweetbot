import webapp2
import tweepy
import random
import datetime
from main import govt_open

no_responses = ['Nope', 'Nah', 'Not yet...', 'No.', 'Negatory', 'Nada', 'Soon???']
yes_responses = ['YES!', 'Yup!', 'yeah', 'affirmative', 'Indeed', 'yessir', 'uh-huh']

class FixedOffset(datetime.tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self.__offset = datetime.timedelta(minutes = offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return datetime.timedelta(0)

class TweetHandler(webapp2.RequestHandler):
    def get(self):
        auth = tweepy.OAuthHandler('consumer-key', 'consumer-secret')
        auth.set_access_token('access-key', 'access-secret') 
        api = tweepy.API(auth)
        tz = FixedOffset(-240, 'EDT')

        if not govt_open():
            text = 'As of {} EDT, {}'.format(datetime.datetime.now(tz).strftime('%x, %I:%M %p'), random.choice(no_responses))
        else:
            text = 'As of {} EDT, {}'.format(datetime.datetime.now(tz).strftime('%x, %I:%M %p'), random.choice(yes_responses))

        api.update_status(text)
        self.response.write('hai there<br>I just tweeted {}'.format(text))

app = webapp2.WSGIApplication([
    ('/tweet', TweetHandler),
], debug=True)
