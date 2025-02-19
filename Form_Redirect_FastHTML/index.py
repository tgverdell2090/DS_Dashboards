from fasthtml.common import *
import pandas as pd


app, route = fast_app()

df = pd.read_csv('ds_events.csv').assign(date=lambda x: pd.to_datetime(x.date))


def event_selector(df):
    """
    Helper function for generating a dropdown menu
    """
    
    options = df[['event name', 'uuid']].apply(lambda x: Option(x['event name'], value=x.uuid), axis=1).to_list()
    
    return Select(
            *([Option(value="", selected='selected', disabled='disabled', hidden='hidden')] + options),
            id="event",
            required=True,
        )
    

form = Div(
Form(
    # Set the action and method
    # arguments so when the form is submitted
    # a post request is sent to the `/submit` endpoint
    action="/submit", method='post'
    )(
    Label('Choose an event', for_="event"),
    event_selector(df),
    Label('Full Name', for_='name'),
    Input(type='text', id='name', placeholder='name', required=True),
    Label('Email', for_='email'),
    Input(type='text', id='email', placeholder='email'),
    Label('Event Date', for_='date'),
    Input(type='date', id='date', placeholder='date'),
    Button('Submit')
)
)

@route('/')
def get():
    return Div(
        Br(),
        Titled('Sign up form!',
        Grid(
        form(),
        )
    ))
    
# Define a route. 
# If the user registered for an event named
# "Event Title" and the event is scheduled for
# "2025-10-03" the route should be
# `/events/Event Title/2025-10-03`
@route('/events/{event_id}/{date}')
def get(event_id:str, date:str):
    event = df[df.uuid == event_id]['event name'].iloc[0] 
    # Return an HTML message telling the user
    # what event they are registered for and 
    # on what date
    return Div(
        H1('Thanks for registering'),
        P(f'You are registering for {event}.'),
        P(f'The event is on {date}'),
        _class="container" 
    )
    

# Keep this route unchanged
# Below we reroute the 
# user to the relevant endpoint
# upon receiving a post request
# containing form data
@route('/submit')
def post(payload: dict = Body(...)): 

    event = payload['event']
    date = payload['date']

    #event_name = df[df['uuid'] == event]['event name'].iloc[0]
    
    return RedirectResponse(f'/events/{event}/{date}', status_code=303)

serve()