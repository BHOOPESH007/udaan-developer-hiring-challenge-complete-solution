from django.shortcuts import render

# from rest framework libraries
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK

from screens.models import Screens, Seats
from screens.serializers import ScreensSerializer, SeatsSerializer
from .resources import get_choice_row_name, set_vacant_seat_matrix, get_updated_seats, get_unreserved_seat
# Create your views here.

def get_contigous_availableSeats(aisleSeats_list, change, seats_index, numSeats, one_row_seats_list):
    availableSeats =[]
    countSeats =0
    while countSeats < numSeats and not one_row_seats_list[seats_index] and seats_index in aisleSeats_list:
            
        availableSeats.append(seats_index)
        seats_index=seats_index+change
        countSeats+=1
    return availableSeats

def get_availableSeats(numSeats, choice, all_seats, seat_info):
    choice_rowName, choice_start_point = get_choice_row_name(choice)
    one_row_seats_list= all_seats[choice_rowName]
    one_row_aisleSeats= seat_info[choice_rowName]['aisleSeats']
    size_one_row_aisleSeats= len(one_row_aisleSeats)
    aisleSeats_matrix =[]
    for i in range(0,size_one_row_aisleSeats, 2):
        aisleSeats_matrix.append(range(one_row_aisleSeats[i], 1+one_row_aisleSeats[i+1]))
    
    for aisleSeats_list in aisleSeats_matrix:
        availableSeats= get_contigous_availableSeats(aisleSeats_list,1, choice_start_point, numSeats, one_row_seats_list)

        if len(availableSeats)==numSeats:
            print availableSeats
            return {choice_rowName:availableSeats}
        
        availableSeats= get_contigous_availableSeats(aisleSeats_list, -1, choice_start_point, numSeats, one_row_seats_list)
        
        if len(availableSeats)==numSeats:
            print availableSeats
            return {choice_rowName:availableSeats}
    
    raise ValidationError('since we do not have '+ str(numSeats)+ ' contigous seats for the user')    

class ScreensView(viewsets.ModelViewSet):
    
    queryset = Screens.objects.all()
    serializer_class = ScreensSerializer


    @detail_route(methods=['get'], url_path='seats')
    def unreserve_seat(self, request, *args, **kwargs):
       
        status = request.GET.get('status', None)
        numSeats = request.GET.get('numSeats', None)
        choice = request.GET.get('choice', None)
        

        if status == 'unreserved':
            screen_obj= Screens.objects.get(name= kwargs['pk'])
            
            seat_obj= Seats.objects.get(name= screen_obj.id)

            all_seats= seat_obj.seat_table
            unreserved_seats_index= {}
            
            for rowName, seat_list in all_seats.iteritems():
                unreserved_seats_index[rowName]= get_unreserved_seat(seat_list)
            return Response({'seats':unreserved_seats_index})

        if choice and numSeats:
            screen_obj= Screens.objects.get(name= kwargs['pk'])
            seat_info= screen_obj.seatInfo
            all_seats= Seats.objects.get(name= screen_obj.id).seat_table
            availableSeats = get_availableSeats(int(numSeats), choice, all_seats, seat_info)
            return Response(availableSeats) 
        
        return Response(HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        screen_name= request.data['name']
        seat_matrix= set_vacant_seat_matrix(request.data['seatInfo'])
        Response= super(ScreensView, self).create(request, *args, **kwargs)
        
        create_seat_obj= Seats.objects.create(name= Screens.objects.get(name=screen_name), seat_table= seat_matrix)
        create_seat_obj.save()
        return Response
    
    @detail_route(methods=['post'], url_path='reserve')
    def reserve_seat(self, request, *args, **kwargs):
        reserve_seat= request.data['seats']

        screen_obj= Screens.objects.get(name= kwargs['pk'])
        seat_obj= Seats.objects.get(name= screen_obj.id)
         
        for rowName, to_be_booked_seat in reserve_seat.iteritems():   

            all_seats= seat_obj.seat_table
            all_seats[rowName]= get_updated_seats(all_seats[rowName], to_be_booked_seat)
            seat_obj.seat_table= all_seats
            seat_obj.save()
        return Response('Congratulations!! you have booked your ticket successfully')


