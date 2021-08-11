def is_on_list(day_list, day):
    if day in day_list:
        return True
    else:
        return False

def get_x(day_list, num):
    return day_list[num]
   

def add_x(day_list, day):
    day_list.append(day)

def remove_x(day_list, day):
    day_list.remove(day)


# \/\/\/\/\/\/\  DO NOT TOUCH AREA  \/\/\/\/\/\/\ #

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

print("Is Wed on 'days' list?", is_on_list(days, "Wed"))

print("The fourth item in 'days' is:", get_x(days, 3))

add_x(days, "Sat")
print(days)

remove_x(days, "Mon")
print(days)


# /\/\/\/\/\/\/\ END DO NOT TOUCH AREA /\/\/\/\/\/\/\ #


