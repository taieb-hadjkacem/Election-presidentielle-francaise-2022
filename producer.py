

"""API ACCESS KEYS"""
access_token = "1464352002264412161-I28HQtehAqVGFMWy8NyNDm4jy7Yg3q"
access_token_secret =  "yopiwM0w0jmbDejOB55eCPQbfZlHH8HWRKFm4oesMYuzT"
consumer_key =  "xRvPjnSV3oGSmjL4eHo4ZV3aQ"
consumer_secret =  "4P17sSWoOndGVYqob7Cy4kbBSaYizbVraQ5QsWvZjN5mNOCGWZ"

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')


topic_name = "election"


class twitterAuth():
    def authenticateTwitterApp(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        return auth



class TwitterStreamer():

    def __init__(self):
        self.twitterAuth = twitterAuth()

    def stream_tweets(self):
        while True:
            listener = ListenerTS() 
            auth = self.twitterAuth.authenticateTwitterApp()
            stream = Stream(auth, listener)
            stream.filter(track=['#Zemmour','#Zemmour2022','#z0zz','#ZemmourEric','#ZemmourPrésident','#ZemmourCandidat','#EricZemmour','#Macron','#EmmanuelMacron','#Emmanuel_Macron','#Macron2022','#LePen','#MarineLePen','#Marine2022','#MarinePréseidente','#MLaFrance','#pécresse','#pécresse2022','#Valérie Pécresse'], stall_warnings=True, languages= ["fr"])


class ListenerTS(StreamListener):

    def on_data(self, raw_data):
        producer.send(topic_name, str.encode(raw_data))
        return True


if __name__ == "__main__":
    
    TS = TwitterStreamer()
    TS.stream_tweets()
