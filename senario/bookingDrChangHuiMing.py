from apscheduler.schedulers.blocking import BlockingScheduler
from services.KMSHService import *

if __name__ == '__main__':
    try:
        scheduler = BlockingScheduler()
        for job in [
            KMSHService(),
        ]:
            scheduler.add_job(job.handle, 'interval', seconds=15)

        scheduler.start()
    except Exception as e:
        print(e)
