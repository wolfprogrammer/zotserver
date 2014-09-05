#!/usr/bin/env python
"""
py2html.py

A set of functions to generate html code to buttons, encode urls,
textarea and forms.

"""

__author__ = 'tux'

from bottle import template


def txt2html(text):
    """
    Convert text to html compatible text
    Add html tag <br /> to a text

    @param:  text ( string )
    @return: text  (string )  With
    """

    lines = text.splitlines()
    txt = ""

    for line in lines:
        txt = "".join([txt, line, ' <br />\n'])

    return txt


def url2tpl(url, label):
    url_tpl = """
          <a href="{{ url }}">{{ label }}</a>
          """

    url = url.replace(" ", "%20")  # Encode whitespace

    code = template(url_tpl, url=url, label=label)
    return code


def html_table(table, cellspacing="10", style='"width:500px"'):
    """
    Creates a html code to a table

    :param table: A list of rows of list of cells(text )
    :param style: Html style for the table:  e.g "width:300px" (default )
    :return:  html code to the table


    e.g:  print html_table( [['hello', 'world', 'haaa'], ['test', 'test4', 'cx854']])

    <table style="width:300px">
    <tr>
	    <td>hello</td>
	    <td>world</td>
	    <td>haaa</td>
    <tr>
    <tr>
	    <td>test</td>
	    <td>test4</td>
	    <td>cx854</td>

    <tr>

    </table>
    """

    txt_ = ""
    for row in table:
        txt = ""

        for cell in row:
            txt = "".join([txt, '\t<td>', cell, '</td>\n'])

        # print txt
        txt_ = "".join([txt_, '<tr>\n', txt, '\n<tr>\n'])

    # return "".join( [ "<table style=", style, '>\n', txt_, '\n</table>' ])

    return "".join(['<table cellspacing="', str(cellspacing), '" >\n', txt_, '\n</table>'])


def html_listbox(name, labels, values):
    """

    @param name:    Name of html listebox
    @param listb:   List of values list and option list
    @return:        Html code to listbox
    """

    lines = ""

    for idx, label in enumerate(labels):
        value = values[idx]
        lines = "".join([lines, '\t<option value="', value, '">', label, '</option>\n'])

    code = "".join(['<select name="', name, '">\n', lines, '\n</select>\n'])
    return code


def html_textarea(name, text="", width=600, height=500):
    width = str(width)
    height = str(height)

    html = "".join(['<TEXTAREA NAME="', name, '" style="width:', width,
                    'px; height:', height, 'px;" >\n\n'])
    html = "".join([html, text, "\n\n</TEXTAREA>"])
    return html


def html_form(action, subforms=[], method='POST', button_name="Submit", button_position="above"):
    form = "".join(['<form action="', action, '" method="', method, '">\n'])

    if button_position == "above":
        form += "".join(['\n<input value="', button_name, '" type="submit" />\n<br />'])

    for form_ in subforms:
        form = "".join([form, "\n<br />", form_])

    if button_position == "below":
        form += "".join(['\n<br /><input value="', button_name, '" type="submit" />\n<br />'])

    form += '\n</form>'

    return form


def html_button_submit(label, name=""):
    # <button name="button" value="OK" type="button">Click Me</button>
    if name != "":
        name = 'name="' + name + '"'

    txt = "".join(['<input ', name, ' value="', label, '"  type="submit" />'])
    return txt


def html_input(name, value, type, size, others=[]):
    txt = "".join(['<input name="', name, '" type="', type, '" value="', value, '" size="', str(size), '"'])

    txt_ = ""
    for other in others:
        txt_ = " ".join([txt_, other, '" />'])

    txt = "".join([txt, txt_, '" />'])
    # ,'" />' ])
    return txt


def html_input_text(name, value='', size=30):
    return html_input(name, value, type="text", size=size)


def html_input_password(name, size=20):
    return html_input(name, "", type="password", size=size)


def html_input_number(name, value="", size=6):
    return html_input(name, value=value, type="number", size=size)


def html_search_form(label="Search", action="search", button_label="Search"):
    """
    """
    html = """
    <form action="/{action}" method="GET">
        {label} <input name="q" type="text" autofocus />
        <input value="{button_label}" type="submit" />
    </form>
    """
    html = html.strip('\n')
    return html.format(label=label, action=action, button_label=button_label )



def html_image(src, width, height, href=None):

    if href:
        _href = '<a href="%s">' % href
    else:
        _href = ''

    txt = """<img src="{src}" width="{width}" height="{height}">"""
    txt= txt.format(src=src, width=str(width), height=str(height))
    txt = _href + txt
    return txt