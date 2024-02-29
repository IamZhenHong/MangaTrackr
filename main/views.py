from django.shortcuts import render
from bs4 import BeautifulSoup
from .models import Link, Page
import requests
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login/')
def scrape(request):
    error_message = None  # Initialize error message
    pages = Page.objects.all()
    if request.method == 'POST':

        if request.POST.get('selected_item'):
            site = request.POST.get('selected_item')
        else:
            site = request.POST.get('site', '')

        try:
            page = requests.get(site)
            page.raise_for_status()  # Raise HTTPError for bad status codes
        except requests.exceptions.RequestException as e:
            error_message = f'Failed to fetch page: {e}'  # Set error message
            links = Link.objects.all()  # Fetch existing links
            return render(request, 'main/result.html', {'error_message': error_message, 'links': links, 'pages': pages})

        soup = BeautifulSoup(page.text, 'html.parser')

        title_tag = soup.find('h1')
        print(title_tag.string)

        if Page.objects.filter(url=site).exists():
            existing_page = Page.objects.get(url=site)
            existing_page.title = title_tag.string
            existing_page.save()
        else:
            existing_page = Page.objects.create(url=site, title=title_tag.string)
        
        existing_link_urls = [link.url for link in existing_page.link_set.all()]


        new_page = Page.objects.create(url=site, title=title_tag.string)
        for link in soup.find_all('a', class_='chapter-name'):
            link_url = link.get('href')
            link_title = link.string
            

            if link_url not in existing_link_urls:
                Link.objects.create(url=link_url, title=link_title, page=new_page, is_new=True)
            else:
                Link.objects.create(url=link_url, title=link_title, page=new_page, is_new=False)
        
        existing_page.link_set.all().delete()
        existing_page.delete()
            
        

        

        links = Link.objects.filter(page=new_page)
        return render(request, 'main/result.html', {'error_message': error_message, 'links': links, 'pages': pages,'selected_page_title': title_tag.string})

    else:
        links = Page.objects.first().link_set.all()
        
        return render(request, 'main/result.html', {'error_message': error_message, 'links': links, 'pages': pages})

@login_required(login_url='/login/')
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
    
   
