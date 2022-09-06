#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:21:11 2022


- Usage:

    msg=json.dumps({'test':'result'})
    o = pubMsg(queue='test',rabhost='host.com',
           user='UUUUU',
           passwd='XXXXXX',
           msg=msg)
    print(o())

@author: tina
"""
import os
import sys
from viaa.observability import logging
from viaa.configuration import ConfigParser
from pika import BlockingConnection, ConnectionParameters, BasicProperties,\
    PlainCredentials
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

config_ = ConfigParser()
LOGGER = logging.get_logger('watcher', config_)


class PubMsg():
    """Publish a message to a queue with exchange and routing key"""

    def __init__(self, queue, rabhost,
                 user, passwd, msg, routing_key='complex_fxp',
                 vhost='/'):
        self.queue = queue
        self.host = rabhost
        self.topic_type = 'topic'
        self.user = user
        self.passwd = passwd
        self.result_exchange = 'fxp'
        self.publish_connection = BlockingConnection(
            ConnectionParameters(host=self.host,
                                 port=5672,
                                 virtual_host=vhost,
                                 retry_delay=3,
                                 connection_attempts=60,
                                 credentials=PlainCredentials(self.user,
                                                              self.passwd)))
        self.publish_channel = self.publish_connection.channel()
        self.result_routing = routing_key
        self.msg = msg
        self.publish_channel.queue_declare(queue=self.queue, passive=False,
                                           durable=True, exclusive=False,
                                           auto_delete=False,
                                           arguments={"x-max-priority": 10})

    def __call__(self):
        if self.queue is not None\
                and self.topic_type is not None:
            self.publish_channel.\
                exchange_declare(exchange='fxp')

            self.publish_channel.queue_bind(queue=self.queue,
                                            exchange=self.result_exchange,
                                            routing_key=self.result_routing)
            self.publish_channel.basic_publish(exchange=self.result_exchange,
                                               routing_key=self.result_routing,
                                               body=self.msg,
                                               properties=BasicProperties(
                                                   content_type='application/json',
                                                   delivery_mode=1))
        LOGGER.info('Message published to exchange: %s with routing key: %s to queue: %s',
                    self.result_exchange, self.result_routing, self.queue)
        self.publish_connection.close()
        return True
