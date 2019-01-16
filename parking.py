
def main():
    # Load Google Maps API key from text file (file not included in Git repository)
    with open('googlemap_key.txt', 'r') as f:
        api_key = f.read()

    #DEBUG
    print(api_key)

if __name__ == '__main__':
    main()
