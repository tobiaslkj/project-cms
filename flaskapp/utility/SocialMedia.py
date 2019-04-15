import twitter
import facebook

def postToSocialMedia(message, option):
    smList = []
    if option == 1:
        smList.append(TwitterPlatform())
    elif option == 2:
        smList.append(FacebookPlatform())
    elif option == 3:
        smList.append(TwitterPlatform())
        smList.append(FacebookPlatform())
    else:
        raise AttributeError()
    
    for sm in smList:
        sm.postToPlatform(message)



class SocialMediaPlatform():
    def postToPlatform(message):
        pass


class TwitterPlatform(SocialMediaPlatform):
    def __init__(self, *args, **kwargs):
        self.api = twitter.Api(
        consumer_key='Dyiafv3GNlGGIlLZ0fqCbUzF5',
        consumer_secret='CLuPZe8Soh6f8HwvUqa0SdmT7B6tKkRCUURTEoL5LghXXpg2Ch',
        access_token_key='1105744338565263360-nKbOjXHmmTwBDUlFUsTGWp3rUb1ymY',
        access_token_secret='1PAWKCy7kOgNCNTDt657YRRA2v45oLRrQa1aV56GsWaDX')
        return super().__init__(*args, **kwargs)
    
    def postToPlatform(self,message):
        status = self.api.PostUpdate(message)

class FacebookPlatform(SocialMediaPlatform):
    def __init__(self, *args, **kwargs):
        self.token = {"EAAeh4hKwY8EBAMZBwuAqQINpe6Vi9opQJUYUEGe4wt5QSigO96AkoTAFjzSMKVkrbyIeZCe4PgrHhn1Oh7hZCUtPIeX50ziVZCFfUdqn1fyx9q9wvIZCRsDf1Y206LCRSBtkD2bZBZCKePip18c9u64ZB6UAY6vBVnTfLZC9HQNfseACnrs2YzZBtTSmV6Dj41G9EZD"}
        self.graph = facebook.GraphAPI(self.token)
        return super().__init__(*args, **kwargs)

    def postToPlatform(self,message):
        self.graph.put_object(parent_object='me', connection_name='feed',message=message)