from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'coin'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/coin'

mongo = PyMongo(app)


# jwt = JWT(app,authenticate,identity) # /auth

# api.add_resource(Item, '/item/<string:symbol>/<string:time_series>')
# api.add_resource(ItemList,'/items')
@app.route('/coins')
def get_all_coins():
    time_series = mongo.db.time_series

    output = []
    for item in time_series.find():
        output.append({'coin_data': item['coin_data']})
    return jsonify({'result': output})


@app.route('/coins/<string:symbol>')
def get_one_coin(symbol):
    time_series = mongo.db.time_series
    coinItem = time_series.find_one({'coin_data.symbol': symbol})
    if coinItem:
        sortdict = [(k, coinItem['time_series'][k])
                    for k in sorted(coinItem['time_series'].keys(), reverse=True)[:7]]
        output = {'name': coinItem['coin_data'],
                  'time_series': sortdict}
    else:
        output = "No such coin."
    return jsonify({'result': output})


@app.route('/coins/<string:symbol>/<int:day>')
def get_one_coin_day(symbol, day):
    time_series = mongo.db.time_series
    coinItem = time_series.find_one({'coin_data.symbol': symbol})
    if coinItem:
        sortdict = [(k, coinItem['time_series'][k])
                    for k in sorted(coinItem['time_series'].keys(), reverse=True)[:day]]
        output = {'name': coinItem['coin_data'],
                  'time_series': sortdict}
    else:
        output = "No such coin."
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
