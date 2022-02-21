from flaskfromscratch.database import config
import json
# from flaskfromscratch import db

# db.create_all()

# from main import User, Post


# user_1 = User(username='Corey', email='C@demo.com', password='password')
# user_2 = User(username='John', email='jd@demo.com', password='password')
# db.session.add(user_1)
# db.session.add(user_2)
# db.session.commit()


# User.query.all()



# d.drop_all()

# import twelvedata


# td = twelvedata.TDClient(apikey=config.API_KEY)
# # assets = td.get_stocks_list().as_json()

# crypto_assets = td.get_cryptocurrencies_list().as_json()





# for crpyto in crypto_assets:
#     with open('sample2.txt', 'a') as filehandle:
#         if crpyto['currency_quote'] == 'US Dollar':
#             filehandle.write('%s\n' % crpyto['symbol'])


# lmao = ['0xBTC/BTC',]
# print(type(lmao))
# print(lmao[0].split('/')[0])



lmao = {
        "symbol": "0xBTC/USD",
        "available_exchanges": [
            "Synthetic"
        ],
        "currency_base": "0xBitcoin",
        "currency_quote": "US Dollar"
    }


print(lmao['available_exchanges'][0])




