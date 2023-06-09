from django.shortcuts import render, redirect
from django.views import View
from room_reservation_app.models import Room, RoomReservation
from datetime import date, datetime
# Create your views here.


class Main(View):
    def get(self, request):
        return render(request, 'index.html')


class AddRoom(View):
    def get(self, request):
        return render(request, 'add_room.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        is_projector_available = request.POST.get(
            'is_projector_available') == 'on'

        if not name:
            return render(request, 'add_room.html', {'error': 'room not provided!'})

        if capacity < 0:
            return render(request, 'add_room.html', {'error': 'room capacity cannot be less than zero!'})

        if Room.objects.filter(name=name).first():
            return render(request, 'add_room.html', {'error': 'room already exists!'})

        new_room = Room()
        new_room.name = name
        new_room.capacity = capacity
        new_room.is_projector_available = is_projector_available
        new_room.save()

        return redirect('/')


class RoomList(View):
    def get(self, request):
        room_list = Room.objects.all()
        for room in room_list:
            room.is_booked = bool(room.roomreservation_set.filter(date=date.today()))

        if not room_list:
            return render(request, 'room_list.html', {'error': 'no rooms available!'})

        return render(request, 'room_list.html', {
            'room_list': room_list,
        })


class DeleteRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        room.delete()
        return redirect('/rooms/')


class EditRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        return render(request, "edit_room.html", {'room': room})

    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)

        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else 0
        is_projector_available = request.POST.get(
            'is_projector_available') == 'on'

        if not name:
            return render(request, 'edit_room.html', {'error': 'room not provided!', 'room': room})

        if capacity < 0:
            return render(request, 'edit_room.html', {'error': 'room capacity cannot be less than zero!', 'room': room})

        room.name = name
        room.capacity = capacity
        room.is_projector_available = is_projector_available
        room.save()

        return redirect('/rooms/')


class BookRoom(View):
    def get(self, request, room_id):
        return render(request, 'book_room.html', {'room_name': Room.objects.get(pk=room_id).name})

    def post(self, request, room_id):
        reservation_date = request.POST.get('reservation_date')
        comment = request.POST.get('comment')

        if datetime.strptime(reservation_date, '%Y-%m-%d').date() < date.today():
            return render(request, 'book_room.html', {
                'room_name': Room.objects.get(pk=room_id).name,
                'error': 'cannot book room in the past, duh...'
            })

        if RoomReservation.objects.filter(room_id=room_id).filter(date=reservation_date):
            return render(request, 'book_room.html', {
                'room_name': Room.objects.get(pk=room_id).name,
                'error': 'room has been booked on given day'
            })

        booked_room = RoomReservation()
        booked_room.room_id = Room.objects.get(pk=room_id)
        booked_room.date = reservation_date
        booked_room.comment = comment
        booked_room.save()

        return redirect('/rooms/')


class RoomDetails(View):
    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        reservations = room.roomreservation_set.filter(
            room_id=room_id).filter(date__gte=date.today()).order_by('date')
        return render(request, 'room_details.html', {
            'room': room,
            'reservations': reservations
        })
