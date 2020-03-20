import tweepy
import sys
import pymongo


class StreamListener(tweepy.streaming.StreamListener):
    #function to get tweets
    def on_status(self, status):
        try:
            #setting necessary fields
            retweet = False
            tweet = status
            #based upon status
            if hasattr(status, "retweeted_status"):
                retweet = True
                tweet = status.retweeted_status
            if hasattr(status, "extended_text"):
                text = status.extended_tweet["full_text"]
            else:
                text = tweet.text
            #adding tweet details to a dictionary
            tweet = {"_id": tweet.id, 'date': tweet.created_at, 'user_id': tweet.user.screen_name, 'text': text, 'hashtags': tweet.entities['hashtags']}
            #inserting the dictionary in the database
            db.tweet_stream.insert_one(tweet)
        #filtering duplicate tweets
        except pymongo.errors.DuplicateKeyError as e:
            print(e)


    def on_error(self, status_code):
        print("Encountered streaming error (" + status_code + ")")
        sys.exit()


if __name__ == "__main__":
    #necessary credentials
    auth = tweepy.OAuthHandler("MENcB6AF13ZKx50eVb4Rr7Zi0", "uqnwCg9OOtF8IfyTM3DcKdyDCNqj3djXtvdzWF1CDlAXrWhbw7")
    auth.set_access_token("1236635062373953537-mmPJAGvxSxpNWYhPh3LarOZSvFndwe", "qL8KVuhd3gQP8qfl6cXUPJhUZaO5A6cCYx6OTItAUWXaz")
    #using the tweepy api
    api = tweepy.API(auth)
    #running local server to host the database
    client = pymongo.MongoClient('localhost', 27017)
    duplicateChecker = []
    #streaming for tweets
    db = client.twitterStream
    db1 = client.twitterDump
    dbl = client.Logs
    db3 = client.invertedIndex
    #checking whether data is stored correctly by printing items
    for item in db['tweet_stream'].find():
        print(item)
    #setting necessary fields
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')
    tags = ["kerala"]
    stream.filter(track=tags)