#!/usr/bin/env python

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2015"
__credits__ = [ "Timothy Tickle" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import matplotlib.pyplot as plt
import quickPlot as qp

# Default axes labels
c_STR_X_AXIS = "Value"
c_STR_Y_AXIS = "Group" 

# Colors
c_STR_BOX_LINE_COLOR = "blue"
c_STR_BOX_PLOT_COLOR = "cyan"
c_STR_MEDIAN_COLOR = "violet"
c_STR_OUTLIER_COLOR = "orange"

class BoxPlot( qp.QuickPlot ):

    def __init__( self ):
        qp.QuickPlot.__init__( self )

    def func_plot( self, json_data, str_output_figure ):
        """
        Function that quickly plots a group of box plots of data in a json file.
        
        * json_data : JSON object or a dict
                    : Object to plot
        * str_output_figure : String path
                            : Figure to plot
        * return : boolean
                 : True indicates success
        """

        # Plot annotations
        str_title = json_data[ qp.c_STR_TITLE ] if qp.c_STR_TITLE in json_data else qp.c_STR_TITLE_DEFAULT

        # Check for axes labels
        
        # Plot
        plt_cur = plt.figure()
        ax = plt_cur.add_subplot( 111 )
        ax.set_xticklabels( json_data[ qp.c_STR_DATA_LABEL ] )
        plt_bp = ax.boxplot( json_data[ qp.c_STR_DATA ], patch_artist=True )

        # Custom coloring
        for patch_box in plt_bp[ "boxes" ]:
            patch_box.set( color = c_STR_BOX_LINE_COLOR, linewidth = 1 )
            patch_box.set( facecolor = c_STR_BOX_PLOT_COLOR )
        for patch_whisker in plt_bp[ "whiskers" ]:
            patch_whisker.set( color = c_STR_BOX_LINE_COLOR, linewidth = 2 )
        for patch_cap in plt_bp[ "caps" ]:
            patch_cap.set( color = c_STR_BOX_LINE_COLOR, linewidth = 2 )
        for patch_median in plt_bp[ "medians" ]:
            patch_median.set( color = c_STR_MEDIAN_COLOR, linewidth = 1 )
        for patch_flier in plt_bp[ "fliers" ]:
            patch_flier.set( marker = "o", color = c_STR_OUTLIER_COLOR, alpha = 0.5 )

        # X axes
        str_x_label = c_STR_X_AXIS if not qp.c_STR_X_AXIS in json_data else json_data[ qp.c_STR_X_AXIS ]
        str_y_label = c_STR_Y_AXIS if not qp.c_STR_Y_AXIS in json_data else json_data[ qp.c_STR_Y_AXIS ]

        # Annotate plot
        plt.title( str_title )
        plt.xlabel( str_x_label )
        plt.ylabel( str_y_label )
        plt.legend( loc="lower right")
        plt.tight_layout()
        plt.savefig( str_output_figure )
        plt.close()

if __name__ == "__main__":
    BoxPlot().func_make_figure()
