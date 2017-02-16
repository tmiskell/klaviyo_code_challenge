#!/usr/bin/python
import os
import sys
import csv
from optparse import OptionParser

def create_fixture( csv_file, fixture_file, model_type ):
    city_header = 'us_city'
    state_header = 'us_state'
    pop_header = 'population'
    air_header = 'airport'
    us_cities = []
    us_states = []
    pop_data = []
    air_data = []
    with open( csv_file, 'rb' ) as input_file:
        csv_rows = csv.DictReader( input_file )
        for row in csv_rows:
            us_cities.append( row[city_header] )
            us_states.append( row[state_header] )
            pop_data.append( row[pop_header] )
            air_data.append( row[air_header] )
    output_lines = []
    for i in range( len(us_cities) ):
        output_lines.append( "- model: " + model_type + "\n" )
        output_lines.append( "  pk: " + str(i+1) + "\n" )
        output_lines.append( "  fields:\n" )
        output_lines.append( "    us_city: " + us_cities[i] + "\n" )
        output_lines.append( "    us_state: " + us_states[i] + "\n" )
        output_lines.append( "    population: " + pop_data[i] + "\n" )
        output_lines.append( "    airport: " + air_data[i] + "\n" )
    with open( fixture_file, 'w' ) as output_file:
        output_file.writelines( output_lines )        

def main( args ):
    
    parser = OptionParser()
    csv_file = "us_city_state.csv"
    help_line = "The input CSV file to containing the fixture data to create a fixture file from. "
    help_line += "Defaults to: " + csv_file
    parser.add_option( '-i', '--input', type='string', dest='csv_file', default=csv_file, help=help_line )
    model_type = "register.location"
    help_line = "The model name to use when writing the output fixture file. "
    help_line += "Defaults to: " + model_type
    parser.add_option( '-m', '--model', type='string', dest='model_type', default=model_type, help=help_line )
                            
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
