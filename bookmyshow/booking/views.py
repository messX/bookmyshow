import datetime
import json

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from booking.models import Movie, Theatre, Screen, Show, Seat, ShowSheatMapping, Booking


def put_movie(request):
    try:
        name = request.POST.get('name')
    except Exception as err:
        return HttpResponse(
            json.dumps({'status': False}), content_type='application/json')
    movie = Movie(name=name)
    movie.save()
    return HttpResponse(
        json.dumps({'status': True, 'id':movie.id}), content_type='application/json')

def put_theatre(request):
    try:
        name = request.POST.get('name')
        city = request.POST.get('city')
        num_screens = request.POST.get('screen_count')
        theater = Theatre(name=name, city=city, no_of_screen=num_screens)
        theater.save()
    except Exception as err:
        print(err)
        return HttpResponse(
            json.dumps({'status': False}), content_type='application/json')
    return HttpResponse(
        json.dumps({'status': True, 'id':theater.id}), content_type='application/json')

def put_screen(request):
    try:
        name = request.POST.get('name')
        theater = Theatre.objects.get(id=request.POST.get('theatre_id'))
        screen = Screen(name=name, theater=theater)
        screen.save()
        return HttpResponse(
            json.dumps({'status': True, 'id': screen.id}), content_type='application/json')
    except Exception as err:
        return HttpResponse(
            json.dumps({'status': False}), content_type='application/json')

def put_show(request):
    try:
        show_time = datetime.datetime.strptime(request.POST.get('show_time'), '%Y-%m-%d %H:%M')
        theatre = Theatre.objects.get(id=request.POST.get('theater_id'))
        screen = Screen.objects.get(id=request.POST.get('screen_id'))
        movie = Movie.objects.get(id=request.POST.get('movie_id'))
        show = Show(show_time=show_time, theatre=theatre, screen=screen, movie=movie)
        show.save()
        return HttpResponse(
            json.dumps({'status': True, 'id': show.id}), content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(
            json.dumps({'status': False}), content_type='application/json')

def put_seat(request):
    try:
        no = request.POST.get('number')
        seat_type = request.POST.get('seat_type')
        show = Show.objects.get(id=request.POST.get('show_id'))
        seat = Seat(no=no, seat_type=seat_type, show=show)
        seat.save()
        # save in seatplan
        show_seat = ShowSheatMapping(seat=seat, show=show)
        show_seat.save()
        return HttpResponse(
                json.dumps({'status': True, 'id': seat.id}), content_type='application/json')
    except Exception as err:
        return HttpResponse(
            json.dumps({'status': False}), content_type='application/json')


def book(request):
    try:
        seats = int(request.POST.get('seats'))
        show = Show.objects.get(id=request.POST.get('show_id'))
        with transaction.atomic():
            all_seats = ShowSheatMapping.objects.filter(show=show, status='Empty')[:seats]
            if len(all_seats) < seats:
                return HttpResponse(json.dumps({'status': False, 'msg': 'seats_unavailable'}), content_type='application/json')
            else:
                blocked_seats = ShowSheatMapping.objects.select_for_update().filter(id__in=[__seat.id for __seat in all_seats])
            booking = Booking(paid_amount=float(request.POST.get('paid_amount')))
            booking.save()
            for _seat in blocked_seats:
                _seat.status = 'Booked'
                _seat.booking = booking
                _seat.save()
        return HttpResponse(
                json.dumps({'status': True, 'id': booking.id}), content_type='application/json')
    except Exception as err:
        return HttpResponse(
            json.dumps({'status': False}), content_type='application/json')
def get_booking(request):
    try:
        booking = Booking.objects.get(id=request.GET.get('id'))
        res = booking.as_json()
        print(res)
        res['seats'] = []
        seats = ShowSheatMapping.objects.filter(booking=booking)
        for _seat in seats:
            res['seats'].append(_seat.as_json())
        return HttpResponse(
            json.dumps({'status': True, 'data': res}), content_type='application/json')
    except Exception as err:
        return HttpResponse(
            json.dumps({'status': False}), content_type='application/json')
