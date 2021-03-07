from amadeus import Client, ResponseError
def activities():
    
    
    amadeus = Client(
        client_id='iwXFJ4yQ6bXt798xi8uNbZqzpfN9sTOA',
        client_secret='RIXEsYiYasLu9CHI'
    )

    try:
        response = amadeus.shopping.activities.get(
            #We can get lat/long from the covid data but I'm not sure how to save data between functions in this case
            latitude = '37.7', 
            longitude = '122.4',
            radius = '10')
        print(response.data)
    except ResponseError as error:
        print(error)
        
    res = response.result['data'][0]
    #the [0] gives the first activity. We could give a random one, or show more than one idk

    try:
        image = res['pictures']
        tab1 = {
             "name":res['name'],
             "description" : res["shortDescription"],
             "rating": res["rating"],
             "price": res['price']
         }
        print(tab1)
        return json.dumps(tab1)
    except Exception as e:
        print(res)
        raise Exception("Value Error")
    
if __name__ == '__main__':
    app.run()