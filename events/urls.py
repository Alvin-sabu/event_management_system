from django.urls import path
from . import views
from .views import get_fest_dates, list_photos, manage_event_and_winners
from .views import add_photo, edit_photo, delete_photo
from .views import event_statistics
from .views import download_department_wise_registrations,view_registrations
from .views import (
    # custom_admin_login, 
    custom_admin_logout, 
    admin_dashboard, 
    update_event,
    delete_event,  
    export_feedback, 
    update_college_poster,
    delete_college_poster,
    delete_fest_view,
    update_fest_view,
    delete_department_view,
    update_department_view,
    create_event,
    create_department,
    create_fest,
    upload_college_poster,
    view_feedbacks,
    manage_college_posters
)
from .views import (
    CustomPasswordResetView, 
    CustomPasswordResetDoneView, 
    CustomPasswordResetConfirmView, 
    CustomPasswordResetCompleteView
)
urlpatterns = [
    # Existing paths
    
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('registration/<int:registration_id>/', views.registration_detail, name='registration_detail'),
    path('registration/<int:registration_id>/download/', views.download_token, name='download_token'),
    path('registration_history/', views.user_registration_history, name='registration_history'),
    path('events/already_registered/', views.already_registered, name='already_registered'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_view'),
    path('calendar/events/<int:year>/<int:month>/<int:day>/', views.events_on_day, name='events_on_day'),
    path('feedback/<int:event_id>/', views.feedback, name='feedback'),
    path('feedback/thanks/', views.feedback_thanks, name='feedback_thanks'),
    path('event/<int:event_id>/feedback/report/', views.event_feedback_report, name='event_feedback_report'),
    path('events/results/<int:event_id>/', views.results_page, name='results_page'),
    path('admin/contactmessage/', views.ContactMessageAdminView, name='contactmessage_changelist'),
    path('admin/contact_messages/', views.contact_message_list, name='contact_message_list'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Custom Admin paths
    path('admin/logout/', custom_admin_logout, name='custom_admin_logout'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Event URLs
    path('events/admin/event/update/<int:pk>/', update_event, name='update_event'),
    path('admin/event/delete/<int:event_id>/', delete_event, name='delete_event'),
    
    # Feedback URLs
    path('admin/feedback/export/', export_feedback, name='export_feedback'),
    path('admin/feedbacks/', views.view_feedbacks, name='view_feedbacks'),
    
    # College Poster URLs
    path('admin/college_poster/update/<int:poster_id>/', update_college_poster, name='update_college_poster'),
    path('admin/college_poster/delete/<int:poster_id>/', delete_college_poster, name='delete_college_poster'),
    
    # Fest URLs
    path('admin/fest/update/<int:fest_id>/', update_fest_view, name='update_fest_view'),
    path('admin/fest/delete/<int:fest_id>/', delete_fest_view, name='delete_fest_view'),
    path('get_fest_dates/<int:fest_id>/', views.get_fest_dates, name='get_fest_dates'),
    
    # Department URLs
    path('events/admin/department/update/<int:pk>/', update_department_view, name='update_department'),
    path('admin/department/delete/<int:department_id>/', delete_department_view, name='delete_department_view'),
    
    # Additional Admin paths
    path('admin/event/create/', create_event, name='create_event'),
    path('admin/department/create/', create_department, name='create_department'),
    path('admin/fest/create/', create_fest, name='create_fest'),
    path('admin/college_poster/upload/', upload_college_poster, name='upload_college_poster'),
    path('admin/feedbacks/', view_feedbacks, name='view_feedbacks'),
    path('admin/college_posters/manage/', manage_college_posters, name='manage_college_posters'),
    path('events/', views.list_events, name='list_events'),
    path('departments/', views.list_departments, name='list_departments'),
    path('fests/', views.list_fests, name='list_fests'),
    path('college-posters/', views.list_college_posters, name='list_college_posters'),
    path('admin/event-performance-analysis/', views.event_performance_analysis, name='event_performance_analysis'),
    path('admin/user-engagement-analysis/', views.user_engagement_analysis, name='user_engagement_analysis'),
    path('manage_winners/', views.manage_event_and_winners, name='manage_event_and_winners'),
    path('manage_winners/<int:event_id>/', views.manage_event_and_winners, name='manage_event_and_winners'),
    path('admin/reply-to-message/<int:message_id>/', views.reply_to_message, name='reply_to_message'),
    path('admin/messages/', views.admin_messages, name='admin_messages'),

    path('admin/media/', views.media_management, name='media_management'),

     # URLs for Team Members
    path('admin/team_members/', views.list_team_members, name='list_team_members'),
    path('admin/team_members/add/', views.add_team_member, name='add_team_member'),
    path('admin/team_members/edit/<int:pk>/', views.edit_team_member, name='edit_team_member'),
    path('admin/team_members/delete/<int:pk>/', views.delete_team_member, name='delete_team_member'),


   # URLs for Front Page Videos
    path('admin/front_page_videos/', views.list_front_page_videos, name='list_front_page_videos'),
    path('admin/front_page_videos/add/', views.add_front_page_video, name='add_front_page_video'),
    path('admin/front_page_videos/edit/<int:pk>/', views.edit_front_page_video, name='edit_front_page_video'),
    path('admin/front_page_videos/delete/<int:pk>/', views.delete_front_page_video, name='delete_front_page_video'),
    path('event/<int:event_id>/registrations/', views.event_registration_list, name='event_registration_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/add/', views.add_news_item, name='add_news'),
    path('news/edit/<int:id>/', views.update_news_item, name='edit_news'),
    path('news/delete/<int:id>/', views.delete_news_item, name='delete_news'),
    path('admin/statistics/', event_statistics, name='event_statistics'),
    path('photos/', list_photos, name='list_photos'),
    path('photo/add/', add_photo, name='add_photo'),
    path('photo/edit/<int:photo_id>/', edit_photo, name='edit_photo'),
    path('photo/delete/<int:photo_id>/', delete_photo, name='delete_photo'),
    path('admin/download_department_wise_registrations/', download_department_wise_registrations, name='download_department_wise_registrations'),   
    path('admin/view_registrations/', view_registrations, name='view_registrations'),
]

