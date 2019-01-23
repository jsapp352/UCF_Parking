# UCF_Parking

## About
This program was written by Justin D. Sapp as a proof-of-concept for an application to help students at the University of Central Florida determine which parking garage to choose for the shortest total travel time. It was also created for the purpose of learning about both the Google Maps API and scraping web information using Python.

The program takes the user's location of origin and a destination on or near UCF campus as inputs, and gathers data from web sources to determine:

  - Which parking garages have available parking places (from UCF Parking Services)
  - Drive time to each garage and walking time from that garage to the user's destination on campus (from Google Maps API)

The program's output then shows each available parking garage, sorted by total expected travel time, with detailed parking availability (available spaces and total capacity) as well as detailed expected travel durations (total travel time, driving time, and walking time).

## Caveats
Since this code was written as a proof-of-concept and as an educational exercise, a number of issues were set aside and would need to be addressed before deploying a finished application:
- The origin and destination are currently hard-coded. For mobile apps, GPS coordinates could be used instead of a street address. For a web-based app, the user could simply type in their origin location. In both cases, the user would also need a way to specify their destination.
- Origin and destination values are not currently be subjected to any validation before being passed to the Google Maps API.
- If this code were to be implemented for commercial purposes, UCF would need to be contacted for permission to gather parking garage data on a larger scale.
- The current web-scraping method for gathering parking garage availability data could easily be broken if the UCF Parking Services website were to change.
- Walking distances from each parking garage to each building on UCF campus should probably be looked up and cached periodically to avoid having two Google Maps API requests per execution.
- The acceptable parking permit types for each garage are currently hard-coded, and only garages with permit type 'D' (general student parking) are considered as parking options. A complete implementation might periodically look up and cache the permit types accepted at each garage and ask the user what type of permit(s) they currently have.
