#!/usr/bin/env python3
import argparse
import scraper, conf

modes = ['search', 'route', 'go']

parser = argparse.ArgumentParser(description='Bixi stuff')

parser.add_argument('mode',
                    help="possible modes: %s" % ', '.join(modes))

parser.add_argument('arguments',
                    help="see the readme for the arguments for each mode",
                    nargs='+')

args = parser.parse_args()

def print_route_info(stations, start_location, end_location):
  print(get_location_info(stations, start_location, 'bikes'))
  print(get_location_info(stations, end_location, 'docks'))

def get_location_info(stations, location, looking_for):
  found = False
  for station_id in conf.locations[location]:
    station = stations[station_id]
    # Either the number of bikes or number of docks
    num_things = station[looking_for]

    if num_things > 0:
      if not found:
        print("%s @ %s:" % (looking_for, location))
        found = True

      try:
          station_name = conf.stations[station_id]
      except KeyError:
          station_name = station['name']
       
      # continue looking for bikes/docks in other stations
      # if the number of things is smaller than the settings
      if num_things < conf.min_things:
        print("\t%s: \t%d %s" % (station_name, num_things, looking_for))
      else:
        return "\t%s: \t%d %s\n" % (station_name, num_things, looking_for)

  # Nothing has been found
  if not found:
     return "No station with %s found near %s! Add a new station?\n" % (looking_for, location)

if args.mode in modes:
    stations = scraper.get_stations(conf.city)

    if args.mode == 'search':
        query = args.arguments[0].lower()
        for station_id, station in stations.items():
          if query in station['name'].lower():
            print( "%s: %s (%d bikes / %d docks)" % (station_id, station['name'], station['bikes'], station['docks']) )

    if args.mode == 'route':
        route = args.arguments[0]

        if route in conf.routes:
            start_location, end_location = conf.routes[route]

            print_route_info(stations, start_location, end_location)
        else:
            parser.error("The route \"%s\" does not exist in your conf file." % route)

    if args.mode == 'go':
        if len(args.arguments) == 2:
            start_location, end_location = args.arguments

            if start_location in conf.locations and end_location in conf.locations:
                print_route_info(stations, start_location, end_location)
            else:
                parser.error("At least one of your locations is not in your conf file.")
        else:
            parser.error("You must enter exactly two stations (a start and an end station).")
else:
    parser.error("See the readme for usage instructions.")
