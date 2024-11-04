from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Stock, Order
from .forms import SignupForm, FeedbackForm
from .models import Store
from .models import User # Assuming you're using the User model
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from .models import StoreRequest  # Import your store request model

import json
import csv
# Signup view
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'stock/register.html', {'form': form})


# Login view
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get 'Remember Me' input

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Store user details in session
            request.session['username'] = user.username
            request.session['full_name'] = f"{user.first_name} {user.last_name}"
            request.session['email'] = user.email

            # Handle 'Remember Me' functionality
            if remember_me:  # If 'Remember Me' is checked
                request.session.set_expiry(1209600)  # Session will expire in 2 weeks
            else:  # Session will expire when the browser is closed
                request.session.set_expiry(0)

            # Redirect based on user role (admin or regular user)
            if user.is_staff:
                return redirect('stock/admin_dashboard')  # Redirect to admin dashboard
            else:
                return redirect('house')  # Redirect to regular user's dashboard or homepage
        else:
            error = "Invalid username or password"
            return render(request, 'stock/login.html', {'error': error})

    return render(request, 'stock/login.html')


# Admin login view (Separate admin login)
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'stock/admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'stock/admin_login.html')

# User Dashboard
@login_required
def dashboard(request):
    if request.user.is_staff:  # Admins should not access the user dashboard
        return redirect('admin_dashboard')
    return render(request, 'stock/dashboard.html')

# Admin Dashboard
@login_required
def admin_dashboard(request):
    # pylint: disable=no-member
    stocks = Stock.objects.all()
    stock_data = {
        'labels': [stock.name for stock in stocks],
        'quantities': [stock.quantity for stock in stocks],
    }
    
    if not request.user.is_staff:  # Only admins (staff) should access this dashboard
        return redirect('dashboard')
    
    return render(request, 'stock/admin_dashboard.html', {'stocks': stocks, 'user': request.user, 'current_year': datetime.now().year, 'stock_data': stock_data})

# Profile view (common for both users and admins)
from .forms import UserProfileForm
@login_required
def profile_view(request):

    
    if request.user.is_authenticated:
        context = {
            'username': request.session.get('username'),
            'full_name': request.session.get('full_name'),
            'email': request.session.get('email'),
            'bio': 'This is a sample bio',  # You can replace this with actual bio logic
        }
        return render(request, 'stock/profile.html', context)
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)  # creates profile if missing
    user_form = UserForm(instance=user)
    profile_form = UserProfileForm(instance=user_profile)
    return render(request, 'blog/dashboard.html', {
        'user_profile': user_profile,
        'user': user,
        
    })

# Admin Profile
@login_required
def admin_profile(request):
    if request.user.is_superuser:
        admin = request.user
        full_name = f"{admin.first_name} {admin.last_name}"
        return render(request, 'stock/admin_profile.html', {
            'admin': admin,
            'full_name': full_name,
            'current_year': 2024  # Dynamically add the current year if needed
        })
    else:
        return redirect(reverse('user_dashboard'))


# Edit Profile
@login_required
@csrf_exempt  # Make sure to secure this properly in production
def edit_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_full_name = data.get('new_full_name')
        if new_full_name:
            request.user.full_name = new_full_name
            request.user.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid data'})

@login_required
@csrf_exempt  # Same as above
def change_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        user = request.user
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Current password is incorrect'})

# Home view
def home_view(request):
    return render(request, 'stock/home.html')

# Logout view
def logout_view(request):
    return render(request, 'stock/home.html')

# General Dashboard view
def dashboard_view(request):
    return render(request, 'stock/dashboard.html')

# Manage Stocks view
@login_required
def manage_stocks(request):
    # Logic for managing stocks
    return render(request, 'stock/manage_stocks.html')

# View Users
@login_required
def view_users(request):
    # Add your logic to display users here
    return render(request, 'stock/view_users.html')

# Settings view
@login_required
def settings_view(request):
    return render(request, 'stock/settings.html')

def house_view(request):
    # pylint: disable=no-member
    recent_stocks = Stock.objects.order_by('-date_added')[:5]
    print(recent_stocks)

    # Get recent orders (last 5 orders)
    recent_orders = Order.objects.order_by('-order_date')[:5]

    context = {
        'recent_stocks': recent_stocks,
        'recent_orders': recent_orders,
    }

    return render(request, 'stock/house.html', context)

# Add Stock view
@login_required
def add_stock(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        category = request.POST.get('category')  # Ensure this variable is being used

        # Create and save the stock if all fields are valid
        if name and quantity and price and category:
             # pylint: disable=no-member
            Stock.objects.create(
                name=name,
                quantity=quantity,
                price=price,
                category=category  # Use category here
            )
            return redirect('view_stock')  # Redirect to the view stock page
        else:
            # Handle the case where any field is missing
            return render(request, 'add_stock.html', {
                'error': "All fields are required."
            })

    return render(request, 'stock/add_stock.html')

# View Stock
@login_required
def view_stock(request):
    # Fetch all stocks
    # pylint: disable=no-member
    stocks = Stock.objects.all()
    # Create a dictionary to group stocks by category
    categorized_stocks = {}
    for stock in stocks:
        if stock.category not in categorized_stocks:
            categorized_stocks[stock.category] = []
        categorized_stocks[stock.category].append(stock)
    return render(request, 'stock/view_stock.html', {'categorized_stocks': categorized_stocks})
# Success Page
def success_page(request):
    return render(request, 'stock/success.html')
# Orders view
@login_required
def orders_view(request):
    # pylint: disable=no-member
    stocks = Stock.objects.all()  # Assuming you have a Stock model
    context = {
        'stocks': stocks
    }
    return render(request, 'stock/orders.html', context)

# Contact Us View
@login_required
def contact_view(request):
    # Logic for handling contact form submission can go here
    return render(request, 'stock/contact.html')

# Feedback View
@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            star_rating = form.cleaned_data['star']           
            # Process the feedback, such as saving to a database (optional)
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback')  # Redirect to the same page after submission

    else:
        form = FeedbackForm()

    return render(request, 'stock/feedback.html', {'form': form})


# Fetch users
def fetch_users(request):
    if request.method == 'GET':
        users = User.objects.all().values('id', 'username', 'email', 'date_joined')  # Adjust fields as necessary
        user_list = list(users)
        return JsonResponse(user_list, safe=False)

@csrf_exempt
@login_required
def delete_stock(request, id):
    if request.method == 'DELETE':
        stock = get_object_or_404(Stock, id=id)
        stock.delete()
        return JsonResponse({'status': 'success'})

# Delete User
@csrf_exempt
@login_required
def delete_user(request, id):
    if request.method == 'DELETE':
        user = get_object_or_404(User, id=id)
        user.delete()
        return JsonResponse({'success': 'success'})

@csrf_exempt
def edit_stock(request, id):
    if request.method == 'POST':
        stock = get_object_or_404(Stock, id=id)  # Improved error handling
        stock.name = request.POST.get('name')
        stock.quantity = request.POST.get('quantity')
        stock.price = request.POST.get('price')
        stock.save()
        return JsonResponse({'status': 'success'})

def restock_stock(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON data
        stock_name = data.get('stock_name')
        quantity = int(data.get('quantity'))

        try:
            # pylint: disable=no-member
            stock = Stock.objects.get(name=stock_name)
            stock.quantity += quantity  # Increase stock quantity
            stock.save()  # Save the changes
            return JsonResponse({'status': 'success'}, status=200)
        except Stock.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Stock not found.'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

# Export Stock data as CSV
def export_stock_csv(request):
    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Quantity', 'Price'])  # CSV Header

    # Write data from Stock model
    # pylint: disable=no-member
    for stock in Stock.objects.all():
        writer.writerow([stock.id, stock.name, stock.quantity, stock.price])

    return response

# Export User data as CSV
def export_user_csv(request):
    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Username', 'Email', 'Date Joined'])  # CSV Header

    # Write data from User model
    for user in User.objects.all():
        writer.writerow([user.id, user.username, user.email, user.date_joined])

    return response

from .models import Store  # Assuming you have a Store model

def register_store(request):
    if request.method == 'POST':
        store_name = request.POST['store_name']
        owner_name = request.POST['owner_name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        description = request.POST['description']

        # Create a new Store instance
        new_store = Store(
            store_name=store_name,
            owner_name=owner_name,
            email=email,
            phone=phone,
            location=location,
            description=description
        )
        new_store.save()

        # Redirect to a new view to display the registered store
         # pylint: disable=no-member
        return redirect('stock/store_list.html')

    return render(request, 'stock/register_store.html')
def store_list(request):
    # pylint: disable=no-member
    stores = Store.objects.all()  # Get all registered stores
    return render(request, 'stock/store_list.html', {'stores': stores})


def sell_stock(request):
    if request.method == 'POST':
        # Add logic to handle stock selling
        stock_name = request.POST.get('stock_name')
        quantity = request.POST.get('quantity')
        # Add logic to process selling the stock
        return HttpResponse(f"Sold {quantity} of {stock_name} stock!")
    return render(request, 'stock/sell_stock.html')

def fetch_store_requests(request):
    if request.method == "GET":
        # pylint: disable=no-member
        store_requests = list(StoreRequest.objects.values())
        return JsonResponse(store_requests, safe=False)

def handle_request(request, id):
    if request.method == "POST":
        decision = request.POST.get('decision')
        # pylint: disable=no-member
        store_request = StoreRequest.objects.get(id=id)
        
        if decision == 'accept':
            # Logic to approve the request
            store_request.status = "approved"
        elif decision == 'decline':
            # Logic to decline the request
            store_request.status = "declined"
        
        store_request.save()
        return JsonResponse({'status': 'success'})
    
def buy_stocks(request):
    # pylint: disable=no-member
    stocks = Stock.objects.all()  # Fetch available stocks from the database
    return render(request, 'stock/orders.html', {'stocks': stocks})

def payment(request):
    # Retrieve stock_id and quantity from query parameters
    stock_id = request.GET.get('stock_id')
    quantity = request.GET.get('quantity')

    # Fetch the stock item from the database
    stock = get_object_or_404(Stock, id=stock_id)

    # Calculate total price
    total_price = stock.price * int(quantity)

    return render(request, 'stock/payment.html', {
        'stock': stock,
        'quantity': quantity,
        'total_price': total_price
    })

def payment_success(request):
    return render(request, 'stock/payment_success.html')

def fetch_stocks(request):
    # pylint: disable=no-member
    stocks = Stock.objects.all().values('id', 'name', 'quantity', 'price')
    return JsonResponse(list(stocks), safe=False)