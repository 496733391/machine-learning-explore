# -*- coding:utf-8 -*-
# 日志设置
'''
日志根据level分别存入相应的文件
'''

import os
import logging
import logging.config
from mathartsys.Config.rootConfig import LOG_PATH_ROOT, LOG_PATH_RS, LOG_PATH_WP, \
    LOG_PATH_DL, LOG_PATH_REPLACEMENT, LOG_PATH_ADV, LOG_PATH_CANCEL

if not os.path.exists(LOG_PATH_ROOT):
    os.makedirs(LOG_PATH_ROOT)


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
        'file_debug': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': os.path.join(LOG_PATH_ROOT, 'debug.log'),
            'formatter': 'verbose'
        },
        'file_rs': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': LOG_PATH_RS,
            'formatter': 'verbose'
        },
        'file_wp': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': LOG_PATH_WP,
            'formatter': 'verbose'
        },
        'file_dl': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': LOG_PATH_DL,
            'formatter': 'verbose'
        },
        'file_replace': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': LOG_PATH_REPLACEMENT,
            'formatter': 'verbose'
        },
        'file_adv': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': LOG_PATH_ADV,
            'formatter': 'verbose'
        },
        'file_cancel': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
            'delay': True,
            'filename': LOG_PATH_CANCEL,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file_debug', 'console'],
            'level': 'DEBUG',
        },

        'logger_rs': {
            'handlers': ['file_rs', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'logger_wp': {
            'handlers': ['file_wp', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'logger_dl': {
                    'handlers': ['file_dl', 'console'],
                    'level': 'DEBUG',
                    'propagate': False
        },
        'logger_replace': {
                    'handlers': ['file_replace', 'console'],
                    'level': 'DEBUG',
                    'propagate': False
        },
        'logger_adv': {
                    'handlers': ['file_adv', 'console'],
                    'level': 'DEBUG',
                    'propagate': False
        },
        'logger_cancel': {
                    'handlers': ['file_cancel', 'console'],
                    'level': 'DEBUG',
                    'propagate': False
        },
    }
})
logger = logging.getLogger(__name__)
logger_rs = logging.getLogger("logger_rs")
logger_wp = logging.getLogger("logger_wp")
logger_dl = logging.getLogger("logger_dl")
logger_replace = logging.getLogger("logger_replace")
logger_adv = logging.getLogger("logger_adv")
logger_cancel = logging.getLogger("logger_cancel")