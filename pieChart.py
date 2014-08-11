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


class PieChart( qp.QuickPlot ):


    def __init__( self ):
        qp.QuickPlot.__init__( self )


    def func_plot( self, json_data, str_output_figure ):
        """
        Function that quickly plots a pieChart of data in a json file.
        """

        # Check to make sure there are only two data objects
        dict_data = json_data[ qp.c_STR_DATA ][ 0 ]

        # Plot annotations
        str_title = json_data[ qp.c_STR_TITLE ] if qp.c_STR_TITLE in json_data else qp.c_STR_TITLE_DEFAULT
        lstr_colors = dict_data[ qp.c_C_PLOT_COLOR ] if qp.c_C_PLOT_COLOR in dict_data else qp.c_C_PLOT_COLOR_DEFAULT
        lstr_labels = dict_data[ qp.c_STR_DATA_LABEL ] if qp.c_STR_DATA_LABEL in dict_data else qp.c_STR_DATA_LABEL
        lf_data = dict_data[ qp.c_STR_DATA ] if qp.c_STR_DATA in dict_data else None
        lf_data = [ float( str_data ) for str_data in lf_data ]
        lf_data_max = max( lf_data )
        lf_data = [ f_data / lf_data_max for f_data in lf_data ]


        # Plot
        plt.pie( x=lf_data, labels=lstr_labels, colors=lstr_colors, autopct="%1.1f%%", shadow = True  )
        plt.title( str_title )
        plt.tight_layout()
        plt.savefig( str_output_figure )
        plt.close()
            
            
if __name__ == "__main__":
    PieChart().func_make_figure()