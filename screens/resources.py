import re
from rest_framework.exceptions import ValidationError


def get_choice_row_name(choice):
    
    regex_rowName = r"([A-Z]+)"
    regex_start_point = r"([0-9]+)"
    
    match_rowName= re.search(regex_rowName, choice)
    match_start_point= re.search(regex_start_point, choice)
    
    choice_rowName= match_rowName.group(0)
    choice_start_point= match_start_point.group(0)
    return str(choice_rowName), int(choice_start_point)

def set_vacant_seat_matrix(seatInfo):
    
    seat_matrix ={}
    for rowName, columnInfo in seatInfo.iteritems():
        seat_matrix.update({rowName:[0]*columnInfo['numberOfSeats']})
    return seat_matrix



def get_updated_seats(old_seats, to_be_booked_seat):
    for seats in to_be_booked_seat:
        if old_seats[seats]:
            raise ValidationError('seat is already booked')
        old_seats[seats]=1
    return old_seats


def get_unreserved_seat(one_row_list):
    unreserved_seats_index= []
    size_list = len(one_row_list)
    for index in range(size_list):
        if not one_row_list[index]:
            unreserved_seats_index.append(index)
    return unreserved_seats_index