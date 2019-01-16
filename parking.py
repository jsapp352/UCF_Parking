import googlemaps
import urllib2

def access_gmap(api_key):
    gmaps = googlemaps.Client(key = api_key)

    geocode_result = gmaps.geocode('4000 Central Florida Blvd, Orlando, FL 32816')

    print(geocode_result)

def get_garage_data(garage_url):
    response = urllib2.urlopen(garage_url)

    garage_html = response.read()

    search = garage_html.partition('DataRow_DevEx')[2].partition('Garage ')[2].partition('</td>')

    while search[2] != '':

        garage_name = search[0]

        search = search[2].partition('<strong>')[2].partition('</strong>/')

        available_spots = search[0]

        search = search[2].partition('</td>')

        total_spots = search[0].rstrip()

        print('Garage {0}: {1} / {2} spaces free'.format(garage_name, available_spots, total_spots))

        search = search[2].partition('DataRow_DevEx')[2].partition('Garage ')[2].partition('</td>')

def main():
    api_key_filename = 'googlemap_key.txt'
    garage_data_url = 'http://secure.parking.ucf.edu/GarageCount/'

    # Load Google Maps API key from text file (file not included in Git repository)
    with open(api_key_filename, 'r') as f:
        api_key = f.read()

    get_garage_data(garage_data_url)

if __name__ == '__main__':
    main()
