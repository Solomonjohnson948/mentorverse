from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Mentor, Booking, Profile, Review
from .forms import BookingForm, SignUpForm, ReviewForm, MentorForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'bookings/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect('admin_dashboard')

            return redirect('dashboard')

    return render(request, 'bookings/login.html')


def signup(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                gender=form.cleaned_data['gender'],
                field=form.cleaned_data['field'],
                goal=form.cleaned_data['goal']
            )

            login(request, user)
            return redirect('dashboard')

    return render(request, 'bookings/signup.html', {'form': form})


def book_session(request):
    mentors = Mentor.objects.all()

    return render(request, 'bookings/book.html', {
        'mentors': mentors
    })


def mentor_detail(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id)

    return render(request, 'bookings/mentor_detail.html', {
        'mentor': mentor
    })

@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if request.method == 'POST':
        booking.payment_status = 'Paid'
        booking.status = 'Pending'
        booking.save()

        return redirect('dashboard')

    return render(request, 'bookings/payment.html', {
        'booking': booking
    })
@login_required
def reserve_session(request, mentor_id):


    mentor = get_object_or_404(Mentor, id=mentor_id)

    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            booking.user = request.user
            booking.mentor = mentor
            booking.customer_name = request.user.username
            booking.email = request.user.email

            booking.status = 'Pending'
            booking.payment_status = 'Unpaid'

            booking.save()

            return redirect('payment', booking_id=booking.id)

    return render(request, 'bookings/reserve.html', {
        'form': form,
        'mentor': mentor
    })

@login_required
def dashboard(request):

    # Prevent admins from accessing user dashboard
    if request.user.is_staff:
        return redirect('admin_dashboard')

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total_bookings = bookings.count()

    pending_count = bookings.filter(
        status='Pending'
    ).count()

    confirmed_count = bookings.filter(
        status='Confirmed'
    ).count()

    completed_count = bookings.filter(
        status='Completed'
    ).count()

    return render(
        request,
        'bookings/dashboard.html',
        {
            'bookings': bookings,
            'total_bookings': total_bookings,
            'pending_count': pending_count,
            'confirmed_count': confirmed_count,
            'completed_count': completed_count,
        }
    )

def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def leave_review(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status='Completed'
    )

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.mentor = booking.mentor
            review.booking = booking
            review.save()

            return redirect('dashboard')

    return render(request, 'bookings/review.html', {
        'form': form,
        'booking': booking
    })

def about(request):
    return render(request, 'bookings/about.html')

@login_required
def leave_review(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status='Completed'
    )

    if Review.objects.filter(booking=booking).exists():
        return redirect('dashboard')

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.mentor = booking.mentor
            review.booking = booking
            review.save()

            mentor = booking.mentor
            all_reviews = Review.objects.filter(mentor=mentor)

            total_reviews = all_reviews.count()
            total_rating = sum(item.rating for item in all_reviews)

            mentor.rating = round(total_rating / total_reviews, 1)
            mentor.reviews = total_reviews
            mentor.save()

            return redirect('dashboard')

    return render(request, 'bookings/review.html', {
        'form': form,
        'booking': booking
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    bookings = Booking.objects.all().order_by('-created_at')

    total_bookings = bookings.count()
    pending_bookings = bookings.filter(status='Pending').count()
    completed_bookings = bookings.filter(status='Completed').count()
    total_mentors = Mentor.objects.count()

    total_revenue = 0
    for booking in bookings.filter(payment_status='Paid'):
        total_revenue += booking.mentor.price

    return render(request, 'bookings/admin_dashboard.html', {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
        'total_mentors': total_mentors,
        'total_revenue': total_revenue,
    })

@login_required
def update_booking_status(request, booking_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking.status = request.POST.get('status')
        booking.payment_status = request.POST.get('payment_status')
        booking.admin_note = request.POST.get('admin_note')
        booking.save()

    return redirect('admin_dashboard')

@login_required
def manage_mentors(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    mentors = Mentor.objects.all().order_by('-id')

    return render(request, 'bookings/manage_mentors.html', {
        'mentors': mentors
    })


@login_required
def add_mentor(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    form = MentorForm()

    if request.method == 'POST':
        form = MentorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('manage_mentors')

    return render(request, 'bookings/mentor_form.html', {
        'form': form,
        'title': 'Add Mentor'
    })

@login_required
def edit_mentor(request, mentor_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    mentor = get_object_or_404(Mentor, id=mentor_id)

    form = MentorForm(
        request.POST or None,
        request.FILES or None,
        instance=mentor
    )

    if form.is_valid():
        form.save()
        return redirect('manage_mentors')

    return render(
        request,
        'bookings/mentor_form.html',
        {
            'form': form,
            'title': 'Edit Mentor'
        }
    )