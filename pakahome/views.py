"""Views for protected frontend pages (driver dashboard, admin dashboard)."""
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required


@require_GET
@ensure_csrf_cookie
def driver_dashboard_view(request):
    """Driver dashboard: only authenticated drivers. Others redirected to home or driver signup."""
    if not request.user.is_authenticated:
        return redirect('/register/driver/?next=/driver-dashboard/')
    if getattr(request.user, 'role', None) != 'driver':
        return redirect('/')
    return render(request, 'driver_dashboard.html')


@require_GET
@ensure_csrf_cookie
def admin_dashboard_view(request):
    """Admin dashboard: only authenticated admins. Others redirected to home."""
    if not request.user.is_authenticated:
        return redirect('/?login=1')
    if getattr(request.user, 'role', None) != 'admin':
        return redirect('/')
    return render(request, 'admin_dashboard.html')


@require_GET
@ensure_csrf_cookie
def driver_signup_view(request):
    """Driver registration page. Redirect to driver-dashboard if already logged in as driver."""
    if request.user.is_authenticated and getattr(request.user, 'role', None) == 'driver':
        return redirect('/driver-dashboard/')
    return render(request, 'driver_signup.html')
