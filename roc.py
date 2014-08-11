#!/usr/bin/env python

__author__ = "Timothy Tickle"
__copyright__ = "Copyright 2014"
__credits__ = [ "Timothy Tickle" ]
__license__ = "MIT"
__maintainer__ = "Timothy Tickle"
__email__ = "ttickle@broadinstitute.org"
__status__ = "Development"


import matplotlib.pyplot as plt
import pieChart
import quickPlot as qp

c_STR_X_AXES = "False positive rate* ( FP/P )"
c_STR_Y_AXES = "True positive rate ( TP/P )" 

# Describes the data coming in
c_INT_INDEX_ACTUAL = 0
c_INT_INDEX_PREDICTED = 1
c_INT_INDEX_VALUE_TO_VARY = 2

# Describes the indexing for the TP,FP,TN,FN
c_INT_INDEX_FN = 0
c_INT_INDEX_FP = 1
c_INT_INDEX_TN = 2
c_INT_INDEX_TP = 3

c_F_POSITIVE = True
c_F_NEGATIVE = not c_F_POSITIVE

class PositiveROC( qp.QuickPlot ):


    def __init__( self ):
        qp.QuickPlot.__init__( self )


    def func_plot( self, json_data, str_output_figure ):
        """
        Function that quickly plots a ROC of data in a json file.
        
        * json_data : JSON object or a dict
                    : Object to plot
        * str_output_figure : String path
                            : Figure to plot
        * return : boolean
                 : True indicates success
        """

        # --------------------------
        # | Known |  Predicted       |
        # |       | +      | -       |
        # |       |-------------------
        # | +     | TP     | FN      |
        # |-------|------------------|
        # | -     | FP     | TN      |
        # --------------------------

        # Plot annotations
        str_title = json_data[ qp.c_STR_TITLE ] if qp.c_STR_TITLE in json_data else qp.c_STR_TITLE_DEFAULT
        
        # Plot each data series
        # Data is expected to be [ [ actual, predicted, value_to_vary ],...]
        # Note that positive = True, negative = False
        for dict_data in json_data[ qp.c_STR_DATA ]:
            str_series_color = dict_data[ qp.c_C_PLOT_COLOR ] if qp.c_C_PLOT_COLOR in dict_data else qp.c_C_PLOT_COLOR_DEFAULT
            str_series_label = dict_data[ qp.c_STR_DATA_LABEL ] if qp.c_STR_DATA_LABEL in dict_data else None
            print "Series:"
            print str_series_label
            ll_point = dict_data[ qp.c_STR_DATA ]
            # Split out the data by the varying value and store TP, FP, TN, FN
            # And count the total number of positives
            i_total_positives = 0
            dict_rates = {}
            for l_point in ll_point:
                i_FN, i_FP, i_TN, i_TP = 0, 0, 0, 0
                if l_point[ c_INT_INDEX_ACTUAL ] == c_F_POSITIVE:
                    i_total_positives = i_total_positives + 1
                    if l_point[ c_INT_INDEX_PREDICTED ] == c_F_NEGATIVE:
                        i_FN = 1
                    else:
                        i_TP = 1
                else:
                    if l_point[ c_INT_INDEX_PREDICTED ] == c_F_NEGATIVE:
                        i_TN = 1
                    else:
                        i_FP = 1

                li_cur_rates = dict_rates.setdefault( l_point[ c_INT_INDEX_VALUE_TO_VARY ], [0,0,0,0] )
                dict_rates[ l_point[ c_INT_INDEX_VALUE_TO_VARY ] ] = [  li_cur_rates[ c_INT_INDEX_FN ] + i_FN,
                                                                        li_cur_rates[ c_INT_INDEX_FP ] + i_FP,
                                                                        li_cur_rates[ c_INT_INDEX_TN ] + i_TN,
                                                                        li_cur_rates[ c_INT_INDEX_TP ] + i_TP ]
            # Force to float
            i_total_positives = i_total_positives * 1.0

            # Plot all point by the value to vary
            ld_x_values = [ 0 ]
            ld_y_values = [ 0 ]
            d_cum_FP = 0.0
            d_cum_TP = 0.0

            for i_value in sorted( dict_rates.keys() ):
                d_cum_FP = d_cum_FP + dict_rates[ i_value ][ c_INT_INDEX_FP ]
                d_cum_TP = d_cum_TP + dict_rates[ i_value ][ c_INT_INDEX_TP ]
                # False positive rates
                ld_x_values.append( d_cum_FP / i_total_positives )
                # True positive rates
                ld_y_values.append( d_cum_TP / i_total_positives )
            
            # Cap off the end with 1,1 if needed
            if ( not ld_x_values[ -1 ] == 1.0 ) and ( not ld_y_values[ -1 ] == 1.0 ):
                ld_x_values.append( 1.0 )
                ld_y_values.append( 1.0 )
                
            # Plot series
            # Calculate the AUC using the relationship to the Gini coefficient
            f_auc = self.func_auc( ld_x_values, ld_y_values )
            plt.plot( ld_x_values, ld_y_values, marker="o", color=str_series_color, label=str_series_label + " ( " +str( round( f_auc, 2 ) ) + " ) ")

        # Annotate plot
        plt.title( str_title )
        plt.xlabel( c_STR_X_AXES )
        plt.ylabel( c_STR_Y_AXES )
        plt.xlim( 0.0,1.0 )
        plt.ylim( 0.0,1.0 )
        plt.legend( loc="lower right")
        plt.tight_layout()
        plt.savefig( str_output_figure )
        plt.close()
            

    def func_auc(self, lf_x, lf_y ):
        """
        Calculate AUC given an ordered set of points from a ROC.
        """
        
        f_sum_x_y = 0
        f_prev_x = lf_x[ 0 ]
        f_prev_y = lf_y[ 0 ]
        for f_x, f_y in zip( lf_x[ 1: ], lf_y[ 1: ] ):
            f_sum_x_y = f_sum_x_y + ( ( f_x - f_prev_x ) * ( f_y + f_prev_y ) )
            f_prev_x = f_x
            f_prev_y = f_y
        # TODO check
        return ( 1 - ( ( 1 - f_sum_x_y ) + 1 ) / 2.0 )


if __name__ == "__main__":
    PositiveROC().func_make_figure()