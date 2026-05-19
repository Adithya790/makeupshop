# products/context_processors.py

from .models import Category

def menu_links(request):
    # Only main categories (categories without a parent)
    links = Category.objects.filter(parent__isnull=True).order_by('name')
    return dict(links=links)