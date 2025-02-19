from fasthtml.common import *
from src import queries
import matplotlib.pyplot as plt
from fh_matplotlib import matplotlib2fasthtml
from create_dropdown import selector

app, route = fast_app()

@route('/')
def get(act:int=None, scene:int=None, speaker:str=None):
    return Titled('Romeo And Juliet Word Count',
        Form(
        Div(
            Label('Act', _for="act"),
            Input(_type='number', name='act', id='act', required=True, value=act, hx_get='/update_scenes', hx_target='#scene')
            #added hx_get and hx_target to update the scene dropdown based on the act selected
        ),
        Div(
            Label('Scene', _for="scene"),
            Select(Option('')),
            id='scene'
        ),
        Div(
            Label('Speaker', _for="speaker"),
            Select(Option('')),
            id='speaker'
        ),
        Div(
            Input(_type='submit', value="Get Speakers!")
        ),
        action="/words/",
        method="post"
        )
    )

@app.route('/update_scenes')
def get(act:int):
    options = queries.scenes(act_id=act).to_dict(orient='records') #get the scenes for the selected act
    dropdown = selector(
        name='scene',
        id='scene',
        label='Scene',
        options=options,
        hx_get='/update_speakers', #added hx_get to update the speaker dropdown based on the scene selected
        hx_target='#speaker',
        hx_include='#act' #added hx_include to include the act in the request
    )
    
    return dropdown

@app.route('/update_speakers')
def get(act:int, scene:int=None):
    options = queries.speakers(act=act, scene=scene).to_dict(orient='records') #get the scenes for the selected act
    dropdown = selector(
        name='speaker',
        id='speaker',
        label='Speaker',
        options=options,
        value_key='id', #added value_key to use the 'text' column as the value for the options
        text_key='speaker', #added text_key to use the 'speaker' column as the text for the options
    )
    
    return dropdown
    
@app.route('/words/')
async def post(r):

    form = await r.form()
    data = form._dict
    
    speaker = data['speaker']
    act = data['act']
    scene = data['scene']

    if all([speaker, act, scene]):

        return RedirectResponse(f"/{speaker}/{act}/{scene}", status_code=303)
    

@route('/{speaker}/{act}/{scene}')
def get(speaker:str, act:int, scene:int):

    df = (
        queries.word_count(speaker=speaker, act=act, scene=scene)
               .sort_values('word_count', ascending=False)
               .iloc[:10]
               )

    @matplotlib2fasthtml
    def viz():
        plt.bar(df.word, df.word_count)
    
    return Titled(speaker, viz())


serve()