from fasthtml.common import Option, Select, Label, Div

def selector(
    name,
    id,
    label,
    options,
    value_key='id',
    hx_get=None,
    hx_target=None,
    hx_include=None
    ):

    _label = Label(label, _for=id)
    _options = []

    for opt in options:
        _opt = Option(opt['text'], value=opt[value_key])
        _options.append(_opt)

    return Div(
        _label,
        Select(
            *_options,
            name=name,
            id=id,
            hx_get=hx_get,
            hx_target=hx_target,
            hx_include=hx_include,
            )
        )
