import log
import logging
import signal
from config.__init__ import read_conf
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BlockingScheduler
from tasks.token_task import reload_access_token

jobstores = {
    'default': RedisJobStore(read_conf(conf_type='redis')['db'])
}


def handler_terminate(signum, frame):
    """信号处理，终止定时任务
    """
    print('Signal handler called with signal', signum)
    raise InterruptedError


signal.signal(signal.SIGINT, handler_terminate)
signal.signal(signal.SIGTERM, handler_terminate)

scheduler = BlockingScheduler(jobstores=jobstores)
# scheduler.add_job(set_inspect, 'interval', minutes=180, id='set_inspect', replace_existing=True)  # 定时生成检查工单

scheduler.add_job(reload_access_token, 'interval', minutes=45, id='reload_access_token',
                  replace_existing=True)  # 检查access token是否过期  20分钟一次

log.setup(debug=True)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("start schedule tasks")
    try:
        scheduler.start()
    except (InterruptedError, KeyboardInterrupt):
        scheduler._logger.info("received interrupt")
    finally:
        scheduler.remove_all_jobs()
        scheduler.shutdown()
