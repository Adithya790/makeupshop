from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, Category, CategoryBanner, Review
from cart.models import Cart


def product_list(request):
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.filter(parent=None)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })

def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug)

    reviews = Review.objects.filter(product=product).order_by('-created_at')

    avg_rating = 0
    if reviews.exists():
        avg_rating = sum(r.rating for r in reviews) / reviews.count()

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1)
    }

    return render(request, "products/product_detail.html", context)


@login_required(login_url='login')
def add_review(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

    return redirect('product_detail', slug=product.slug)



def category_products(request, slug):

    category = get_object_or_404(Category, slug=slug)

    categories = Category.objects.filter(parent=None)
    subcategories = category.subcategories.all()

    if subcategories.exists():
        products = Product.objects.filter(
            category__in=subcategories,
            stock__gt=0
        )

        banners = CategoryBanner.objects.filter(category=category)

    else:
        products = Product.objects.filter(
            category=category,
            stock__gt=0
        )

        banners = CategoryBanner.objects.filter(category=category.parent)

    return render(request, 'products/product_list.html', {
        'products': products,
        'selected_category': category,
        'categories': categories,
        'subcategories': subcategories,
        'banners': banners,
    })

def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect('cart_detail')