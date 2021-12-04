import datetime
import sys
import logging

def get_current_date():
    """
    :return: DateTime object
    """
    return datetime.datetime


def get_current_platform():
    """
    :return: current platform
    """
    return sys.platform
    
def filtr_number(filtr):
    numbers=range(0,101)
    if filtr=="True":
    	msg = "Парні елементи: " 
    elif filtr=="False":
    	msg = "Непарні елементи: "
    
    for num in numbers:
    	if (filtr == "True") & (num%2 == 0):
    	    msg += str(num) + " "
    	elif (filtr == "False") & (num%2 != 0):
    	    msg += str(num) + " "
    return msg

def view_array():
    x=[5,9,6,3]
    print("Масив X[]:", x)
    index = int(input("Введіть номер елемента масиву який хочете вивести: "))
    try:
    	print(f"X[{index}] = {x[index]}")
    except IndexError:
        logging.error("Ви ввели число за межами проміжку 0-3")
    else:
    	logging.info("Ви ввели коректні дані")
