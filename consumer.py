from kafka import KafkaConsumer
import json
from elasticsearch import Elasticsearch
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


from pandas import json_normalize
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import *
from pyspark.sql import functions as F

from fuzzywuzzy import fuzz
import statistics

nltk.download('vader_lexicon')
es = Elasticsearch()

def Myfuzz(a,b):
    return fuzz.ratio(a,b)

def blob_sentiment(text):
    tweet_blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
   
    polarity = tweet_blob.sentiment[0]
    #print("blobed twee: \n " , tweet_blob)
    if polarity > 0:
        blob_sentiment = "Positive"
    elif polarity < 0:
        blob_sentiment = "Negative"
    else:
        blob_sentiment = "Neutral" 

    return blob_sentiment  

        
         
def main():
    # set-up a Kafka consumer
    consumer = KafkaConsumer("election")
    for msg in consumer:

        dict_data = json.loads(msg.value)
        a=dict_data['entities']['hashtags']
        hashtags=[]
        for i in range(len(a)):
            hashtag=a[i]['text']
            hashtags.append(hashtag)

        data={}
        data['hashtags']=hashtags
        data['name_user']=dict_data["user"]["screen_name"]
        data['created_at']=dict_data["created_at"]  
        data['tweet']=dict_data["text"] 
        
        if (len(dict_data['entities']['hashtags'])==0):
            continue
            
        print("original tweet:\n" +   dict_data["text"] )

        Macron=statistics.mean([Myfuzz("Macron",i) for i in hashtags])
        Pecresse=statistics.mean([Myfuzz("Pecresse",i) for i in hashtags])
        Marine=statistics.mean([Myfuzz("MarineLePen",i) for i in hashtags])
        Zemmour=statistics.mean([Myfuzz("Zemmour",i) for i in hashtags])
        
        liste=[Macron,Pecresse,Marine,Zemmour]
        name_prezs=["Macron","Pecresse","Marine","Zemmour"]
        
        if (max(liste)>50):
            name_prez=name_prezs[liste.index(max(liste))]
        else:
            continue    
     
        data['president']=name_prez

        data_str = json_normalize(data).to_json(orient="records") 
        spark = SparkSession.builder.appName('test').getOrCreate()
        rows_list = [data_str]
        rdd = spark.sparkContext.parallelize(rows_list)
        df = spark.read.json(rdd)
        # tweets cleaning
        df = df.withColumn('tweet', F.regexp_replace('tweet', r'http\S+', ''))
        df = df.withColumn('tweet', F.regexp_replace('tweet', '@\w+', ''))
        df = df.withColumn('tweet', F.regexp_replace('tweet', '#', ''))
        df = df.withColumn('tweet', F.regexp_replace('tweet', 'RT', ''))
        df = df.withColumn('tweet', F.regexp_replace('tweet', ':', ''))

        #print("cleaned tweet:\n ", df.collect()[0]["tweet"])

        blob_sentiment_udf = udf(blob_sentiment, StringType())
        df = df.withColumn("blob_sentiment", blob_sentiment_udf("tweet"))
      
        
        print()
        print("Blob Sentiment: ", df.collect()[0]["blob_sentiment"])
        print()

        # add text and sentiment info to elasticsearch
        es.index(index="electionsfrance",
                 doc_type="test-type",
                 body={"author": dict_data["user"]["screen_name"],
                       "date": dict_data["created_at"],
                       "message": dict_data["text"],
                       "president": name_prez,
                       "blob_sentiment": df.collect()[0]["blob_sentiment"]})
 

if __name__ == "__main__":
    main()
