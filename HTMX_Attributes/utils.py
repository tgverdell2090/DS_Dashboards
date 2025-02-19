import pandas as pd
from fasthtml.common import Option, Select

def filter_events(df, start, end):

    start, end = pd.to_datetime([start, end])
    start = start if start else df.date.min()
    end = end if end else df.date.max()
    
    events_filtered = df[(df.date >= start) & (df.date <= end)]
    
    return events_filtered


def event_selector(df, value=None):
    
    options = (
        df[['event name', 'uuid']]
        .apply(lambda x: 
                Option(
                    x['event name'],
                    value=x.uuid,
                    selected="selected" if value == x.uuid else ""
                    ), axis=1)
        .to_list()
        )
        
    if value != None:
        options = [Option(value="", selected='selected', disabled='disabled', hidden='hidden')] + options
        
    return Select(
            *options,
            id="event",
            required=True,
            hx_get='/update_date',
            hx_target='#date',
            hx_swap='outerHTML',
        )