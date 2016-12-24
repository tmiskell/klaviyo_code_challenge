#!/usr/bin/python
import os
import sys
import csv
from optparse import OptionParser

def create_fixture( csv_file, fixture_file, model_type ):
    city_header = 'us_city'
    state_header = 'us_state'
    pop_header = 'population'
    us_cities = []
    us_states = []
    pop_data = []
    with open( csv_file, 'rb' ) as input_file:
        csv_rows = csv.DictReader( input_file )
        for row in csv_rows:
            us_cities.append( row[city_header] )
            us_states.append( row[state_header] )
            pop_data.append( row[pop_header] )
    output_lines = []
    for i in range( len(us_cities) ):
        output_lines.append( "- model: " + model_type + "\n" )
        output_lines.append( "  pk: " + str(i+1) + "\n" )
        output_lines.append( "  fields:\n" )
        output_lines.append( "    us_city: " + us_cities[i] + "\n" )
        output_lines.append( "    us_state: " + us_states[i] + "\n" )
        output_lines.append( "    population: " + pop_data[i] + "\n" )
    with open( fixture_file, 'w' ) as output_file:
        output_file.writelines( output_lines )        

def main( args ):
    
    parser = OptionParser()
    parser.add_option( '-i', '--input', type='string', dest='csv_file', default="us_city_state.csv",
                       help="The input CSV file to containing the fixture data to create a fixture file from.")
    parser.add_option( '-m', '--model', type='string', dest='model_type', default="register.location",
                       help="The model name to use when writing the output fixture file." )
    (options, args) = parser.parse_args()
    try:
        csv_file = os.path.abspath( options.csv_file )
        if not ( os.path.exists(csv_file) ):
            parser.error( 'Unable to find the input file ' + options.csv_file )
    except:
            parser.error( 'Unable to find the input file ' + options.csv_file )        
    # Setup the destination file.
    dest_dir = os.path.dirname( os.path.realpath(__file__) )
    ext = "yaml"
    fixture_file = "pre_load_db" + '.' + ext
    fixture_file = os.path.join( dest_dir, fixture_file )
    create_fixture( options.csv_file, fixture_file, options.model_type )
    sys.stdout.write( "Wrote " + os.path.basename(fixture_file) + "\n" )
    return os.EX_OK

if __name__ == "__main__":
    sys.exit( main(sys.argv) )
