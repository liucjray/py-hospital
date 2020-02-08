from apscheduler.schedulers.blocking import BlockingScheduler
from services.KMSHService import *

if __name__ == '__main__':
    try:
        scheduler = BlockingScheduler()
        for job in [
            KMSHService(settings={
                'bg': True,
                'dept': '婦產科',
                'noonType': 'Night',
                'date': '2019/7/22',
                'doctor': '龍震宇',
            }),
            KMSHService(settings={
                'bg': True,
                'dept': '婦產科',
                'noonType': 'Night',
                'date': '2019/7/24',
                'doctor': '張慧名',
            }),
        ]:
            scheduler.add_job(job.register, 'interval', seconds=15)

        scheduler.start()
    except Exception as e:
        print(e)
