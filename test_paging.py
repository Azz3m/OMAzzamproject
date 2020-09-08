from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator


#models.py
from .models import Articles



def pagination_pro(request):
    #model
    my_model = Articles.objects.all()
    #number of items on each page
    number_of_item = 10
    #Paginator
    paginatorr = Paginator(my_model, number_of_item)
    #query_set for first page
    first_page = paginatorr.page(1).object_list
    #range of page ex range(1, 3)
    page_range = paginatorr.page_range

    context = {
    'paginatorr':paginatorr,
    'first_page':first_page,
    'page_range':page_range
    }
    #
    if request.method == 'POST':
        page_n = request.POST.get('page_n', None) #getting page number
        results = list(paginatorr.page(page_n).object_list.values('id', 'title'))
        return JsonResponse({"results":results})


    return render(request, 'index.html',context)
