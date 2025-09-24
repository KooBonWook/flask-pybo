from markupsafe import Markup
import mistune

def format_datetime(value, fmt='%Y-%m-%d %H:%M'):
    return value.strftime(fmt)

md = mistune.create_markdown(escape=True, hard_wrap=True)
def markdown_filter(s):
    return Markup(md(s) if s else '')
