import googlemaps
import urllib2

#DEBUG
import pprint

def get_distance_to_garage(api_key, origin, destination, garage_data):
    gmaps = googlemaps.Client(key = api_key)

    garage_keys = garage_data.keys()

    garages = ['UCF Parking Garage {0}'.format(name) for name in garage_keys]

    driving_distance_matrix = gmaps.distance_matrix(origin, garages, mode='driving')
    driving_distances = driving_distance_matrix['rows'][0]['elements']
    driving_durations = [x['duration']['value'] for x in driving_distances]

    walking_distance_matrix = gmaps.distance_matrix(garages, destination, mode='walking')
    walking_distances = walking_distance_matrix['rows']
    walking_durations = [x['elements'][0]['duration']['value'] for x in walking_distances]

    # driving_distances = [driving_distance_matrix['rows']['elements'][i]['duration']['value']
    pprint.pprint(driving_durations)
    pprint.pprint(walking_durations)

    return zip(garage_keys, [sum(x) for x in zip(driving_durations, walking_durations)])

def get_garage_permission(garage_name):
    permit_d = ['A', 'B', 'C', 'D', 'G', 'H', 'I']

    if garage_name in permit_d:
        return 'D'
    else:
        return None

def get_garage_coordinates(garage_name):
    garage_coords = {
    'A': (28.600174, -81.205645),
    'B': (28.597147, -81.200374),
    'C': (28.602579, -81.195876),
    'D': (28.605202, -81.197227),
    'H': (28.605314, -81.201248),
    'I': (28.601409, -81.204942)
    }

    # Return the garage coordinated if they are known. Otherwise, return None.
    return garage_coords.get(garage_name, None)

def get_garage_data(garage_url):
    # Create an empty dictionary to hold garage data
    garage_data = dict()

    # Get UCF Garage Availability HTML file from website
    garage_html = urllib2.urlopen(garage_url).read()

    # Parse HTML file sequentially to find availability/capacity for each garage
    search = garage_html.partition('DataRow_DevEx')[2].partition('Garage ')[2].partition('</td>')
    while search[2] != '':
        garage_name = search[0]
        search = search[2].partition('<strong>')[2].partition('</strong>/')

        available_spots = int(search[0])
        search = search[2].partition('</td>')

        total_spots = int(search[0].rstrip())
        search = search[2].partition('DataRow_DevEx')[2].partition('Garage ')[2].partition('</td>')

        #DEBUG
        print('Garage {0}: {1} / {2} spaces free'.format(garage_name, available_spots, total_spots))

        # If the garage has open spots, add its data (as nested dict.) to the main garage dictionary
        if get_garage_permission(garage_name) == 'D' and available_spots > 0:
            garage = {
            'available': available_spots,
            'capacity': total_spots,
            'coordinates': get_garage_coordinates(garage_name)
            }

            garage_data[garage_name] = garage

    return garage_data

def main():
    api_key_filename = 'googlemap_key.txt'
    garage_data_url = 'http://secure.parking.ucf.edu/GarageCount/'

    # Load Google Maps API key from text file (file not included in Git repository)
    with open(api_key_filename, 'r') as f:
        api_key = f.read()

    garage_data = get_garage_data(garage_data_url)

    print(garage_data)

    origin = '1815 S Semoran Blvd, Orlando, FL 32822'
    destination = 'Harris Corporation Engineering Center, Orlando, FL, 32816'

    garage_distances = get_distance_to_garage(api_key, origin, destination, garage_data)

    print(garage_distances)

if __name__ == '__main__':
    main()
