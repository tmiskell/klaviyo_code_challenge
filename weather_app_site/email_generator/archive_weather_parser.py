"""
"""
from __future__ import with_statement
import HTMLParser
import os
import sys

class ArchiveWeatherParser( HTMLParser.HTMLParser ):

    def __init__( self ):
        HTMLParser.HTMLParser.__init__( self )
        self._n_col = 0
        self._n_row = 0
        self._finished = False
        self._mean_loc = None
        self._actual_loc = None
        self._avg_loc = None
        self._rec_loc = None
        self._actual_temp = None
        self._avg_temp = None
        self._rec_temp = None
        self._units = ""

    def _is_int( self, x ):
        try:
            int( x )
            return True
        except ValueError:
            return False

    def ActualTemp( self ):
        return self._actual_temp

    def AvgTemp( self ):
        return self._avg_temp

    def RecTemp( self ):
        return self._rec_temp

    def Units( self ):
        return self._units
    
    def handle_starttag( self, tag, attrs ):
        if self._finished:
            return
        if tag == "table":
            self._n_row = 0
            self._n_col = 0
            self._mean_loc = None
            self._actual_loc = None
            self._avg_loc = None
            self._rec_loc = None
        elif tag == "tr":
            self._n_col = 0
            self._n_row += 1
        elif tag == "th":
            self._n_col += 1
        elif tag == "td":
            self._n_col += 1
        return
            
    def handle_endtag( self, tag ):
        if self._finished:
            return
        if tag == "tr":
            if self.ActualTemp() or self.AvgTemp() or self.RecTemp():
                self._finished = True
        return
            
    def handle_data( self, data ):
        if self._finished:
            return
        cleaned_data = data.strip().lower()
        if cleaned_data:
            if self._mean_loc:
                if self._n_row == self._mean_loc:
                    if self._is_int( cleaned_data ):
                        if self._actual_loc:
                            if self._n_col == self._actual_loc:
                                self._actual_temp = int( cleaned_data )
                        if self._avg_loc:
                            if self._n_col == self._avg_loc:
                                self._avg_temp = int( cleaned_data )
                        if self._rec_loc:
                            if self._n_col == self._rec_loc:
                                self._rec_temp = int( cleaned_data )
                    elif ("f" in cleaned_data) or ("c" in cleaned_data):
                        self._units = cleaned_data.replace("&nbps;", "").replace("&deg;", "")
            elif cleaned_data == "mean temperature":
                self._mean_loc = self._n_row
            elif cleaned_data == "actual":
                self._actual_loc = self._n_col
            elif cleaned_data == "average":
                self._avg_loc = self._n_col
            elif cleaned_data == "record":
                self._rec_loc = self._n_col
        return
                
def main( args=[] ):

    archive_file = os.path.join( "C:" + os.sep + "Users", "tmiskell", "Documents", "python_scripts", "page_source_wu_boston.html" )

    # Parse HTML
    parser = ArchiveWeatherParser()
    if os.path.exists( archive_file ):
        lines = ""
        with open( archive_file, 'r' ) as input_file:
            lines_array = input_file.readlines()
            for next_line in lines_array:
                lines += next_line
        parser.feed( lines )
        if parser.AvgTemp():
            sys.stdout.write( "Average Temp: %s %s\n" % (parser.AvgTemp(), parser.Units()) )
        elif parser.ActualTemp():
            sys.stdout.write( "Average Temp: %s %s (Approx. based on actual.)\n" % (parser.ActualTemp(), parser.Units()) )
        elif parser.RecTemp():
            sys.stdout.write( "Average Temp: %s %s (Approx. based on record.)\n" % (parser.RecTemp(), parser.Units()) )
        else:
            sys.stderr.write( "*** Unable to determine average temperature. ***" )
    else:
        sys.stderr.write( "File does not exist: %s %s" % (archive_file) )
    return 0

if __name__ == "__main__":
    sys.exit( main(sys.argv) )
