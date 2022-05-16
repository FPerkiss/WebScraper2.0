# Import stuff to make it all work! [Libraries]
import warnings
import requests as r
from bs4 import BeautifulSoup
import pandas as pd
from numpy import random  # Adding sleep (prevent DDOS)
from time import sleep  # Adding sleep (prevent DDOS)

# Store the data we want [Location, price, property type, property ID] after scraping/
warnings.filterwarnings("ignore")
prop_location = []
prop_price = []
prop_type = []
prop_id = []
prop_rooms = []
url_pageNo = 0
prop_NoOfListings = 24
prop_listings = None

# User selected variables [No of bedrooms, property type, location]
userSelected_type = None

# User inputs [They select prop type, location and number of bedrooms.]
property_types = ['detached', 'semi-detached', 'terraced', 'flat', 'bungalow']

# When a place it entered it converts it to a code used on the rightmove website If it does not match then it will trow an error and ask again.
location_codes = {
    "dartford": "5E407",
    "sevenoaks": "5E1191",
    "edenbridge": "5E473",
    "tonbridge": "5E1347",
    "southborough": "5E22619",
    "royal Tonbridge Wells": "5E1366",
    "pembury": "5E19488",
    "snodland": "5E1219",
    "aylesford": "5E73",
    "kings Hill": "5E14082",
    "west Malling": "5E1428",
    "paddock Wood": "5E19244",
    "maidstone": "5E897",
    "bearsted": "5E3129",
    "goudhurst": "5E11023",
    "cranbrook": "5E375",
    "staplehurst": "5E23175",
    "benenden": "5E3294",
    "headcorn": "5E12203",
    "sheerness": "5E1194",
    "minster on Sea": "5E17365",
    "sittingbourne": "5E1211",
    "faversham": "5E507",
    "brogdale": "5E77663",
    "lenham": "5E14903",
    "charing": "5E6028",
    "chilham": "5E6240",
    "ashford": "5E57",
    "kingsnorth": "5E14129",
    "woodchurch": "5E27304",
    "lydd": "5E16454",
    "new Romney": "5E975",
    "dymchurch": "5E8795",
    "lympne": "5E16485",
    "whitstable": "5E1447",
    "herne Bay": "5E631",
    "canterbury": "5E279",
    "hythe": "5E672",
    "folkestone": "5E521",
    "hawkinge": "5E12128",
    "aylesham": "5E2569",
    "wingham": "5E27080",
    "birchington": "5E160",
    "minster": "5E17363",
    "sandwich": "5E1173",
    "whitfield": "5E26780",
    "dover": "5E435",
    "deal": "5E413",
    "ramsgate": "5E1111",
    "broadstairs": "5E221",
    "margate": "5E909",
}

panda_location = ""


data = {
        "Location": panda_location,
        "Price": prop_price,
        "Type": userSelected_type,
        "rooms": prop_rooms,
        "Property ID": prop_id,
    }
no_rooms = [1, 2, 3, 4, 5]
url_pageNo = 24
kent_data = pd.DataFrame.from_dict(data)
try:
    for i in location_codes:
        print("---" + i + "---")
        for j in property_types:
            print("---" + j + "---")
            for ii in no_rooms:
                print("--- " + str(ii) + " room ---")
                userSelected_rooms = ii
                while url_pageNo <= 984:
                    # This url is used to get the properties with the parameters we want.
                    URL = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{location_codes[i]}&maxBedrooms={ii}&minBedrooms={ii}&radius=1.0&index={url_pageNo}&propertyTypes={j}&secondaryDisplayPropertyType=detachedshouses&includeSSTC=true&mustHave=&dontShow=&furnishTypes=&keywords="
                    page = r.get(URL)
                    soup = BeautifulSoup(page.content, "html.parser")
                    url_pageNo += 24
                    sleeptime = 0

                    try:
                        prop_NoOfListings = soup.find("span", {"class": "searchHeader-resultCount"})
                        prop_NoOfListings = prop_NoOfListings.get_text()
                        prop_NoOfListings = int(prop_NoOfListings.replace(",", ""))

                        if prop_NoOfListings != 0:
                            prop_search = soup.find(id="propertySearch")
                            container = prop_search.find(id="propertySearch-results-container")
                            search_results = container.find(id="l-searchResults")
                            prop_listings = search_results.find_all('div', class_="l-searchResult is-list")
                            if prop_listings.__len__() != 0:
                                for prop_listing in prop_listings:
                                    soupLocation = prop_listing.find('meta', itemprop="streetAddress")
                                    soupPrice = prop_listing.find("div", class_="propertyCard-priceValue")
                                    soupID = prop_listing.find('a', "propertyCard-anchor", "id")
                                    soupID = soupID.attrs['id']

                                    prop_price.append(soupPrice.text)
                                    prop_id.append(soupID)

                                sleep(sleeptime)
                                placeholder = kent_data.shape[0]
                                for x in prop_id:
                                    y = prop_id.index(x)
                                    new_entry = {"Location": i, "Price": prop_price[y], "Type": j, "rooms": ii, "Property ID": x}
                                    kent_data = kent_data.append(new_entry, ignore_index=True)
                                print(str(kent_data.shape[0]-placeholder) + " entries found")
                                prop_id.clear()
                                prop_price.clear()
                            else:
                                print("no entries")
                                url_pageNo = 24
                                sleep(sleeptime)
                                break
                        else:
                            print("no entries")
                            url_pageNo = 24
                            sleep(sleeptime)
                            break
                    except:
                        break
            url_pageNo = 24
        url_pageNo = 24
except:
    kent_data.to_csv(r"Kent_Test_Data.csv", encoding="utf-8")

print(kent_data)
kent_data.to_csv(r"Kent_Test_Data.csv", encoding="utf-8")
