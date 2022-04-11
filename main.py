# Import stuff to make it all work! [Libraries]
import requests as r
from bs4 import BeautifulSoup
import pandas as pd
from numpy import random  # Adding sleep (prevent DDOS)
from time import sleep  # Adding sleep (prevent DDOS)

# Store the data we want [Location, price, property type, property ID] after scraping/
prop_location = []
prop_price = []
prop_type = []
prop_id = []
prop_rooms = []
url_pageNo = 0
prop_NoOfListings = None
prop_listings = None
prop_added = 0
prop_tempCount = 0

# User selected variables [No of bedrooms, property type, location]
userSelected_rooms = None
userSelected_type = None
UserSelected_location = None

# User inputs [They select prop type, location and number of bedrooms.]
print("Please type one of the following 'detached', 'semi-detached', 'terraced', 'flat', 'bungalow', 'park-home':")
userSelected_type = input()
userSelected_rooms = int(input("Please enter the amount of bedrooms you have: "))

# When a place it entered it converts it to a code used on the rightmove website If it does not match then it will trow an error and ask again.
location_codes = {
    "kent": "5E61307",
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
locationTrue = 0
while locationTrue == 0:
    userSelected_location = input("Please enter location: ").lower()
    panda_location = userSelected_location
    if userSelected_location in location_codes:
        userSelected_location = location_codes[userSelected_location]
        locationTrue = 1
    else:
        print("Please try a different location.")

def urlReload():
    global url_pageNo
    global URL
    global soup
    # This url is used to get the properties with the parameters we want.
    URL = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{userSelected_location}&maxBedrooms={userSelected_rooms}&minBedrooms={userSelected_rooms}&radius=0.0&index={url_pageNo}&propertyTypes={userSelected_type}&secondaryDisplayPropertyType=detachedshouses&includeSSTC=true&mustHave=&dontShow=&furnishTypes=&keywords="
    page = r.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    url_pageNo = url_pageNo + 24


def findAdd():
    try:
        global prop_added
        global prop_tempCount
        global prop_NoOfListings
        # Gets us the number of listings:
        prop_NoOfListings = soup.find("span", {"class": "searchHeader-resultCount"})
        prop_NoOfListings = prop_NoOfListings.get_text()
        prop_NoOfListings = int(prop_NoOfListings.replace(",", ""))
        prop_search = soup.find(id="propertySearch")
        container = prop_search.find(id="propertySearch-results-container")
        search_results = container.find(id="l-searchResults")
        prop_listings = search_results.find_all('div', class_="l-searchResult is-list")

        for prop_listing in prop_listings:
            soupLocation = prop_listing.find('meta', itemprop="streetAddress")
            soupPrice = prop_listing.find("div", class_="propertyCard-priceValue")
            soupID = prop_listing.find('a', "propertyCard-anchor", "id")
            soupID = soupID.attrs['id']

            if soupID not in prop_id:
                prop_location.append(soupLocation['content'])
                prop_price.append(soupPrice.text)
                prop_id.append(soupID)
                prop_rooms.append(userSelected_rooms)
                prop_added = prop_added +1
                prop_tempCount = prop_tempCount +1
            else:
                None
    except:
        exportPanadas()
        print ("Failed (findAdd()) but exported up until failure.")

def exportPanadas():
    # Data export to a .CSV file using the Pandas library.
    data = {
        "Location": panda_location,
        "Price": prop_price,
        "Type": userSelected_type,
        "rooms": prop_rooms,
        "Property ID": prop_id,
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv(rf"{panda_location} - {userSelected_type} - {userSelected_rooms} bed.csv", encoding="utf-8")

urlReload()
findAdd()

def runNow():
    try:
        while prop_added < prop_NoOfListings:
            urlReload()
            findAdd()
            print(f"{prop_added} / {prop_NoOfListings}")
            print (f"url: {url_pageNo}")
            sleeptime = random.uniform(3, 7)
            print("sleeping for:", sleeptime, "seconds")
            sleep(sleeptime)
            print("sleeping is over")
    except:
        exportPanadas()
        print("Failed (while()) but exported up until failure.")
runNow()

exportPanadas()