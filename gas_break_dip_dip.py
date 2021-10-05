import requests
import json
import pandas as pd

# list of all the dealerships in CA, ID, NV
dealers = ["27020", "27024", "27021", "27022", "04739", "04080", "04159", "04772", "04285", "04102", "04308", "04250",
           "04508", "04649", "04636", "04315", "04033", "04726", "04096", "04748", "04136", "04154", "04303", "04283",
           "04640", "04094", "04309", "04297", "04079", "04211", "04356", "04108", "04013", "04087", "04059", "04109",
           "04247", "04137", "04543", "04284", "04347", "04167", "04638", "04228", "04915", "04554", "04713", "04279",
           "04388", "04737", "04990", "04344", "04061", "04333", "04359", "04263", "04218", "04456", "04180", "04097",
           "04095", "04536", "04353", "04576", "04041", "04278", "04282", "04222", "04819", "04135", "04076", "04786",
           "04150", "04734", "04215", "04676", "04277", "04181", "04273", "04232", "04290", "04140", "04098", "04053",
           "04541", "04056", "04262", "04361", "04221", "04426", "04226", "04412", "04213", "04119", "04454", "04143",
           "04256", "04688", "04104", "04338", "04088", "04317", "04346", "04007", "04660", "04362", "04051", "04022",
           "04563", "04753", "04176", "04122", "04374", "04292", "04169", "04364", "04389", "04201", "04077", "04421",
           "04487", "04682", "04774", "04185", "04265", "04253", "04324", "04017", "04072", "04070", "04039", "04583",
           "04158", "04151", "04288", "04163", "04260", "27016", "04260", "27015", "27013"]
# empty dataframe
truck_df = pd.DataFrame(columns=['dealer', 'msrp_total', 'msrp_base', 'model_title', 'color', 'VIN'])
# for each dealer in the dealer list
for dealer in dealers:
    # json objects to the send to the toyota api
    data = {
      "brand": "TOY",
      "mode": "content",
      "group": True,
      "groupmode": "full",
      "relevancy": False,
      "pagesize": 200,
      "pagestart": 0,
      "filter": {
          "year": [2021],
          "series": ["rav4"],
          "dealers": [dealer],
          "andfields": ["accessory", "packages", "dealer"]
      }
    }
    headers = {'content-type': 'application/json'}
    json_object = json.dumps(data)
    # send POST request with data and headers objects
    r = requests.post("https://www.toyota.com/config/services/inventory/search/getInventory",
                      data=json_object,
                      headers=headers
                      )
    # convert response from POST request to json and query data for array of objects with each individual auto data
    json_response = r.json()
    response_array = json_response["body"]["response"]["docs"]
    # loop through the array all the autos available at the current dealer
    for response in response_array:
        # save selected data to dict
        x = {
            "dealer": [dealer],
            "msrp_total": [response["priceInfo"]["totalMSRP"]],
            "msrp_base": [response["priceInfo"]["totalMSRP"]],
            "model_title": [response["model"]["title"]],
            "color": [response["exteriorcolor"]["title"]],
            "VIN": [response["vin"]]
        }
        # convert dict to dataframe and append to the main dataframe
        df_x = pd.DataFrame.from_dict(x)
        truck_df = truck_df.append(df_x)
# export the main dataframe to a csv file
truck_df.to_csv("scrappers.csv")
