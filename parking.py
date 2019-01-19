import datetime
import googlemaps
import urllib2

def get_distance_to_garage(api_key, origin, destination, garage_keys):
    gmaps = googlemaps.Client(key = api_key)

    garages = ['UCF Parking Garage {0}'.format(name) for name in garage_keys]

    driving_distances = gmaps.distance_matrix(origin, garages, mode='driving')['rows'][0]['elements']
    driving_durations = [x['duration']['value'] for x in driving_distances]

    walking_distances = gmaps.distance_matrix(garages, destination, mode='walking')['rows']
    walking_durations = [x['elements'][0]['duration']['value'] for x in walking_distances]

    total_durations = [sum(x) for x in zip(driving_durations, walking_durations)]

    return zip(garage_keys, driving_durations, walking_durations, total_durations)

def get_garage_permission(garage_name):
    permit_d = ['A', 'B', 'C', 'D', 'G', 'H', 'I']

    if garage_name in permit_d:
        return 'D'
    else:
        return None

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

        # If the garage has open spots, add its data (as nested dict.) to the main garage dictionary
        if get_garage_permission(garage_name) == 'D' and available_spots > 0:
            garage = {
            'available': available_spots,
            'capacity': total_spots
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

    origin = '1815 S Semoran Blvd, Orlando, FL 32822'
    destination = 'Harris Corporation Engineering Center, Orlando, FL, 32816'

    print('Origin: {0}'.format(origin))
    print('Destination: {0}\n'.format(destination))

    garage_distances = get_distance_to_garage(api_key, origin, destination, garage_data.keys())

    # Add travel durations to garage_data dictionary
    for garage in garage_distances:
        garage_data[garage[0]]['driving_duration'] = garage[1]
        garage_data[garage[0]]['walking_duration'] = garage[2]
        garage_data[garage[0]]['travel_duration'] = garage[1] + garage[2]

    garage_distances.sort(key=lambda tup: tup[3])

    garage = garage_distances[0]

    print('Shortest travel duration:\n')

    print('  Garage {0}\n'.format(garage[0]))
    print('  Travel time: {0}\n'.format(str(datetime.timedelta(seconds=garage[3]))))
    print('    Driving time: {0}'.format(str(datetime.timedelta(seconds=garage[1]))))
    print('    Walking time: {0}\n'.format(str(datetime.timedelta(seconds=garage[2]))))
    print('  Available spaces: {0} of {1}\n\n'.format(garage_data[garage[0]]['available'],
    garage_data[garage[0]]['capacity']))

    print('Other garages:\n')

    for garage in garage_distances[1:]:
        print('  Garage {0}\n'.format(garage[0]))
        print('  Travel time: {0}\n'.format(str(datetime.timedelta(seconds=garage[3]))))
        print('    Driving time: {0}'.format(str(datetime.timedelta(seconds=garage[1]))))
        print('    Walking time: {0}\n'.format(str(datetime.timedelta(seconds=garage[2]))))
        print('  Available spaces: {0} of {1}\n\n'.format(garage_data[garage[0]]['available'],
        garage_data[garage[0]]['capacity']))

if __name__ == '__main__':
    main()
