from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Maid, AvailabilitySlot
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse
# Create your views here.



def search_maids(request):
    if request.method=='POST':
        try:
            requested_time_str = request.POST['datetime']
            requested_time=' '.join(requested_time_str.split('T'))
            

            available_maids = Maid.objects.filter(
                (Q(availabilityslot__start_time__lte=requested_time) |
                Q(availabilityslot__end_time__gte=requested_time)) & 
                (Q(availabilityslot__start_time__lte=requested_time) &
                Q(availabilityslot__end_time__gte=requested_time))
            ).order_by('-rating')

            if not available_maids:
                message = "Sorry, no maids available."
                return render(request, 'error.html', {'message': message})

            return render(request, 'maid,cook,nanny_list.html', {'maids': available_maids})
        except ValueError:
            message = "Invalid time format. Please use HH:MM."
            return render(request, 'error.html', {'message': message})
    return render(request,'booking.html')
