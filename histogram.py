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


class Histogram( qp.QuickPlot ):


    def __init__( self ):
        qp.QuickPlot.__init__( self )


    def func_plot( self, json_data, str_output_figure ):
        """
        Function that quickly plots a histogram of data in a json file.
        """

        str_title = json_data[ qp.c_STR_TITLE ] if qp.c_STR_TITLE in json_data else qp.c_STR_TITLE_DEFAULT
        str_x_title = json_data[ qp.c_STR_X_AXIS ] if qp.c_STR_X_AXIS in json_data else qp.c_STR_X_AXIS_DEFAULT
        str_y_title = json_data[ qp.c_STR_Y_AXIS ] if qp.c_STR_Y_AXIS in json_data else qp.c_STR_Y_AXIS_DEFAULT
        i_bins = int( json_data[ qp.c_STR_BINS ] ) if qp.c_STR_BINS in json_data else qp.c_i_BINS_DEFAULT

        ldict_data = json_data[ qp.c_STR_DATA ]
        
        d_max_count = 0
        d_alpha = 1.0
        
        for dict_data in ldict_data:
            str_data_label = dict_data[ qp.c_STR_DATA_LABEL ] if qp.c_STR_DATA_LABEL in dict_data else None
            c_color = dict_data[ qp.c_C_PLOT_COLOR ] if qp.c_C_PLOT_COLOR in dict_data else qp.c_C_PLOT_COLOR_DEFAULT
            li_count, ldbl_bins, lpatch_batches = plt.hist( dict_data[ qp.c_STR_DATA ], color=c_color, label=str_data_label, alpha=d_alpha, bins=i_bins )
            d_max_count = max( d_max_count, max(li_count) )
            d_alpha = 0.5
            
        plt.ylim( [ 0, d_max_count + ( d_max_count * .1 ) ] )
        plt.title( str_title )
        plt.xlabel( str_x_title )
        plt.ylabel( str_y_title )
        plt.legend()
        plt.tight_layout()
        plt.savefig( str_output_figure )
        plt.close()
        
        return True
            
            
if __name__ == "__main__":
    Histogram().func_make_figure()