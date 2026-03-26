from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import User
from .forms import UserRegistrationForm, UserSearchForm

def home(request):
    """Home page"""
    total_users = User.objects.count()
    recent_users = User.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'recent_users': recent_users,
    }
    return render(request, 'users/home.html', context)

def register_user(request):
    """Register new user"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User registered successfully! Unique ID: {user.unique_id}')
            return redirect('user_detail', pk=user.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_list(request):
    """List all users with search"""
    form = UserSearchForm(request.GET)
    users = User.objects.all().order_by('-created_at')
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            users = users.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(unique_id__icontains=search_query)
            )
    
    context = {
        'users': users,
        'form': form,
        'total_users': User.objects.count()
    }
    return render(request, 'users/user_list.html', context)

def user_detail(request, pk):
    """View single user details"""
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})

def user_edit(request, pk):
    """Edit user information"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('user_detail', pk=user.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm(instance=user)
    
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})

def user_delete(request, pk):
    """Delete user"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_list')
    
    return render(request, 'users/delete_user.html', {'user': user})