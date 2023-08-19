from django.shortcuts import render
from . import util

from django.http import HttpResponse
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pages(request, page_name):
    output = util.get_entry(page_name)
    
    if (output is not None):
        #return HttpResponse(markdown2.markdown(output))
        return render(request, "encyclopedia/pages.html", {
            "page_name": page_name,
            "markdown_to_HTML": markdown2.markdown(output),
            })

    return render(request, "encyclopedia/pagenotfound.html")
