import json
from pprint import pprint
import re  # noqa
from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

register = template.Library()


def generate_paragraph(data):
    text = data.get('text').replace('&nbsp;', ' ')
    return f'<p>{text}</p>'


def generate_list(data):
    config = {}
    list_li = []
    for index, item in enumerate(data.get('items')):
        if search := re.search('<code class="inline-code">([^<]+)</code>\s*(.*?)$', item, re.IGNORECASE):
            if index == 0:
                config.update(dict(re.compile(r'(\w+)="([^"]*)"').findall(search.group(1))))
            else:
                list_li.append({'icon': search.group(1), 'text': search.group(2)})
        else: 
            item = {'text': item.replace('<i></i>', '')}
            if config.get('icon'):
                item.update({'icon': config.get('icon')})
            list_li.append(item)
    
    if config.get('type'):
        return render_to_string('catalog/school/partials/lists/index.html', {'type': config.get('type'), 'items': list_li})
    else:
        list_li = ''.join([f'<li>{item}</li>' for item in data.get('items')])
        tag = 'ol' if data.get('style') == 'ordered' else 'ul'
        return f'<{tag}>{list_li}</{tag}>'


def generate_header(data):
    text = data.get('text').replace('&nbsp;', ' ')
    level = data.get('level')
    return f'<h{level}>{text}</h{level}>'


def generate_image(data):
    url = data.get('file', {}).get('url')
    caption = data.get('caption')
    classes = []

    if data.get('stretched'):
        classes.append('stretched')
    if data.get('withBorder'):
        classes.append('withBorder')
    if data.get('withBackground'):
        classes.append('withBackground')

    classes = ' '.join(classes)

    return f'<img src="{url}" alt="{caption}" class="img-fluid {classes}" />'


def generate_delimiter():
    return '<div class="spacer"></div>'


def generate_table(data):
    rows = data.get('content', [])
    table = ''

    for row in rows:
        table += '<tr>'
        for cell in row:
            table += f'<td>{cell}</td>'
        table += '</tr>'

    return f'<table>{table}</table>'


def generate_warning(data):
    title, message = data.get('title'), data.get('message')

    if title:
        title = f'<div class="alert__title">{title}</div>'
    if message:
        message = f'<div class="alert__message">{message}</div>'

    return f'<div class="alert">{title}{message}</div>'


def generate_quote(data):
    alignment = data.get('alignment')
    caption = data.get('caption')
    text = data.get('text')

    if caption:
        caption = f'<cite>{caption}</cite>'

    classes = f'align-{alignment}' if alignment else None

    return f'<blockquote class="{classes}">{text}{caption}</blockquote>'


def generate_code(data):
    code = data.get('code')
    return f'<code class="code">{code}</code>'


def generate_raw(data):
    return data.get('html')


def generate_embed(data):
    service = data.get('service')
    caption = data.get('caption')
    embed = data.get('embed')
    iframe = f'<iframe src="{embed}" allow="autoplay" allowfullscreen="allowfullscreen"></iframe>'

    return f'<div class="embed {service}">{iframe}{caption}</div>'


def generate_link(data):

    link, meta = data.get('link'), data.get('meta')

    if not link or not meta:
        return ''

    title = meta.get('title')
    description = meta.get('description')
    image = meta.get('image')

    wrapper = f'<div class="link-block"><a href="{ link }" target="_blank" rel="nofollow noopener noreferrer">'

    if image.get('url'):
        image_url = image.get('url')
        wrapper += f'<div class="link-block__image" style="background-image: url(\'{image_url}\');"></div>'

    if title:
        wrapper += f'<p class="link-block__title">{title}</p>'

    if description:
        wrapper += f'<p class="link-block__description">{description}</p>'

    wrapper += f'<p class="link-block__link">{link}</p>'
    wrapper += '</a></div>'
    return wrapper

def generate_alert(data):
    type, message = data.get('type'), data.get('message')
    return f'<div class="alert alert-{type}" role="alert">{message}</div>'

@register.filter(is_safe=True)
def editorjs(value):
    if not value or value == 'null':
        return ""

    if not isinstance(value, dict):
        try:
            value = json.loads(value)
        except ValueError:
            return value
        except TypeError:
            return value

    html_list = []
    for item in value['blocks']:

        type, data = item.get('type'), item.get('data')
        type = type.lower()

        if type == 'paragraph':
            html_list.append(generate_paragraph(data))
        elif type == 'header':
            html_list.append(generate_header(data))
        elif type == 'list':
            html_list.append(generate_list(data))
        elif type == 'image':
            html_list.append(generate_image(data))
        elif type == 'delimiter':
            html_list.append(generate_delimiter())
        elif type == 'warning':
            html_list.append(generate_warning(data))
        elif type == 'table':
            html_list.append(generate_table(data))
        elif type == 'code':
            html_list.append(generate_code(data))
        elif type == 'raw':
            html_list.append(generate_raw(data))
        elif type == 'embed':
            html_list.append(generate_embed(data))
        elif type == 'quote':
            html_list.append(generate_quote(data))
        elif type == 'linktool':
            html_list.append(generate_link(data))
        elif type == 'alert':
            html_list.append(generate_alert(data))


    return mark_safe(''.join(html_list))
