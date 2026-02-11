import csv
import os
import datetime

class LoggingModule:
    def __init__(self, events_file='events.csv', sessions_file='sessions.csv'):
        self.events_file = events_file
        self.sessions_file = sessions_file

    def log_event(self, event_type, event_description):
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.events_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, event_type, event_description])

    def log_session(self, user, action):
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.sessions_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, user, action])


def main():
    logger = LoggingModule()
    # Example logs
    logger.log_event('info', 'Module loaded.')
    logger.log_session('mpascoe92', 'started session')

if __name__ == '__main__':
    main()