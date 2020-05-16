# -*- coding:utf-8 -*-
# 日志设置
'''
日志根据level分别存入相应的文件
'''

import logging.config
from logging.handlers import RotatingFileHandler

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s](%(levelname)5s)(%(processName)s|%(threadName)s)(%(process)d|%(thread)d)<%(filename)s:%(lineno)d>: %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file_scopus': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': 'C:/Users/Administrator/Desktop/machine-learning-explore/log_pack/scopus.log',
            'formatter': 'verbose'
        },
        'file_aff1': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': 'C:/Users/Administrator/Desktop/machine-learning-explore/log_pack/aff1.log',
            'formatter': 'verbose'
        },
        'file_aff2': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': 'C:/Users/Administrator/Desktop/machine-learning-explore/log_pack/aff2.log',
            'formatter': 'verbose'
        },
        'file_aff3': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': 'C:/Users/Administrator/Desktop/machine-learning-explore/log_pack/aff3.log',
            'formatter': 'verbose'
        },
        'file_aff4': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'encoding': 'utf-8',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': 'C:/Users/Administrator/Desktop/machine-learning-explore/log_pack/aff4.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'logger_scopus': {
                    'handlers': ['file_scopus', 'console'],
                    'level': 'DEBUG',
                    'propagate': False
        },
        'logger_aff1': {
            'handlers': ['file_aff1', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'logger_aff2': {
            'handlers': ['file_aff2', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'logger_aff3': {
            'handlers': ['file_aff3', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'logger_aff4': {
            'handlers': ['file_aff4', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
})

logger_scopus = logging.getLogger("logger_scopus")
logger_aff1 = logging.getLogger("logger_aff1")
logger_aff2 = logging.getLogger("logger_aff2")
logger_aff3 = logging.getLogger("logger_aff3")
logger_aff4 = logging.getLogger("logger_aff4")
