from fasthtml.common import *
import matplotlib.pyplot as plt
from fh_matplotlib import matplotlib2fasthtml
from src import queries

app, route = fast_app()


@route('/get_form')
def get(speaker:str=None, act:int=None, scene:int=None): #adding input fields to the form(Query Parameters)
    return Form(
        Div(
            Label('Act', _for="act"),
            Input(_type='number', name='act', id='act', required=True, value=act)
        ),
        Div(
            Label('Scene', _for="scene"),
            Input(_type='number', name='scene', id='scene', required=True, value=scene)
        ),
        Div(
            Label('Speaker', _for="speaker"),
            Input(_type='text', name='speaker', id='speaker', required=True, value=speaker)
        ),
        Div(
            Input(_type='submit', value="Get Word Count!")
        ),
        action="/words/",
        method="get"
    )

@route('/post_form')
def get():
    return Form(
        Div(
            Label('Act', _for="act"),
            Input(_type='number', name='act', id='act', required=True)
        ),
        Div(
            Label('Scene', _for="scene"),
            Input(_type='number', name='scene', id='scene', required=True)
        ),
        Div(
            Label('Speaker', _for="speaker"),
            Input(_type='text', name='speaker', id='speaker')
        ),
        Div(
            Input(_type='submit', value="Get Speakers!")
        ),
        action="/words/",
        method="post"
    )

@app.route('/words/')
def get(speaker:str=None, act:int=None, scene:int=None):

    df = queries.word_count(
        speaker=speaker,
        act=act,
        scene=scene
        )
    df = df.sort_values('word_count', ascending=False).iloc[:10]

    @matplotlib2fasthtml
    def viz():
        plt.bar(df.word, df.word_count)

    title = Div(
        H1(speaker),
        P(f'Act {act} Scene {scene}')
    )

    return Div(title, viz(), _class="container")

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

    df = queries.word_count(speaker=speaker, act=act, scene=scene).sort_values('word_count', ascending=False).iloc[:10]

    @matplotlib2fasthtml
    def viz():
        plt.bar(df.word, df.word_count)
    
    return Titled(speaker, viz())



serve()