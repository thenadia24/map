# map
1. def process_data_line_row(data_str): this function returns the list with the year, coordinates and title of the movie.
2. def process_locations_list(path_to_locations_list): this function returns the list of previous lists.
3. def generate_map(dataset): this function accepts a list of lists in the form.
[year, coordinates, movie title].Creates a folium map, overcomes a layer with tooltips (which is built from dataset).
Then adds this loyer, and in addition some default Layer control.
Then saves the map in Map.html locally.
The function returns the folium object.
4. def get_coordinates(address): this function returns latitude and longitud.
5. def calculate_distance(user_coords, place_coords): this function returns distsnce between two tuples of coordinates.
6. def create_map(data, map_name): this function creates a map.
