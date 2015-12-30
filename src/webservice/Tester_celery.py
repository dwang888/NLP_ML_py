'''
Created on Dec 22, 2015

@author: lingandcs
'''
from tasks import add
from celery import Celery


if __name__ == '__main__':
    result = add.delay(4, 4)
#     print result.get(timeout=8)
    print result.backend