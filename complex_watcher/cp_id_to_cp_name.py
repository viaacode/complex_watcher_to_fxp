#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:25:28 2022
Description:
    - Gets mam name from or-id using org api
Args:
    - or-id: string
    - env : string
Usage:
    - print(get_mam_name('OR-gm81n50')
Returns:
    - mam name: string
    - On error , returns None
@author: tina
"""
import sys
import os
from string import Template
import requests
from viaa.configuration import ConfigParser
from viaa.observability import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
config = ConfigParser()
org_api_url = config.app_cfg['watcher']['org_api_url']
logger = logging.get_logger(__name__, config)
header = {'Content-Type': 'application/json'}
queryTemplate = Template("""
    {
         organizations(id: "$orid") {
            iri
            id
            mam_label
         }
    }
    """)


def get_mam_name(or_id):
    '''Description:
        - returns the or_ip from org api'''
    query = queryTemplate.substitute(orid=or_id)
    request = requests.post(org_api_url, json={'query': query}, headers=header)
    try:
        if request.status_code == 200:
            _j = request.json()
            req_headers = request.headers
            mam_name = _j['data']['organizations'][0]['mam_label']
            logger.info('org name mam: %s ', str(mam_name))
            logger.debug(str(req_headers))
            return mam_name
        logger.error(request.status_code)
    except TypeError as exc:
        logger.error(str(exc))
        return None
    except IndexError as exc:
        logger.error(str(exc))
        # raise requests.exceptions.HTTPError from exc
        return None


# print(get_mam_name('OR-0z70w1b'))
