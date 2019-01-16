import googlemaps

def main():
    # Load Google Maps API key from text file (file not included in Git repository)
    with open('googlemap_key.txt', 'r') as f:
        api_key = f.read()

    gmaps = googlemaps.Client(key = api_key)

    geocode_result = gmaps.geocode('4000 Central Florida Blvd, Orlando, FL 32816')

    print(geocode_result)


if __name__ == '__main__':
    main()
