from django.shortcuts import render
from . import util

from django import forms
from django.http import HttpResponse
import markdown2
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

#For NewPage function for creating a new wiki entry
class NewTaskForm(forms.Form):
    title = forms.CharField(label="title")
    page = forms.CharField(widget=forms.Textarea, label="NewPage")

#Default index page listing all wiki entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Displays a wiki entry
def pages(request, page_name):
    output = util.get_entry(page_name)
    
    if (output is not None):
        return render(request, "encyclopedia/pages.html", {
            "page_name": page_name,
            "markdown_to_HTML": markdown2.markdown(output),
            })

    return render(request, "encyclopedia/pagenotfound.html")

#Functionality for the search bar and the search page
def Search(request):
    query = request.GET.get('q', '')
    if (query in util.list_entries()):
        return pages(request, query)

    searchresults = []
    for entry in util.list_entries(): 
        index = entry.find(query)
        if index != -1:
            searchresults.append(entry)

    return render(request, "encyclopedia/searchresults.html", {
        "query":query, 
        "entries":searchresults
        })

def NewPage(request):
    error = "Page already exists"
    no_error = " "

    #Handles a POST request
    if request.method == "POST":
        form = NewTaskForm(request.POST)

        #Serverside validation
        if form.is_valid():
            title = form.cleaned_data["title"]
            page = form.cleaned_data["page"]

            #Ensures duplicate page doesn't exist and returns the entry back if it is
            if (title in util.list_entries()):
                return render(request, "encyclopedia/newpage.html", {
                    "form":form,
                    "error":error
                    })

            #Saves to disk
            page = f"#{title}\n{page}"
            util.save_entry(title, page)
            #Takes us to a new form
            return render(request, "encyclopedia/newpage.html", {
                "form": NewTaskForm(),
                "error":no_error
                })

        #If form is not valid, it is simply returned to the user
        else: 
            return render(request, "encyclopedia/newpage.html", {
                "form":form,
                "error":no_error
                })

    #If it is a GET request it is taken to a new request
    return render(request, "encyclopedia/newpage.html", {
        "form": NewTaskForm(),
        "error":no_error
        })

def EditPage(request, page_name):

    #Handles POST request
    if (request.method == "POST"):
        new_content = f"# {page_name}\n{request.POST.get('changed_page_content')}"
        util.save_entry(page_name, new_content)
        return HttpResponseRedirect(f"/wiki/{page_name}")
        #return HttpResponse(request.POST.get('changed_page_content'))


    #Handles GET request (from clicking the button on the wiki page)
    #Splits title and page content
    content = util.get_entry(page_name)
    lines = content.split('\n')
    title = lines.pop(0)
    page ='\n'.join(lines)

    return render(request, "encyclopedia/editpage.html", {
        "page_name": page_name, 
        "page": page,
        })

def Random(request): 
    entries = util.list_entries()
    return HttpResponseRedirect(f"/wiki/{random.choice(entries)}/")
