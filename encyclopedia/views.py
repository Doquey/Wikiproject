from hashlib import new
from django import forms
from django.forms.widgets import HiddenInput
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse
import random
from markdown2 import Markdown
markdowner = Markdown()

class newform(forms.Form):
    title = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Title','style':'margin-bottom:4%;margin-top:2%; width:30%; padding:2%', 'class':'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'style':'height:80%;width:80%','class':'form-control'}),label="")
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(),required=False)
 





def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create_entry(request):
    if request.method =="POST":
        form = newform(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title) is None or form.cleaned_data['edit'] is True:
                util.save_entry(title,content)
                entry = util.get_entry(title)
                return render(request,'encyclopedia/page.html',{'title':title, 'content':entry})
            else:
                return render(request,'encyclopedia/pageexist.html',{'title':title,'content':content})
        else:
            return render(request,'encyclopedia/createentry.html',{
            'form':newform()
        })
    else:
        return render(request,'encyclopedia/createentry.html',{
            'form':newform()
        })

def nav(request):
    title = request.GET.get('nave','')
    if(util.get_entry(title) in util.list_entries()):
        return view_page(request,title)
    else:
        subsearches =[]
        for entry in util.list_entries():
            if title.upper() in entry.upper():
                subsearches.append(entry)
        return render(request,"encyclopedia/index.html",{'entries':subsearches})

def view_page(request,name):
    if name in util.list_entries():
        content = util.get_entry(name)
        entry_converted = markdowner.convert(content)
        context = {'content':entry_converted,'title':name}
        return render(request,'encyclopedia/page.html',context)
    else:
        content = util.get_entry(name)
        context = {'content':content,'title':name}
        return render(request,'encyclopedia/pagenotfound.html',context)
    

def randomx(request):
    radnum = random.randint(0,len(util.list_entries())-1)
    randomentry = util.list_entries()[radnum]
    context = {"entry":randomentry,'content':util.get_entry(randomentry)}
    return render(request,'encyclopedia/randompage.html',context)

def editentry(request,name):
    content = util.get_entry(name)
    if content is None:
        return render(request,"encyclopedia/pagenotfound.html",{'title':name})
    else:
        form = newform()
        form.fields['title'].initial = name
        form.fields['title'].widgets = HiddenInput()
        form.fields['content'].initial = content
        form.fields['edit'].initial = True
        context = {'form':form,'edit':form.fields['edit'].initial,"title":form.fields['title'].initial}
        return render(request,'encyclopedia/createentry.html', context)

