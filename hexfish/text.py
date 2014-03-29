
STYLE = {
    '\x02': 'bold',
    '\x03': 'color',
    '\x0F': 'reset',
    '\x1D': 'italic',
    '\x1F': 'underline',
}

STYLE_INV = dict((val, key) for key, val in STYLE.items())

COLOR = {
    0: 'white',
    1: 'black',
    2: 'dark_blue',
    3: 'green',
    4: 'red',
    5: 'brown',
    6: 'purple',
    7: 'orange',
    8: 'yellow',
    9: 'light_green',
    10: 'teal',
    11: 'cyan',
    12: 'blue',
    13: 'pink',
    14: 'dark_gray',
    15: 'light_gray',
}

COLOR_INV = dict((val, key) for key, val in COLOR.items())

def add_style(style, text):
    return '{}{}{}'.format(STYLE_INV[style], text, STYLE_INV['reset'])

def add_color(fgcolor, bgcolor, text):
    return '{}{},{}{}{}'.format(STYLE_INV['color'], COLOR_INV.get(fgcolor, ''), COLOR_INV.get(bgcolor, ''), text, STYLE_INV['reset'])