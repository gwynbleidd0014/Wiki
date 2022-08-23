from http.client import HTTPResponse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django import forms
from . import util
from markdown import markdown
from django.db import models
from django.urls import reverse
from random import randint



# Create a form to allow users to create new pages
class addPageForm(forms.Form):
    title = forms.CharField(label="Title of page")
    pageData = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 10}), label="Write your page")


# Create a from to allow users edit pages
class editPageForm(forms.Form):
    pageData = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 10}), label="Edit your page")



# handle default page
def index(request):
    # handle search on side bar
    q = request.GET.get("q")
    if q in util.list_entries():
        return redirect(f"/{q}")
    elif q:
        results = []
        for name in util.list_entries():
            if q in name.lower():
                results.append(name)

        return render(request, "encyclopedia/results.html", {
            "results": results
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })



# Add new page
def new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = addPageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            formDict = {}
            title = form.cleaned_data["title"]
            title = title.capitalize()
            pageData = form.cleaned_data["pageData"]
            if title in util.list_entries():
                return HttpResponse("Page already exists")
            formDict[title] = pageData
            with open(f"entries/{title}.md", 'w') as f:
                f.write(pageData)
            return HttpResponseRedirect(reverse("pages", args=[title]))
        else:
            return HttpResponseNotFound("Please enter valid inputs")  
    else:
        form = addPageForm()

    return render(request, "encyclopedia/new.html", {
        "form": form
    })

# Creating a view for all entries

def entries(request, entrie):
    if entrie not in util.list_entries():
        return HttpResponseNotFound("Invalid Page")
    
    return render(request, "encyclopedia/entirePage.html", {
        'title': entrie,
        'body': markdown(util.get_entry(entrie))
    })

# Creating a view for edit page
def edit(request, page):
    preForm = editPageForm(initial={"pageData": util.get_entry(page)})
    if request.method == "POST":
        form = editPageForm(request.POST)
        if form.is_valid():
            pageData = form.cleaned_data["pageData"]
            with open(f"entries/{page}.md", "w") as f:
                f.write(pageData)
            return HttpResponseRedirect(reverse("pages", args=[page]))
        else:
             return HttpResponseNotFound("Please enter valid inputs")
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": preForm,
            "title": page
        })

# Creating a view for random pages
def random(request):
    pages = util.list_entries()
    i = randint(0, len(pages) - 1)
    print(i)
    print(pages[i])
    return HttpResponseRedirect(reverse("pages", args=[pages[i]]))