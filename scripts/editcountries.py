import json
import os.path
import wget
import csv
import os
import time

with open("../QuizPersistent/countries_info.json", "r") as file:
    COUNTRIES = json.load(file)

with open("countries_info2.json", "w") as file:
    i = 0

    country_list = []
    for country in COUNTRIES:
        i = i + 1
        country_stripped = {}
        country_stripped["name"] = {}
        country_stripped["name"]["common"] = country["name"]["common"]
        country_stripped["name"]["official"] = country["name"]["official"]
        country_stripped["capital"] = country["capital"]
        country_stripped["region"] = country["region"]
        country_stripped["subregion"] = country["subregion"]
        country_stripped["id"] = i
        print(f'../QuizPersistent/flags/{country["name"]["common"]}.png')
        if os.path.isfile(f'../QuizPersistent/flags/{country["name"]["common"]}.png'):
            print (f'{country["name"]["common"]}.png exists')
            country_stripped["flag"] = f'{country["name"]["common"]}.png'


        csvFile = csv.reader(open('../QuizPersistent/LatLong.csv'), delimiter=',')
        for line in csvFile:
            country = line[0]
            code = line[1]
            lat = line[2]
            longi = line[3]
            if(country == country_stripped["name"]["common"] or country == country_stripped["name"]["official"]):
                country_stripped["code"] = code
                country_stripped["lat"] = lat
                country_stripped["long"] = longi
                break

        country_list.append(country_stripped)

    json.dump(country_list, file, indent=4)