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

class BarChart( qp.QuickPlot ):


    def __init__( self ):
        qp.QuickPlot.__init__( self )


    def func_plot( self, json_data, str_output_figure ):
        """
        Function that quickly plots a bar chart of data in a json file.
        
        * json_data : JSON object or a dict
                    : Object to plot
        * str_output_figure : String path
                            : Figure to plot
        * return : boolean
                 : True indicates success
        """

        # Get annotations
        str_title = json_data.get( qp.c_STR_TITLE, qp.c_STR_TITLE_DEFAULT )
        str_x_title = json_data.get( qp.c_STR_X_AXIS, qp.c_STR_X_AXIS_DEFAULT )
        str_y_title = json_data.get( qp.c_STR_Y_AXIS, qp.c_STR_Y_AXIS_DEFAULT ) 
        i_y_limit = int( json_data[qp.c_STR_Y_LIMIT ] ) if qp.c_STR_Y_LIMIT in json_data else None
        str_label_sort = json_data.get( qp.c_STR_SORT, None ) 
                
        # Max value in all series
        i_max_count = 0
        
        # Data tick labels (set by the first label instance that is not none)
        lstr_data_xticks = None

        # Global labels in case some data have different labels
        lstr_global_labels, f_update_labels, dict_label_instances = self.func_get_consistent_x_ticks( json_data, str_label_sort )

        # Width of the bars are dependent on the how many bar groups are given ( how many series of bar values are given )
        if f_update_labels:
            i_len_data_list = max( [ i_count for i_count in dict_label_instances.values()[ 0 ] ] )
        else:
            i_len_data_list = len( json_data[ qp.c_STR_DATA ] )
        i_bar_width = 1.0 / ( i_len_data_list + 1.0 ) if i_len_data_list > 1.0 else 0.5

        # make index between 1 and N
        # Also if there are no groups but each is a single bar add .25 to make the label center under the bar
        li_index = range( 1, len( lstr_global_labels ) + 1 )
        if i_len_data_list == 1:
            li_index = [ i_index + 0.25 for i_index in li_index ]

        # Get data
        for dict_data in json_data[ qp.c_STR_DATA ]:
            # Update the max value
            i_max_count = max( [ i_max_count, max( dict_data[ qp.c_STR_DATA ] ) ] )
            
            # Get data specific information
            li_data = dict_data [ qp.c_STR_DATA ]
            str_data_label = dict_data[ qp.c_STR_DATA_LABEL ] if qp.c_STR_DATA_LABEL in dict_data else None
            c_color = dict_data[ qp.c_C_PLOT_COLOR ] if qp.c_C_PLOT_COLOR in dict_data else qp.c_C_PLOT_COLOR_DEFAULT
            li_error_values = dict_data[ qp.c_STR_ERROR_VALUES ] if qp.c_STR_ERROR_VALUES in dict_data else None
            # Get x ticks
            if not lstr_data_xticks:
                lstr_data_xticks = dict_data[ qp.c_STR_X_TICK_LABEL ] if qp.c_STR_X_TICK_LABEL in dict_data else None
            
            # If updating the data to a global x ticks label is needed do that here
            li_cur_index, i_bar_width = [ li_index, i_bar_width ] if not f_update_labels else self.func_get_index_for_labels( lstr_global_labels, lstr_data_xticks, i_len_data_list, dict_label_instances )

            bar_cur = plt.bar( li_cur_index, li_data, 
                     width=i_bar_width, color=c_color, 
                     yerr=li_error_values, label=str_data_label )
            self.func_label_bars( bar_cur, li_error_values, plt.gca() )
            
            # Need to set to None so it will be refreshed
            # Or update the indices, cleanup to do at the end depending on the mode
            if f_update_labels:
                lstr_data_xticks = None
            else:
                li_index = [ i_cur_index + i_bar_width for i_cur_index in li_index ]

        # Annotate plots
        # Change y limits
        plt.ylim( 0, i_max_count + ( i_max_count * .1 ) )
        plt.title( str_title )
        plt.xlabel( str_x_title )
        plt.ylabel( str_y_title )

        # Add .5 to center the labels to the groups
        plt.xticks( [ i_index + 0.5 for i_index in range( 1, len( li_index ) + 1 ) ], lstr_global_labels if f_update_labels else lstr_data_xticks )
        plt.legend()
        plt.tight_layout()
        if not i_y_limit is None:
            plt.ylim( 0, i_y_limit )
        plt.savefig( str_output_figure )
        plt.close()
        
        return True


    def func_get_consistent_x_ticks(self, json_cur, str_sort_type = None ):
        """
        Series of data may have different labels.
        Combining those labels to a global x tick label set
        is implemented here for convenience.
        """
        
        # Global set of labels to compile
        sstr_global_labels = None
        
        # Indicates if an update will be needed given the labels
        # If there where no changes to the labels logic can be avoided and
        # Faster plotting can occur
        f_updates_are_needed = False
        
        # Measures the maximum number of data associated to a label
        # This helps to know how to measure the columns
        dict_label_instances_counter = {}

        # Get a combined set of labels
        for dict_data in json_cur[ qp.c_STR_DATA ]:

            # Get the current data's tick labels
            lstr_labels_cur = dict_data.get( qp.c_STR_X_TICK_LABEL, None )
            
            # Skip a data without labels
            # It is assumed that these labels mirror an already given set or set to be given
            # It is assumed this does not happen if mismatched x tick labels are given
            if lstr_labels_cur is None:
                continue
            
            # We received a label set
            sstr_labels_cur = set( lstr_labels_cur )
 
            # If this is the first time a label set is received
            # Use that set
            # Check to see if there are any differences in the global label set and the current
            # If there are then updating data and errors and such have to happen do to subsets of label sets
            # Being given instead of a consistent label set.
            if sstr_global_labels is None:
                sstr_global_labels = sstr_labels_cur
            else:
                if not len( sstr_global_labels ) == len( sstr_labels_cur ):
                    f_updates_are_needed = True
            
            # Update the global union of all sets received
            sstr_global_labels.update( sstr_labels_cur )
            
            # Update labels dictionary
            for str_label in sstr_labels_cur:
                dict_label_instances_counter[ str_label ] = dict_label_instances_counter.get(str_label, 0 ) + 1
                
        # Add the bar widths to the label count dict
        #"{ 'str_label' : [ i_count, i_bar_width ] }"
        for str_key, i_value in dict_label_instances_counter.iteritems():
            dict_label_instances_counter[ str_key ] = [ i_value, 1.0 / ( i_value + 1 ) ]
            
        # If sorting
        lstr_global_labels = list( sstr_global_labels )
        if str_sort_type:
            if str_sort_type == qp.c_STR_SORT_NUMERICALLY:
                lstr_global_labels = sorted( [ int( str_label ) for str_label in lstr_global_labels ] )
                lstr_global_labels = [ str( i_label ) for i_label in lstr_global_labels ]
            elif str_sort_type == qp.c_STR_SORT_LEX:
                lstr_global_labels.sort()

        return [ lstr_global_labels, f_updates_are_needed, dict_label_instances_counter ]


    def func_label_bars(self, ptch_bars, li_errors, ax_cur ):
        """
        Add heights as labels on bars.
        
        * ptch_bars : List of ax.bar
                    : The bars to label
        * li_errors : List of integers
                    : List of errors
        * ax_cur : Axes associated with the bars
                 : Current axes
        """
        
        if li_errors is None:
            li_errors = [ 0 ] * len( ptch_bars )
        for ptch_cur, i_error in zip( ptch_bars, li_errors ):
            i_height = ptch_cur.get_height()
            ax_cur.text( ptch_cur.get_x()+ptch_cur.get_width()/2.0, ( ( i_height + i_error ) + 0.25 ), '%d'%int(i_height), ha="center", va="bottom" )
            
            
    def func_get_index_for_labels( self, lstr_master_labels, lstr_labels_cur, i_data_group_count, dict_group_count ):
        """
        This assumes all of the labels of the lstr_labels_cur are in the lstr_master_labels and the lstr_labels_cur has only unique values .
        """
                #"{ 'str_label' : [ i_count, i_bar_width ] }"
        if not lstr_labels_cur:
            return lstr_labels_cur

        li_update_indices = []
        li_bar_widths = []

        for str_label in lstr_labels_cur:
            i_translated_index = lstr_master_labels.index( str_label )
            i_singleton_fudge = 1.0
            i_mlt_group_adjust = dict_group_count[ str_label ][ 1 ] * ( dict_group_count[ str_label ][ 0 ] - 1 )
            if dict_group_count[ str_label ][ 0 ] == 1:
                i_singleton_fudge = 1.25
            else:
                i_mlt_group_adjust = i_mlt_group_adjust + 0.25
            li_update_indices.append( i_translated_index + i_singleton_fudge + i_mlt_group_adjust )

            dict_group_count[ str_label ] = [ dict_group_count[ str_label ][ 0 ] - 1.0, dict_group_count[ str_label ][ 1 ] ]
            li_bar_widths.append( dict_group_count[ str_label ][ 1 ] )
        return [ li_update_indices, li_bar_widths ]


if __name__ == "__main__":
    BarChart().func_make_figure()