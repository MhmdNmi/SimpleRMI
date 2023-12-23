from datetime import datetime
from PyRMI.RMIServer import *
from PyRMI.RMIconfig import config

REGISTRY_ADDRESS = (config['REGISTRY_HOST'], config['REGISTRY_PORT'])

date_format = "%Y-%m-%d %H:%M:%S"

class Calendar:
    def __init__(self):
        self.events = []

    def get_num_events(self):
        print("get_num_events")
        return len(self.events)

    def get_all_events(self):
        print("get_all_events")
        return self.events

    def get_event_by_name(self, name):
        print("get_event_by_name")
        find_event = None
        for e in self.events:
            if e['name'] == name:
                find_event = e
                break
        return find_event

    def add_event(self, event):
        print("add_event")
        find_event = self.get_event_by_name(event['name'])
        if find_event is None:
            self.events.append(event)
            return "Event added successfully!"
        else:
            return "Duplicate event name!"

    def remove_event(self, name):
        print("remove_event")
        find_event = self.get_event_by_name(name)
        if find_event is None:
            return "Event doesn't exist!"
        else:
            self.events = [e for e in self.events if e['name'] != name]
            return "Event removed successfully!"

    def get_events_by_type(self, etype):
        print("get_events_by_type")
        return [e for e in self.events if e['type'] == etype]

    def get_events_by_date(self, edate):
        print("get_events_by_date")
        return [e for e in self.events if e['date'] == edate]

    def get_events_by_location(self, elocation):
        print("get_events_by_location")
        return [e for e in self.events if e['location'] == elocation]

    def get_events_by_month_and_year(self, month, year):
        print("get_events_by_month_and_year")            
        return [e for e in self.events if e['date'].month == month and e['date'].year == year]

def main():
    server = Server(REGISTRY_ADDRESS)

    # register object
    server.register("Calendar_NSR", Calendar, update=True)

    print("\n\tServer is Ready.\n")
    server.run()    # start the event loop of the server to wait for calls


if __name__ == "__main__":
    main()

