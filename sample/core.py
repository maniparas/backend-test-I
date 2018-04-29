import tweepy
import re
from docs.conf import consumer_key, consumer_secret, access_token_secret, access_token
from time import sleep

from sample.spreadsheet import GSpreadSheet


def init_configuration():
    """
    This method is used for initial configuration to set up the secure authentication
    :return: AuthHandler
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # For Secured Connection
    auth.secure = True

    return auth


class MyCustomBot(object):
    def __init__(self):
        auth = init_configuration()
        self.api = tweepy.API(auth)

    def find_tweets(self, q='#CongManifestoScam'):
        for tweet in tweepy.Cursor(self.api.search, q=q, lang='en').items(10):
            try:
                username = tweet.user.screen_name
                followers_count = tweet.user.followers_count
                print("Found tweet by: @" + username, followers_count)
            except tweepy.TweepError as e:
                print(e.reason)
                sleep(10)
                continue
            except StopIteration:
                break


class MyCustomBotListener(tweepy.StreamListener):
    def on_error(self, status_code):
        """
        This method would be used to handle any kind of error,
        we can use this method to disconnect the listener if already active
        :param status_code:
        :return:
        """

    def on_status(self, status):
        """
        This method would be used whenever there is a new status from the stream
        we can use this method to perform our action
        :param status:
        :return:
        """
        username = status.user.screen_name
        count_followers = status.user.followers_count

        data_to_write = [username, count_followers]
        spreadsheet = GSpreadSheet()

        file_name = 'TestHashtagBot'
        spreadsheet.write(file=file_name, data_to_write=data_to_write)

        print(f'[*] Profile Name : {username}')
        print(f'[*] Followers Count : {count_followers}')
        if 1000 <= count_followers <= 50000:
            print(f'[*] Matching the followers criteria')
        else:
            print(f'[*] Not matching the followers criteria')
        print('-' * 100)


if __name__ == "__main__":
    text = input(" Enter comma separated hash tags, with hash tag symbol :- ")
    # Find all tags
    tags = re.findall(r"[\w']+", text)
    hash_tags = [tag for tag in tags]
    if hash_tags:
        my_auth = init_configuration()
        stream_listener = MyCustomBotListener()
        stream = tweepy.Stream(my_auth, stream_listener)
        print(f'[-] Following are the hash tags : {hash_tags}')
        print('-' * 80)
        stream.filter(track=hash_tags)


# bot = MyCustomBot()
# sheet = GSpreadSheet()
# bot.find_tweets()
