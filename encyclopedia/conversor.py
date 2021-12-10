from . import markdown
from . import util

def conversor(entry):
    markdowner= markdown.Markdown()
    for entry in util.list_entries():
        entry = markdowner.convert(entry)
        
    