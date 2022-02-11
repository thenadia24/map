from hashlib import new
from numpy import sort
import folium
from geopy.geocoders import Nominatim
import os
import re
import sys
from geopy.distance import vincenty

import urllib.parse
import requests


def process_data_line_row(data_str):
    """

    :param data_str:
    :return: the list with the year, coordinates and title of the movie
    """
    year = re.findall(r"(\d{4})", data_str)[0]
    film_name = data_str.split("\"")[1]
    # print(data_str.split("\""))
    location_name = data_str.split("\t")[-1]
    coords = get_coordinates(location_name)
    if not coords:
        return False
    return [year, coords, film_name]


# get dataset
def process_locations_list(path_to_locations_list):
    """

    :param path_to_locations_list:
    :return: the list of previous lists.
    """
    with open(path_to_locations_list, 'r') as f:
        data = f.read().split("\n")[20:50]
    res = []
    for r in data:
        new_row = process_data_line_row(r)
        if new_row:
            res.append(new_row)
    return res


def generate_map(dataset):
    """
     this function accepts a list of lists in the form.
     [year, coordinates, movie title].
     Creates a folium map, overcomes a layer with tooltips (which is built from dataset).
    Then adds this loyer, and in addition some default Layer control.
    Then saves the map in Map.html locally. The function returns the folium object.
    """
    map = folium.Map()
    name_layer = folium.FeatureGroup(name="name's layer")
    for row in dataset:
        name_layer.add_child(folium.Marker(location=row[1],
                                           tooltip=row[2]))
    map.add_child(name_layer)
    map.add_child(folium.LayerControl())
    map.save('Map.html')

    print('Saved map in Map.html')
    return map


def get_coordinates(address):
    """

    :param address:
    :return:latitude and longitud
    """
    geolocator = Nominatim(user_agent="Lakoma", timeout=5)
    location = geolocator.geocode(address)
    if not location:
        return
    return location.latitude, location.longitude


    # calculate_distance(user_coords, place_coords):
    # calculate Hoversin distance between user coords (lat, long)
    #geopy.distance.vincenty(location1, location2).km
    #return 5


def create_map(data, map_name):
    """
    creates a map
    """
    data = get_coordinates(data)
    generate_map(data, map_name)


def main(year, lat, long, path):
    dataset = process_locations_list(path)  # year, (lat, long), film_name
    user_coords = (lat, long)
    year = str(year)
    # filter by year
    dataset = [d for d in dataset if str(d[0]) == year]
    # get 10 closest locations
    for i in range(len(dataset)):
        dataset[i].append(calculate_distance(user_coords, dataset[i][1]))

    dataset = sorted(dataset, key=lambda x: x[-1])[:10]
    # create a map from 10 closest locations
    generate_map(dataset)


if __name__ == "__main__":
    # read sys arguments and launch program
    main(*sys.argv[1:])
