from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Testimonial
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")  # Redirect to homepage
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def user_signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Error creating account. Try again.")

    form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("login")


def home(request):
    # Get one product from each category
    categories = Product.objects.values_list('category', flat=True).distinct()
    featured_products = {}
    for category in categories:
        product = Product.objects.filter(category=category).first()
        if product:
            featured_products[category] = product

    # Get approved testimonials
    testimonials = Testimonial.objects.filter(approved=True)[:6]  # Limit to 6 testimonials

    return render(request, 'index.html', {
        'featured_products': featured_products,
        'testimonials': testimonials,
    })   


# Product Listing View
def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    
    # Get distinct categories for dropdown
    categories = products.values_list('category', flat=True).distinct()
    
    # Group products by category
    products_by_category = {category: products.filter(category=category) for category in categories}

    return render(request, 'shop/product_list.html', {'products_by_category': products_by_category, 'categories': categories})

# Product Detail View

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

# Cart View

def cart(request):
    # cart_items = OrderItem.objects.filter(order__customer=request.user, order__status='cart')
    # total_price = cart_items.aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'shop/cart.html')
    # return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Add to Cart
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product_name = data.get('product_name')
        product_price = data.get('product_price')

        # For logged-in users, you can save the cart to the database here
        if request.user.is_authenticated:
            # Add logic to save to the database
            pass

        # Return a success response
        return JsonResponse({'status': 'success', 'message': 'Product added to cart'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
# Remove from Cart

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')

        # For logged-in users, you can remove the item from the database here
        if request.user.is_authenticated:
            # Add logic to remove from the database
            pass

        # Return a success response
        return JsonResponse({'status': 'success', 'message': 'Product removed from cart'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def update_cart_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        # For logged-in users, you can update the quantity in the database here
        if request.user.is_authenticated:
            # Add logic to update the quantity in the database
            pass

        # Return a success response
        return JsonResponse({'status': 'success', 'message': 'Cart quantity updated'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
# Checkout and WhatsApp Redirect
@login_required
def checkout(request):
    order = get_object_or_404(Order, customer=request.user, status='cart')
    order.status = 'pending'
    order.save()
    whatsapp_message = f'New order from {request.user.username}:\n'
    for item in order.order_items.all():
        whatsapp_message += f'{item.quantity}x {item.product.name} - ${item.product.price}\n'
    whatsapp_message += f'Total: ${order.get_total_price()}'
    whatsapp_link = f'https://wa.me/1234567890?text={whatsapp_message}'
    return redirect(whatsapp_link)

@login_required
def testimonials(request):
    approved_testimonials = Testimonial.objects.filter(approved=True)  # Show only approved ones
    return render(request, 'shop/testimonials.html', {'testimonials': approved_testimonials})

# Submit Testimonial
@login_required
def submit_testimonial(request):
    if request.method == 'POST':
        content = request.POST['content']
        Testimonial.objects.create(customer=request.user, content=content, approved=False)
        messages.success(request, 'Testimonial submitted for approval!')
    return redirect('testimonials')

# Admin: Approve/Delete Testimonials
@login_required
def manage_testimonials(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'admin/manage_testimonials.html', {'testimonials': testimonials})

@login_required
def approve_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    testimonial.approved = True
    testimonial.save()
    messages.success(request, 'Testimonial approved!')
    return redirect('manage_testimonials')

@login_required
def delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted!')
    return redirect('manage_testimonials')
