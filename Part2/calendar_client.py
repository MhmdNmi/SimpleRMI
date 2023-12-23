from datetime import datetime
from PyRMI.RMIClient import *
from PyRMI.RMIconfig import config

REGISTRY_ADDRESS = (config['REGISTRY_HOST'], config['REGISTRY_PORT'])

def test(calendar):
    print('===========================================')
    print('\n\tTest Started!\n')

    event1 = {
        'type': 'speech',
        'date': datetime(2023, 12, 15, 10, 30),
        'length_minutes': 60,
        'name': 'Speech Event',
        'description': 'A speech on a relevant topic',
        'location': 'Conference Room A'
    }

    event2 = {
        'type': 'speech',
        'date': datetime(2023, 12, 15, 10, 30),
        'length_minutes': 100,
        'name': 'Speech Event',
        'description': 'A speech on a relevant topic',
        'location': 'Conference Room A'
    }

    event3 = {
        'type': 'contest',
        'date': datetime(2023, 11, 15, 10, 30),
        'length_minutes': 180,
        'name': 'Contest Event',
        'description': 'A programming contest',
        'location': 'Conference Room A'
    }

    print(f'\n\tadd_event: {calendar.add_event(event1)}')
    print(f'\n\tadd_event: {calendar.add_event(event2)}')
    print(f'\n\tadd_event: {calendar.add_event(event3)}')

    print(f'\n\tget_num_events: {calendar.get_num_events()}')

    print(f'\n\tget_all_events: {calendar.get_all_events()}')

    print(f'\n\tevent_by_name: {calendar.get_event_by_name("Speech Event")}')
    
    print(f'\n\tevents_by_type: {calendar.get_events_by_type("speech")}')
    
    print(f'\n\tevents_by_date: {calendar.get_events_by_date(datetime(2023, 12, 15, 10, 30))}')
    
    print(f'\n\tevents_by_location: {calendar.get_events_by_location("Conference Room A")}')
    
    print(f'\n\tevents_by_month_and_year: {calendar.get_events_by_month_and_year(12, 2023)}')

    print(f'\n\tremove_event: {calendar.remove_event("Speech Event")}')
    print(f'\n\tremove_event: {calendar.remove_event("Speech Event")}')

    print('\n\tTest Finished!\n')
    print('===========================================')


def main():

    calendar = Stub(REGISTRY_ADDRESS, "Calendar_NSR")

    print("\n\tWelcome To The My CALENDAR!\n")
    while True:
        print("\nWhat do you want to do?\n1. Add Event\n2. Delete Event\n3. Search Events\n4. Show All Events\n5. General test\n6. Exit\n")
        order = int(input())
        if order == 1:
            while True:
                event_type = int(input('What is your event type?\n1. speech\n2. tutorial\n3. contest\n4. sport match'))
                if event_type == 1:
                    event_type = 'speech'
                    break
                elif event_type == 2:
                    event_type = 'tutorial'
                    break
                elif event_type == 3:
                    event_type = 'contest'
                    break
                elif event_type == 4:
                    event_type = 'sport match'
                    break
                else:
                    print("Wrong Input!")
            year = int(input('When is your event date?\nEnter year:'))
            month = int(input('Enter month:'))
            day = int(input('Enter day:'))
            hour = int(input('Enter hour:'))
            minute = int(input('Enter minute:'))
            event_date = datetime(year, month, day, hour, minute)
            length_minutes = int(input('How lonh is your event? in minutes!'))
            event_name = str(input('What is the name of your event?'))
            description = str(input('Give me a description of your event:'))
            location = str(input('Where is the location of your event?'))
            
            event_tmp = {
                'type': event_type,
                'date': event_date,
                'length_minutes': length_minutes,
                'name': event_name,
                'description': description,
                'location': location
            }
            print(calendar.add_event(event_tmp))

        elif order == 2:
            event_name = str(input('What is the name of your event?'))
            print(calendar.remove_event(event_name))

        elif order == 3:
            method = int(input('What is your prefered method?\n1. name\n2. type\n3. date\n4. location\n'))
            if method == 1:
                event_name = str(input('What is the name of your event?'))
                print(calendar.get_event_by_name(event_name))
            if method == 2:
                while True:
                    event_type = int(input('What is your event type?\n1. speech\n2. tutorial\n3. contest\n4. sport match\n'))
                    if event_type == 1:
                        event_type = 'speech'
                        break
                    elif event_type == 2:
                        event_type = 'tutorial'
                        break
                    elif event_type == 3:
                        event_type = 'contest'
                        break
                    elif event_type == 4:
                        event_type = 'sport match'
                        break
                    else:
                        print("Wrong Input!")
                print(calendar.get_events_by_type(event_type))
            if method == 3:
                choice = int(input('When is your prefered method?\n1. by exact date\n2. by month and year\n'))
                if choice == 1:
                    year = int(input('When is your event date?\nEnter year:'))
                    month = int(input('Enter month:'))
                    day = int(input('Enter day:'))
                    hour = int(input('Enter hour:'))
                    minute = int(input('Enter minute:'))
                    event_date = datetime(year, month, day, hour, minute)
                    print(calendar.get_events_by_date(event_date))
                elif choice == 2:
                    year = int(input('When is your event date?\nEnter year:'))
                    month = int(input('Enter month:'))
                    print(calendar.get_events_by_month_and_year(12, 2023))
                else:
                    print("Wrong input!")
            if method == 4:
                location = str(input('Where is the location of your event?'))
                print(calendar.get_events_by_location(location))

        elif order == 4:
            print("Here is the list of all events:")
            print(calendar.get_all_events())

        elif order == 5:
            test(calendar)

        elif order == 6:
            print("\n\tGood Luck!\n")
            break

if __name__ == "__main__":
    main()
