from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.dummy.as_view(), name='dummy'),
    path('login', views.login.as_view(), name='login'),
    path('registration', views.registration.as_view(), name='registration'),
    path('logout', views.logout.as_view(), name='logout'),
    path('index', views.index.as_view(), name='index'),
    path('profile/<int:id>/',views.profile.as_view(), name='profile'),
    path('details/<int:id>/',views.details.as_view(), name='details'),
    path('dummyDetails/<int:id>/',views.dummyDetails.as_view(), name='dummyDetails'),
    path('editProfile/<int:id>/',views.editProfile.as_view(),name='editProfile'),
    path('company', views.company.as_view(), name='company'),
    path('ali', views.ali.as_view(), name='ali'),

]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
