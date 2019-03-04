import googlemaps
import json

# Build a list of buildings on UCF campus from a text table that was copy/pasted form UCF website
def make_building_list(filename):
    with open(filename, 'r') as f:
        building_data = f.readlines()

        buildings = {}

        # Parse building data
        for line in building_data:
            building = dict();

            line = line.partition('\t')

            building['abbr'] = line[0]

            line = line[2].partition('\t')

            building['name'] = line[0].partition('(')[0].strip()

            building['id'] = line[2].strip()

            buildings[building['id']] = building

        return buildings

# For each building in the list, add walking times from each parking garage using
# Google Maps API
def add_garage_walk_times(api_key, buildings, garages):
    gmaps = googlemaps.Client(key = api_key)

    garage_names = [('UCF Parking Garage ' + name + ', Orlando, FL, 32816') for name in garages]

    for k in buildings.keys():
        building = buildings[k]
        walking_distances = gmaps.distance_matrix(garage_names, (building['name']+', Orlando, FL, 32816'), mode='walking')['rows']

        try:
            walking_durations = [x['elements'][0]['duration']['value'] for x in walking_distances]
        except:
            print('Error fetching walk times for ' + building['name'] + '.\n')
            continue

        garage_walk_durations = zip(garages, walking_durations)

        garage_walk_durations.sort(key=lambda tup: tup[1])

        buildings[k]['garage_walk_durations'] = [{'name':g[0], 'walk_duration':g[1]} for g in garage_walk_durations]

    return buildings

# A Google Maps Distance Matrix API key is needed in order to run this script. The key is stored
# in the text file indicated by "api_key_filename"
def main():
    api_key_filename = 'googlemap_key.txt'
    building_list_file = 'ucf_building_list.txt'
    json_filename = 'building_data.json'

    # Load Google Maps API key from text file (file not included in Git repository)
    with open(api_key_filename, 'r') as f:
        api_key = f.read()

    garages = ['A', 'B', 'C', 'D', 'G', 'H', 'I', 'Libra']

    buildings = make_building_list(building_list_file)

    buildings = add_garage_walk_times(api_key, buildings, garages)

    with open(json_filename, 'w') as out:
        json.dump(buildings, out)

if __name__ == '__main__':
    main()
