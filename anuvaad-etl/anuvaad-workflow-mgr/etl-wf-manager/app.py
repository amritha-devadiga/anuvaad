#!/bin/python
import logging
import os
import threading

from logging.config import dictConfig
from controller.wfmcontroller import wfmapp
from kafkawrapper.wfmconsumer import consume
from kafkawrapper.wfmcoreconsumer import core_consume
from kafkawrapper.wfmerrorconsumer import error_consume


log = logging.getLogger('file')
app_host = os.environ.get('ANU_ETL_WFM_HOST', '0.0.0.0')
app_port = os.environ.get('ANU_ETL_WFM_PORT', 5002)


# Starts the kafka consumer in a different thread
def start_consumer():
    with wfmapp.test_request_context():
        try:
            wfmConsumerThread = threading.Thread(target=consume, name='WFMConsumer-Thread')
            wfmCoreConsumerThread = threading.Thread(target=core_consume, name='WFMCoreConsumer-Thread')
            wfmErrorConsumerThread = threading.Thread(target=error_consume, name='WFMErrorConsumer-Thread')
            wfmConsumerThread.start()
            wfmCoreConsumerThread.start()
            wfmErrorConsumerThread.start()
        except Exception as e:
            log.exception("Exception while starting the kafka consumer: " + str(e))


if __name__ == '__main__':
    start_consumer()
    wfmapp.run(host=app_host, port=app_port)


# Log config
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] {%(filename)s:%(lineno)d} %(threadName)s %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'info': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': 'info.log'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'file': {
            'level': 'DEBUG',
            'handlers': ['info', 'console'],
            'propagate': ''
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['info', 'console']
    }
})
