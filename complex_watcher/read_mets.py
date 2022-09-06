#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 13:11:07 2022
- Usage: or_id_from_mets(zipfile)

- Returns:
    cp_id: string
@author: tina
"""
import os
import sys
import json
from shutil import rmtree
from zipfile import ZipFile, BadZipFile
from lxml import etree
from viaa.configuration import ConfigParser
from viaa.observability import logging
from complex_watcher.publisher import PubMsg

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
config = ConfigParser()
logger = logging.get_logger(__name__, config)
pub_err_queue = config.app_cfg['amqpPublisher']['error_queue']
pub_user = config.app_cfg['amqpPublisher']['user']
pub_pass = config.app_cfg['amqpPublisher']['pass']
pub_host = config.app_cfg['amqpPublisher']['host']


def or_id_from_mets(zip_file):
    '''Description:
        - Unzip mets.xml from complex/zip

    returns :
        - or-id: string

        - if mets not found : return None
    '''
    suffix = '_mets.xml'
    base_name = (os.path.basename(zip_file))
    fb_name, ext = os.path.splitext(base_name)
    mets = fb_name + suffix
    logger.debug('extention: %s', ext)
    logger.info('mets.xml: %s', mets)

    try:
        with ZipFile(zip_file) as complex_obj:
            complex_obj.extract(mets, path='.' + mets)
            root = etree.parse(str('.' + mets + '/' + mets))
            cp_id = root.xpath("//CP_id/text()")[0]
    except KeyError as exc:
        logger.error(exc)
        logger.info('_mets.xml not found: %s', mets)
        return None
    except BadZipFile as exc:
        logger.error(str(exc))
        err = {'error': '{}'.format(str(exc)),
               'file': '{}'.format(zip_file)}
        msg = json.dumps(err)
        PubMsg(pub_err_queue, pub_host, pub_user, pub_pass, msg,
               routing_key='complex_err_fxp')()
        return None

    logger.info('cp_id: %s', cp_id)
    rmtree('.' + mets + '/')
    return cp_id
