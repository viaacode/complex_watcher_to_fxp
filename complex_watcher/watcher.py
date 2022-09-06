#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:05:56 2022
Kind:

    - watchfolder for complex

Discription:
    - Daemon inotify watchfolder
    - Create a msg for fxp when a .complex file is closed on dir
Target:
    - meemoo fxp rabbit consumer : https://github.com/viaacode/fxp_service.git
@author: tina
"""
import os
import sys
import json
from string import Template
import inotify.adapters
import inotify
from viaa.configuration import ConfigParser
from viaa.observability import logging
from complex_watcher.publisher import PubMsg
from complex_watcher.read_mets import or_id_from_mets
from complex_watcher.cp_id_to_cp_name import get_mam_name

config = ConfigParser()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
logger = logging.get_logger('watcher', config)
dest_host = config.app_cfg['watcher']['dest_host']
dest_user = config.app_cfg['watcher']['dest_user']
dest_pass = config.app_cfg['watcher']['dest_pass']
source_host = config.app_cfg['watcher']['source_host']
source_user = config.app_cfg['watcher']['source_user']
source_pass = config.app_cfg['watcher']['source_pass']
dest_path = config.app_cfg['watcher']['dest_path']
dirname = config.app_cfg['watcher']['source_path']
pub_user = config.app_cfg['amqpPublisher']['user']
pub_pass = config.app_cfg['amqpPublisher']['pass']
pub_host = config.app_cfg['amqpPublisher']['host']
pub_queue = config.app_cfg['amqpPublisher']['queue']
pub_err_queue = config.app_cfg['amqpPublisher']['error_queue']
fxpTemplate = Template("""
                         {
                               "destination_file": "$Filename",
                               "destination_host": "$Dhost",
                               "destination_password": "$Dpass",
                               "destination_path": "$Dpath",
                               "destination_user": "$Duser",
                               "source_file": "$Sfile",
                               "source_host": "$Shost",
                               "source_password": "$Spass",
                               "source_path": "$Spath",
                               "source_user": "$Suser",
                               "move": false
                             }
                         """)


def __main__():
    """Watch a dir in dirname = config.app_cfg['watcher']['source_path']:

            - If file is closed send a fxp msg with the publisher.py

    """
    i = inotify.adapters.Inotify()
    i.add_watch((dirname))
    logger.info('Watching dir : %s', dirname)
    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                logger.debug(str(type_names) + ',' + str(filename))
                logger.debug(str(header))
                # file is closed
                if type_names == ['IN_CLOSE_WRITE']:
                    filepath = watch_path + filename
                    ext = os.path.splitext(filepath)[1]
                    # get the extention
                    if ext in ('.complex', '.COMPLEX', '.zip', '.zip'):
                        if config.app_cfg['watcher']['read_mets'] is True:
                            # get the or-id for zip
                            logger.info("Reading zip file %s", filepath)
                            cp_id = or_id_from_mets(filepath)
                            logger.debug('OR-id: %s', cp_id)
                            # get the mam name
                            try:
                                cp_name = get_mam_name(cp_id)
                                # failed to get cp name from mam
                                if cp_name is None:
                                    logger.error('Could not find CP name')
                                    error_msg = {'Error': 'Could not find CP name',
                                                 'file': filepath}
                                    PubMsg(queue=pub_err_queue,
                                           rabhost=pub_host,
                                           user=pub_user,
                                           passwd=pub_pass,
                                           routing_key='complex_err_fxp',
                                           msg=json.dumps(error_msg))()
                                if cp_name:
                                    org_dest_path = '/' + cp_name
                                    msg = fxpTemplate.substitute(
                                        Filename=filename,
                                        Dhost=dest_host,
                                        Dpass=dest_pass,
                                        Dpath=org_dest_path,
                                        Duser=dest_user,
                                        Sfile=filename,
                                        Shost=source_host,
                                        Spass=source_pass,
                                        Spath=dirname,
                                        Suser=source_user)
                                    logger.info(
                                        "Publish msg for file: %s", filename)
                                    PubMsg(queue=pub_queue,
                                           rabhost=pub_host,
                                           user=pub_user,
                                           passwd=pub_pass,
                                           routing_key='complex_fxp',
                                           msg=msg)()
                            except TypeError as exc:
                                error_msg = {"Error": "{}".format(str(exc)),
                                             "file": "{}".format(filepath)
                                             }
                                logger.error("Failed to get cp name",
                                             data=error_msg)
                                PubMsg(queue=pub_err_queue,
                                       rabhost=pub_host,
                                       user=pub_user,
                                       passwd=pub_pass,
                                       msg=json.dumps(error_msg),
                                       routing_key='complex_err_fxp')()
                        if config.app_cfg['watcher']['read_mets'] is False:
                            msg = fxpTemplate.substitute(Filename=filename,
                                                         Dhost=dest_host,
                                                         Dpass=dest_pass,
                                                         Dpath=dest_path,
                                                         Duser=dest_user,
                                                         Sfile=filename,
                                                         Shost=source_host,
                                                         Spass=source_pass,
                                                         Spath=dirname,
                                                         Suser=source_user
                                                         )
                            logger.info(
                                "Publish msg for file: %s", filename)
                            PubMsg(queue=pub_queue,
                                   rabhost=pub_host,
                                   user=pub_user,
                                   passwd=pub_pass,
                                   routing_key='complex_fxp',
                                   msg=msg)()

    finally:
        # remove the watch on the folders
        i.remove_watch = dirname
        logger.info('Removing watch on dir : %s', dirname)


if __name__ == '__main__':
    __main__()
