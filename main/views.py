from django.shortcuts import render
from bs4 import BeautifulSoup
from .models import Link
import requests
from django.http import HttpResponseRedirect
from django.http import JsonResponse

# Create your views here.

def scrape(request):
    error_message = None  # Initialize error message
    if request.method == 'POST':
        if Link.objects.all().count() > 0:
            Link.objects.all().delete()
        site = request.POST.get('site', '')
        try:
            page = requests.get(site)
            page.raise_for_status()  # Raise HTTPError for bad status codes
        except requests.exceptions.RequestException as e:
            error_message = f'Failed to fetch page: {e}'  # Set error message
            links = Link.objects.all()  # Fetch existing links
            return render(request, 'main/result.html', {'error_message': error_message, 'links': links})

        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a', class_='chapter-name'):
            link_url = link.get('href')
            link_title = link.string
            Link.objects.create(url=link_url, title=link_title)

        return HttpResponseRedirect('/')
    else:
        links = Link.objects.all()
        return render(request, 'main/result.html', {'error_message': error_message, 'links': links})
    
def delete(request):
    Link.objects.all().delete()
    return render(request, 'main/result.html', {'links': []})

# def add_to_list(request):
#     if request.method == 'POST':
#         site = request.POST.get('site', '')
#         title = request.POST.get('title', '')
#         if PageList.objects.filer(title=title).exists():
#             pagelist = PageList.objects.get(title=title)
#         else:
#             pagelist = PageList.objects.create(title=title)

#         new_page = Page.objects.create(url=site, pagelist=pagelist)
    
#         return HttpResponseRedirect('/')
#     else:
#         return render(request, 'main/add_to_list.html', {})
    
   
