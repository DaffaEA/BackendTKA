# sentiment_analysis.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Database setup
client = MongoClient('mongodb+srv://doadmin:7A132aq95tnE8To6@db-mongodb-sgp1-94371-434492d4.mongo.ondigitalocean.com/sentiment_analysis?tls=true&authSource=admin&replicaSet=db-mongodb-sgp1-94371')
db = client.sentiment_analysis
collection = db.history

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get('text', '')
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity

    # Save to database
    collection.insert_one({'text': text, 'sentiment': sentiment})

    return jsonify({'sentiment': sentiment})

@app.route('/history', methods=['GET'])
def get_history():
    history = list(collection.find({},{'_id':0}).sort("_id",-1))
    return jsonify(history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
