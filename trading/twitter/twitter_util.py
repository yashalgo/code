# File: twitter_util.py
import tweepy
import json
from ..common.config import *


class Twitter:
    def __init__(self):
        with open(cred_twitter, "r") as f:
            data = json.load(f)

        # get API
        auth = tweepy.OAuthHandler(data["api_key"], data["api_secret"])
        auth.set_access_token(data["access_token"], data["access_token_secret"])
        self.api = tweepy.API(auth)

        # get Client
        client = tweepy.Client(
            bearer_token=data["bearer_token"],
            consumer_key=data["api_key"],
            consumer_secret=data["api_secret"],
            access_token=data["access_token"],
            access_token_secret=data["access_token_secret"],
        )
        self.client = client

        # verify API
        if self.api.verify_credentials():
            print("API authentication successful.")
        else:
            print("API authentication failed.")

    def tweet(self, message, image_path=None):
        print("TWEET: ", message)
        if image_path is not None:
            print(image_path)
            media = self.api.media_upload(filename=image_path)
            print("MEDIA: ", media)
            # tweet = self.api.update_status(
            #     status=message, media_ids=[media.media_id_string]
            # )
            tweet = self.client.create_tweet(
                text=message, media_ids=[media.media_id_string]
            )
        else:
            tweet = self.client.create_tweet(text=message)
        return tweet
