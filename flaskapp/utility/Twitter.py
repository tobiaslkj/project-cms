import twitter

api = twitter.Api(
    consumer_key='Dyiafv3GNlGGIlLZ0fqCbUzF5',
    consumer_secret='CLuPZe8Soh6f8HwvUqa0SdmT7B6tKkRCUURTEoL5LghXXpg2Ch',
    access_token_key='1105744338565263360-nKbOjXHmmTwBDUlFUsTGWp3rUb1ymY',
    access_token_secret='1PAWKCy7kOgNCNTDt657YRRA2v45oLRrQa1aV56GsWaDX')



def postToTwitter(message):
    status = api.PostUpdate(message)
