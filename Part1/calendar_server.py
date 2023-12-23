import Pyro4
from datetime import datetime

date_format = "%Y-%m-%dT%H:%M:%S"

@Pyro4.expose
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
        return [e for e in self.events if datetime.strptime(e['date'], date_format).month == month and datetime.strptime(e['date'], date_format).year == year]


def main():
    daemon = Pyro4.Daemon() # make a Pyro daemon
    ns = Pyro4.locateNS()   # find the name server
    uri_calender = daemon.register(Calendar)    # register the calender as a Pyro object
    ns.register("example.calender", uri_calender)    # register the object with a name in the name server

    print("Ready.")
    print(f"Object uri = \'{uri_calender}\'")

    daemon.requestLoop()    # start the event loop of the server to wait for calls


if __name__ == "__main__":
    main()

