from flask import Flask
from flask_cors import CORS
import pymongo
import json
from bson import json_util

  
# Connecting to MongoDB 
app = Flask(__name__)
mongo  = pymongo.MongoClient("mongodb+srv://mahmoud:12345678910@cluster0.mgdgq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
  
# Database

Database = mongo.get_database('newspaper')
#select collection
SampleTable = Database.News
  
def tojson(data):
    """convert mongo object to json""""
    return json.dumps(data, default=json_util.default)

@app.route("/news-keywords/<keyword>")
def news_keywords(keyword):
    results = SampleTable.find({'text': {'$regex': '.*' + keyword + '.*'}},{"_id":0})
    json_results = []
    for result in results:
        json_results.append(result)
    return tojson(json_results)


if  __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)
    