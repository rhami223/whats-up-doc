from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from customuser_app.models import CustomUser
from .models import Tickets
from .forms import AddTicket, LoginForm
from django.conf import settings
# Create your views here.

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"),password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage"))
                )

    form = LoginForm()
    return render(request, "generic_forms.html", {"form": form})


def logout_view(request):
    logout(request)    
    return HttpResponseRedirect(reverse("homepage"))

@login_required
def index(request):
    new_tickets = Tickets.objects.filter(status=Tickets.Status.NEW)
    inprogresstickets = Tickets.objects.filter(status=Tickets.Status.IN_PROGRESS)
    donetickets = Tickets.objects.filter(status=Tickets.Status.DONE)
    invalidtickets = Tickets.objects.filter(status=Tickets.Status.INVALID)
    return render(request, "index.html", {"new_tickets": new_tickets, 'inprogresstickets': inprogresstickets, 'donetickets': donetickets, 'invalidtickets': invalidtickets})


@login_required
def ticket_view(request, ticket_id):
    data = Tickets.objects.filter(id=ticket_id).first()
    return render(request, 'ticket_view.html', {'data': data})

    
@login_required
def user_view(request, user_id):
    new_tickets = Tickets.obects.filter(status=Tickets.Status.NEW, filed_by=user_id)
    inprogresstickets = Tickets.objects.filter(status=Tickets.Status.IN_PROGRESS, assigned_to=user_id)
    donetickets = Tickets.objects.filter(status=Tickets.Status.DONE, completed_by=user_id)
    invalidtickets = Tickets.objects.filter(status=Tickets.Status.INVALID, filed_by=user_id)
    user_info = CustomUser.objects.filter(id=user_id).first()
    return render(request, "index.html", {'user_info': user_info, "new_tickets": new_tickets, 'inprogresstickets': inprogresstickets, 'donetickets': donetickets, 'invalidtickets': invalidtickets})

@login_required
def newticket_view(request):
    if request.method == "POST":
        form = AddTicket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Tickets.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                filed_by=request.user
            )
            return HttpResponseRedirect(reverse('homepage'))
    form = AddTicket()
    return render(request, 'generic_forms.html', {'form': form})


                               
def editticket_view(request, ticket_id):
    ticket = Tickets.objects.get(id=ticket_id)
    if request.method == 'POST':
        form = AddTicket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title=data.get('title')
            ticket.description=data.get('description')
            ticket.save()
            return HttpResponseRedirect(reverse('ticketview', args=[ticket.id]))
    data = {
        'title': ticket.title, 
        'description': ticket.description 

    }
    form = AddTicket(initial=data)
    return render(request, 'generic_forms.html', {'form': form})


def assignticket_view(request, ticket_id):
    ticket = Tickets.objects.get(id=ticket_id)
    ticket.status = Tickets.Status.IN_PROGRESS
    ticket.assigned_to = request.user
    ticket.save()
    return HttpResponseRedirect(reverse('ticketview', args=[ticket.id]))

def doneticket_view(request, ticket_id):
    ticket = Tickets.objects.get(id=ticket_id)
    ticket.status = Tickets.Status.DONE
    ticket.assigned_to = None
    ticket.completed_by = request.user
    ticket.save()
    return HttpResponseRedirect(reverse('ticketview', args=[ticket.id]))

def invalidticket_view(request, ticket_id):
    ticket = Tickets.objects.get(id=ticket_id)
    ticket.status = Tickets.Status.INVALID
    ticket.assigned_to = None
    ticket.completed_by = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticketview', args=[ticket.id]))
    
def reopenticket_view(request, ticket_id):
    ticket = Tickets.objects.get(id=ticket_id)
    ticket.status = Tickets.Status.IN_PROGRESS
    ticket.assigned_to = request.user
    ticket.completed_by = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticketview', args=[ticket.id]))

def returnticket_view(request, ticket_id):
    ticket = Tickets.objects.get(id=ticket_id)
    ticket.status = Tickets.Status.NEW
    ticket.assigned_to = None
    ticket.completed_by = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticketview', args=[ticket.id]))
