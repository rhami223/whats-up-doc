"""bugtracker_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bugtracker_app import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('new_ticket/', views.newticket_view),
    path('ticket_view/<int:ticket_id>/', views.ticket_view, name='ticketview'),
    path('user_view/<int:user_id>/', views.user_view),
    path('edit_ticket/<int:ticket_id>/', views.editticket_view),
    path('assign_ticket/<int:ticket_id>/', views.assignticket_view),
    path('done_ticket/<int:ticket_id>/', views.doneticket_view),
    path('invalid_ticket/<int:ticket_id>/', views.invalidticket_view),
    path('reopen_ticket/<int:ticket_id>/', views.reopenticket_view),
    path('return_ticket/<int:ticket_id>/', views.returnticket_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('admin/', admin.site.urls),
]
