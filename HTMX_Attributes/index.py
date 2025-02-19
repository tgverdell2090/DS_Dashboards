from fasthtml.common import *
from datetime import date
import pandas as pd
from fasthtml.core import Request
from utils import filter_events, event_selector


app, route = fast_app()

df = pd.read_csv('ds_events.csv').assign(date=lambda x: pd.to_datetime(x.date))

def form(date_start=None, date_end=None, event=None, name=None, email=None, event_date=None):
    return Div(
        Grid(
# ==========================================================
    Input(
        type="date",
        name="date_start",
        id="event_start_filter",

        # Set an `hx_get` argument
        # that send a get request to `/update_events/`
        hx_get='/update_events/',

        # Set an `hx_target` argument
        # so changes to the date_start
        # filter update the list of 
        # available events. The list of html
        # events has an id of "event"
        hx_target="#event",

        # Set an `hx_include` argument
        # so the date entered into the `date_end`
        # filter is also passed to the endpoint
        # Be sure to use the ID for the element
        hx_include="#event_end_filter",

        # Set `hx_swap` to the string 'outerHTML'
        hx_swap="outerHTML",

        value=date_start,
        min=df.date.min().strftime('%Y-%m-%d'),
        max=df.date.max().strftime('%Y-%m-%d')
        ),
    Input(
        type="date",
        name="date_end",
        id="event_end_filter",
        hx_get='/update_events/',
        hx_target="#event",
        hx_include='#event_start_filter',
        hx_swap='outerHTML',
        value=date_end,
        min=df.date.min().strftime('%Y-%m-%d'),
        max=df.date.max().strftime('%Y-%m-%d')
        )
# ==========================================================
        ),
    Form(action='/submit', method='post')(
        Label('Choose an event', for_="event"),
        event_selector(df, value=event),
        Label('Full Name', for_='name'),
        Input(type='text', id='name', placeholder='name', required=True, value=name),
        Label('Email', for_='email'),
        Input(type='text', id='email', placeholder='email', value=email),
        Label('Event Date', for_='date'),
        Input(type='date', name="event_date", id='date', placeholder='date', value=event_date),
        Button('Submit')
    )
    )

@route('/update_events/')
def get(date_start:str, date_end:str):
    from utils import filter_events
    events_filtered = filter_events(df, date_start, date_end)

    return event_selector(events_filtered)

@route('/')
def get(
    date_start:str=None,
    date_end:str=None,
    event:str=None,
    name:str=None,
    email:str=None,
    event_date:str=None,
    ):
    return Div(
        Br(),
        Titled('Sign up form!',
        Grid(
        form(
            date_start=date_start,
            date_end=date_end,
            event=event,
            name=name,
            email=email,
            event_date=event_date
            ),
        )
    ))
    

@route('/events/{event_name}/{event_date}')
def get(event_name:str, event_date:str):
    return H1(f'You are registered for {event_name} on {event_date}!')
    

@route('/submit')
def post(payload: dict = Body(...)): 

    event = payload['event']
    date = payload['date']

    return RedirectResponse(f'/events/{event}/{date}', status_code=303)
        
    
@route('/update_date/')
def get(event: str):
    date = events[events.uuid == event].date.iloc[0].strftime('%Y-%m-%d')
    return Input(type='date', id='date', value=date, disabled=True)

serve()