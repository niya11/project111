from flask import Flask
from flask import request
import requests
import json
import os


app = Flask(__name__)

@app.route('/')
def load_page():
    return app.send_static_file('index.html')

@app.route('/covid_data', methods=["GET"])

def covid_data():
    county = request.args.get('q')
    json_data = open(os.path.join("static", "fips.json"), "r")
    data = json.load(json_data)
    fips = 0
    for x in data:
        if x["subregion"] == county:
            fips = x["us_county_fips"]

    print(fips)

    headers = {
        'Content-Type': 'application/json'
    }
    key = "914ab4703d294df6a4dc915c93f79b03"
    # req_adr = "https://api.ti73a97ac27b8b2bb6e286ae5eb46a76a1fdc785d"
    req_adr = 'https://api.covidactnow.org/v2/county/' + str(fips) + '.json?apiKey=' + key
    requestResponse = requests.get(req_adr, headers=headers)
    res = requestResponse.json()
    print(res)
    #return(res)

    try:
        risk=res['riskLevels'];
        metrics=res['metrics'];
        actuals=res['actuals']
        tab1 = {
             "county":res["county"],
             "riskLevels" : risk["overall"],
             "newCases": actuals["newCases"],
             "infectionRate": round(float(metrics["infectionRate"]),5),
             "newCasesDensity": (float(actuals["newCases"])/float(res['population'])),
             "Vaccination":round(float(metrics['vaccinationsCompletedRatio']),2)
         }
        print(tab1)
        return json.dumps(tab1)
    except Exception as e:
        raise Exception("Value Error")

# @application.route('/stock_summary', methods=["GET"])
# def stock_summary():
#     keyword_form = request.args.get('q')
#
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     ticker_token = "673a97ac27b8b2bb6e286ae5eb46a76a1fdc785d"
#     req_adr = "https://api.tiingo.com/iex/" + keyword_form + "?token=" + ticker_token
#     requestResponse = requests.get(req_adr, headers=headers)
#     summary = requestResponse.json()
#
#     try:
#         change = summary[0]['last'] - summary[0]['prevClose']
#         change_per = round(((change / summary[0]['prevClose']) * 100), 2)
#
#         arrow = 2
#         if change > 0:
#             arrow = 1
#         elif change < 0:
#             arrow = 0
#
#         change_per = str(change_per) + '%'
#
#         tab2 = {'stock_ticker_sym': summary[0]['ticker'],
#                 'trading_day': summary[0]['timestamp'][0:10],
#                 'previous_closing_price': summary[0]['prevClose'],
#                 'opening_price': summary[0]['open'],
#                 'high_price': summary[0]['high'],
#                 'low_price': summary[0]['low'],
#                 'last_price': summary[0]['last'],
#                 'change': round(change, 2),
#                 'change_percent': change_per,
#                 'no_shares_traded': summary[0]['volume'],
#                 'arrow': arrow
#                 }
#         print(tab2)
#
#         return json.dumps(tab2)
#     except Exception as e:
#         raise Exception("Invalid Value")
#
# @application.route('/charts', methods=["GET"])
# def charts():
#     now = datetime.now()
#     prior_date = now + relativedelta(months=-6)
#     prior_date = prior_date.strftime('%Y-%m-%d')
#     keyword_form = request.args.get('q')
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     ticker_token = "673a97ac27b8b2bb6e286ae5eb46a76a1fdc785d"
#     req_adr = "https://api.tiingo.com/iex/" + keyword_form + "/prices?startDate=" + prior_date \
#               + "&resampleFreq=12hour&columns=open,high,low,close,volume&token=" + ticker_token
#     requestResponse = requests.get(req_adr, headers=headers)
#     data = requestResponse.json()
#
#     try:
#
#         res= {"price":[], "volume":[]}
#
#         for x in data:
#             formatted_date = datetime.fromisoformat(x["date"][:-1])
#             timestamp = datetime.timestamp(formatted_date)
#             res["price"].append([int(timestamp*1000),x["close"]])
#             res["volume"].append([int(timestamp*1000), x["volume"]])
#
#         return json.dumps(res)
#     except Exception as e:
#         raise Exception("Invalid Value")
#
# @application.route('/latest_news', methods=["GET"])
# def latest_news():
#     keyword_form = request.args.get('q')
#
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     ticker_token = "fa2094471d7542528bbe434c36eb50bb"
#     req_adr = "https://newsapi.org/v2/everything?apiKey=" + ticker_token + "&q=" + keyword_form
#     requestResponse = requests.get(req_adr, headers=headers)
#     news = requestResponse.json()
#     try:
#         tab4 = []
#         count = 0
#         for x in news["articles"]:
#             if x["urlToImage"] and x["title"] and x["publishedAt"] and x["url"]:
#                 date = dt.datetime.strptime(str(x["publishedAt"][0:10]), "%Y-%m-%d").strftime("%m/%d/%Y")
#                 if len(x["title"])>105:
#                     x["title"] = x["title"][0:103] + '...'
#                 temp = {
#                     "image": x["urlToImage"],
#                     "title": x["title"],
#                     "date": date,
#                     "original_post_link": x["url"]
#                 }
#                 tab4.append(temp)
#                 count += 1
#             if count == 5:
#                 break
#
#         return json.dumps(tab4)
#     except Exception as e:
#         raise Exception("Invalid Value")

if __name__ == '__main__':
    app.run()
