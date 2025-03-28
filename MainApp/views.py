from django.http import Http404, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    # Создаем пустую форму при запросе методом GET
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
               'form': form,
               }
        return render(request, 'pages/add_snippet.html', context)
    
    #Получаем данные из формы и на их основе создаем новый снипет в БД

    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets-list")
        return render(request, 'pages/add_snippet.html', {'form': form})


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов',
               'snippets': snippets 
               }
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id: int):
    context = {"pagename": "Просмотр сниппета"}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"Snippet with id={snippet_id} not found")
    else:
        context["snippet"] = snippet
        context["type"] = "view"
        return render(request, "pages/snippet_detail.html", context)

def snippet_edit(request, snippet_id: int):
    context = {"pagename": "Редактирование сниппета"}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return Http404
    
    if request.method == "GET":
        form = SnippetForm()
        context = {
               'snippet': snippet,
               "type": "edit" 
               }
        return render(request, 'pages/snippet_detail.html', context)
    
    #Получаем данные из формы и на их основе создаем новый снипет в БД

    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        snippet.save()
        return redirect("snippets-list")
        



def snippet_delete(request, snippet_id: int):
    if request.method == "POST" or request.method == "GET":
        snippet = get_object_or_404(Snippet, id=snippet_id)
        snippet.delete()
    return redirect("snippets-list")

