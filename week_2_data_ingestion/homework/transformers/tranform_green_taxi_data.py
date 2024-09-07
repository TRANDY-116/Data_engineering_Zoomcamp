if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import inflection


@transformer
def transform(data, *args, **kwargs):
    """
    cleaning the data by doing the following
        * Remove rows where the passenger count is equal to 0 and 
            the trip distance is equal to zero.
        * Create a new column lpep_pickup_date by converting
             lpep_pickup_datetime to a date.
        * Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.
            Add three assertions:
            - vendor_id is one of the existing values in the column (currently)
            - passenger_count is greater than 0
            - trip_distance is greater than 0
    """
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]


    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    print(""" 
            * Removed rows where the passenger count is equal to 0 and
                 the trip distance is equal to zero.
            * Created a new column lpep_pickup_date by converting
             lpep_pickup_datetime to a date.
        
        """)

    data.columns = [inflection.underscore(col) for col in data.columns]


    print("""
            * columns chnaged to lowercase
        """)




    

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    # assert output is not None, 'The output is undefined'

    assert 'vendor_id' in output.columns, "'vendor_id' column not found"

    assert (output['passenger_count'] > 0).all(), "Some passenger_count values are not greater than 0!"
    
    assert (output['trip_distance'] > 0).all(), "Some trip_distance values are not greater than 0!"
