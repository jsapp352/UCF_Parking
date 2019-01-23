import datetime
import googlemaps
import urllib2

def get_travel_times(api_key, origin, destination, garage_data):
    gmaps = googlemaps.Client(key = api_key)
    garage_keys = garage_data.keys()
    garages = ['UCF Parking Garage {0}'.format(name) for name in garage_keys]

    # There may be a better way to extract travel durations from the distance matrices
    driving_distances = gmaps.distance_matrix(origin, garages, mode='driving',
    departure_time='now')['rows'][0]['elements']

    driving_durations = [x['duration_in_traffic']['value'] for x in driving_distances]

    walking_distances = gmaps.distance_matrix(garages, destination, mode='walking')['rows']
    walking_durations = [x['elements'][0]['duration']['value'] for x in walking_distances]

    total_durations = [sum(x) for x in zip(driving_durations, walking_durations)]

    garage_distances = zip(garage_keys, driving_durations, walking_durations, total_durations)

    # Add travel durations to garage_data dictionary
    for garage in garage_distances:
        garage_data[garage[0]]['driving_duration'] = garage[1]
        garage_data[garage[0]]['walking_duration'] = garage[2]
        garage_data[garage[0]]['travel_duration'] = garage[1] + garage[2]

    # Sort garages by total travel duration
    garage_distances.sort(key=lambda tup: tup[3])

    # Return list of garage dictionary keys sorted by travel time
    return [garage[0] for garage in garage_distances]

def has_garage_permission(garage_name):
    permit_d = ['A', 'B', 'C', 'D', 'G', 'H', 'I']

    return garage_name in permit_d

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

        # If the garage has open spots and the correct parking permit type,
        # add its data (as nested dict.) to the main garage dictionary
        if has_garage_permission(garage_name) and available_spots > 0:
            garage = {
            'available': available_spots,
            'capacity': total_spots
            }

            garage_data[garage_name] = garage

    return garage_data

def main():
    api_key_filename = 'googlemap_key.txt'
    garage_data_url = 'http://secure.parking.ucf.edu/GarageCount/'

    origin = '1815 S Semoran Blvd, Orlando, FL 32822'
    destination = 'Harris Corporation Engineering Center, Orlando, FL, 32816'

    # Print the intended origin and destination locations
    print('Origin: {0}'.format(origin))
    print('Destination: {0}\n'.format(destination))

    # Load Google Maps API key from text file (file not included in Git repository)
    with open(api_key_filename, 'r') as f:
        api_key = f.read()

    # Retrieve garage availability data from UCF Parking Services
    garage_data = get_garage_data(garage_data_url)

    # Use Google Maps API to find driving/walking times for each garage
    sorted_garage_keys = get_travel_times(api_key, origin, destination, garage_data)

    # Print final results
    print('Garages listed by total travel time:\n')
    for garage in sorted_garage_keys:
        g = garage_data[garage]

        travel_time = str(datetime.timedelta(seconds = g['travel_duration']))
        driving_time = str(datetime.timedelta(seconds = g['driving_duration']))
        walking_time = str(datetime.timedelta(seconds = g['walking_duration']))

        print('  Garage {0}\n'.format(garage))
        print('  Travel time: {0}\n'.format(travel_time))
        print('    Driving time: {0}'.format(driving_time))
        print('    Walking time: {0}\n'.format(walking_time))
        print('  Available spaces: {0} of {1}\n\n'.format(g['available'], g['capacity']))

if __name__ == '__main__':
    main()
