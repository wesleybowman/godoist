from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler


def job(new_date):
    # get the current datetime up to the seconds. This is what GitHub uses in searches
    new_date = datetime.now().isoformat(timespec='seconds')

    with open('schedule_test.txt', 'w') as f:
        f.write(new_date)


if __name__ == '__main__':

    # Seems like I need to keep the main thread live using this system.
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone='utc')
    scheduler.add_job(job, 'interval', seconds=10, id='my_test_job')
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
