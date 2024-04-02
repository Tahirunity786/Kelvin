from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .models import Product, Vote, Comment
from django.utils import timezone
from django.http import Http404



def home(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products': products})


@login_required(login_url='/accounts/signup')
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        url = request.POST.get('url')
        image = request.FILES.get('image')
        icon = request.FILES.get('icon')

        if title and body and url and image and icon:
            product = Product()
            product.title = title
            product.body = body
            if url.startswith("http://") or url.startswith("https://"):
                product.url = url
            else:
                product.url = "http://" + url
            product.icon = icon
            product.image = image
            product.pub_date = timezone.now()
            product.hunter = request.user
            product.save()
            
            # Modified redirect to include the created query parameter
            redirect_url = reverse('detail', args=[product.id]) + '?created=true'
            return redirect(redirect_url)
        else:
            context = 'Hey! All fields are mandatory'
            return render(request, 'products/create.html', {'error': context})
    return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})

def home(request):
    products = Product.objects.all()
    for product in products:
        product.comments_total = Comment.objects.filter(product=product).count()
    return render(request, 'products/home.html', {'products': products})


@login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        # Avoid creating multiple votes by the same user for a single product
        if not Vote.objects.filter(voter=request.user, product=product).exists():
            Vote.objects.create(voter=request.user, product=product)
        return redirect('detail', product_id=product_id)

@login_required(login_url='/accounts/signup')
def add_comment(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            # Assuming you have a Comment model with a 'text' field
            Comment.objects.create(product=product, user=request.user, text=comment_text)
        return redirect('detail', product_id=product_id)


