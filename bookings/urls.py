from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_session, name='book'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('mentor/<int:mentor_id>/', views.mentor_detail, name='mentor_detail'),
    path('reserve/<int:mentor_id>/', views.reserve_session, name='reserve_session'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment'),
    path('review/<int:booking_id>/', views.leave_review, name='leave_review'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update-booking/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
    path('manage-mentors/', views.manage_mentors, name='manage_mentors'),
path('add-mentor/', views.add_mentor, name='add_mentor'),
path(
    'edit-mentor/<int:mentor_id>/',
    views.edit_mentor,
    name='edit_mentor'
),
]