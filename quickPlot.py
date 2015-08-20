#!/usr/bin/env python

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"

import abc
import argparse
import json

# Constants to find data in the JSON object
c_STR_DATA = "data"
c_STR_DATA_LABEL = "label"
c_STR_ERROR_VALUES = "error"
c_STR_BINS = "bins"
c_i_BINS_DEFAULT = 40
c_C_PLOT_COLOR = "color"
c_C_PLOT_COLOR_DEFAULT = "cyan"
c_STR_SORT = "sort"
c_STR_SORT_LEX = "lexical"
c_STR_SORT_NUMERICALLY = "numeric"
c_STR_TITLE = "title"
c_STR_TITLE_DEFAULT = "Histogram"
c_STR_X_AXIS = "x_axis"
c_STR_X_AXIS_DEFAULT = "X Axis"
c_STR_Y_AXIS = "y_axis"
c_STR_Y_AXIS_DEFAULT = "Count"
c_STR_Y_LIMIT = "y_limit"
c_STR_X_TICK_LABEL = "x_ticks"


class QuickPlot(object):
    """
    Base parent class that manages a lot of the logistics to plotting.
    Exposes a func_plot that is over written by children and allows
    customization of plotting.
    """
    
    # This bit helps me make an abstract class that is checked on object instantiation
    __metaclass__ = abc.ABCMeta


    def __init__( self ):
        """
        Init called during inheritance.
        """
        
        pass

    def func_make_figure( self ):
        """
        Call the commands needed to plot.
        """
        
        args_cur = self.func_read_parameters()
        self.func_plot_from_paths( args_cur.hndl_input_file, args_cur.str_output_file )

    def func_plot_from_paths( self, hndl_path_json, str_path_output_plot ):
        """
        Allow to plot from paths if needed.
        """
        json_cur = json.load( hndl_path_json )
        
        # Check to make sure the json object has a data section
        if not c_STR_DATA in json_cur:
            print "".join( [ "Please make sure the JSON input file has a data labeled \"", self.str_DATA,"\"" ] )

        self.func_plot( json_cur, str_path_output_plot )

    @abc.abstractmethod
    def func_plot( self, json_data, str_output_file ):
        """
        Abstract method to write over.
        Enables plotting
        """
        
        print "QuickPlot plot"
        pass
    

    def func_read_parameters( self ):
        """
        Read command line.
        Only output and input files are given. 
        The rest of the customization is expected to be in the json objects.
        """
        
        print "Read Parameters"
            
        # Parse arguments
        prsr_arguments = argparse.ArgumentParser( prog = "quickPlot.py", description = "Quickly plot graphs", formatter_class = argparse.ArgumentDefaultsHelpFormatter )
        prsr_arguments.add_argument( metavar = "input_file", dest = "hndl_input_file", type = argparse.FileType( 'Ur' ), help = "Input file path." )
        prsr_arguments.add_argument( metavar = "output_file", dest = "str_output_file", help = "Output file path." )
        args = prsr_arguments.parse_args()
        
        return( args )
