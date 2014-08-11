#!/usr/bin/env python

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import quickPlot as qp


class VennDiagram( qp.QuickPlot ):


    def __init__( self ):
        qp.QuickPlot.__init__( self )
        

    def func_plot( self, json_data, str_output_figure ):
        """
        Function that quickly plots a venn diagram of data in a json file.
        """
        
        str_title = json_data[ qp.c_STR_TITLE ] if qp.c_STR_TITLE in json_data else qp.c_STR_TITLE_DEFAULT
        ldict_data = json_data[ qp.c_STR_DATA ]

        # Two venn diagram mode
        if len( ldict_data ) == 2:
            # Plot venn diagram
            # Labels
            str_data_label_1 = ldict_data[ 0 ][ qp.c_STR_DATA_LABEL ] if qp.c_STR_DATA_LABEL in ldict_data[ 0 ] else None
            str_data_label_2 = ldict_data[ 1 ][ qp.c_STR_DATA_LABEL ] if qp.c_STR_DATA_LABEL in ldict_data[ 1 ] else None
            # Set colors
            str_data_color_1 = ldict_data[ 0 ][ qp.c_C_PLOT_COLOR ] if qp.c_C_PLOT_COLOR in ldict_data[ 0 ] else 'r'
            str_data_color_2 = ldict_data[ 1 ][ qp.c_C_PLOT_COLOR ] if qp.c_C_PLOT_COLOR in ldict_data[ 1 ] else 'g'
            venn2( [ set( ldict_data[ 0 ][ qp.c_STR_DATA ] ), set( ldict_data[ 1 ][ qp.c_STR_DATA ] ) ],
                set_labels = [ str_data_label_1, str_data_label_2 ], set_colors = [ str_data_color_1, str_data_color_2 ] )
        else:
            return False

        plt.title( str_title )
        plt.tight_layout()
        plt.savefig( str_output_figure )
        plt.close()
        
        return True


if __name__ == "__main__":
    VennDiagram().func_make_figure()