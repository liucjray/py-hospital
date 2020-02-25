from apscheduler.schedulers.blocking import BlockingScheduler
from services.SJTAService import *

if __name__ == '__main__':
    try:
        scheduler = BlockingScheduler()
        for job in [
            SJTAService(settings={
                'bg': True,
            }),
        ]:
            scheduler.add_job(job.query, 'interval', seconds=10)

        scheduler.start()
    except Exception as e:
        print(e)
