#!/usr/bin/env python

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import matplotlib.pyplot as plt
import quickPlot as qp


class ScatterPlot( qp.QuickPlot ):


    def __init__( self ):
        qp.QuickPlot.__init__( self )


    def func_plot( self, json_data, str_output_figure ):
        """
        Function that quickly plots a histogram of data in a json file.
        """

        # Check to make sure there are only two data objects
        ldict_data = json_data[ qp.c_STR_DATA ]
        if not len( ldict_data ) == 2:
            return False

        # Plot annotations
        str_title = json_data[ qp.c_STR_TITLE ] if qp.c_STR_TITLE in json_data else qp.c_STR_TITLE_DEFAULT
        str_color = json_data[ qp.c_C_PLOT_COLOR ] if qp.c_C_PLOT_COLOR in json_data else qp.c_C_PLOT_COLOR_DEFAULT
        str_data_label_X = ldict_data[ 0 ][ qp.c_STR_DATA_LABEL ] if qp.c_STR_DATA_LABEL in ldict_data[ 0 ] else None
        str_data_label_Y = ldict_data[ 1 ][ qp.c_STR_DATA_LABEL ] if qp.c_STR_DATA_LABEL in ldict_data[ 1 ] else None


        # Plot
        plt.scatter( x = ldict_data[ 0 ][ qp.c_STR_DATA ], y = ldict_data[ 1 ][ qp.c_STR_DATA ], c = str_color )
        plt.title( str_title )
        plt.xlabel( str_data_label_X )
        plt.ylabel( str_data_label_Y )
        plt.tight_layout()
        plt.savefig( str_output_figure )
        plt.close()
            
            
if __name__ == "__main__":
    ScatterPlot().func_make_figure()