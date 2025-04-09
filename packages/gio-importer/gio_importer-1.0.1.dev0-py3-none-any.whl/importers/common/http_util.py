#!/bin/env python3
# -*- coding: UTF-8 -*-
import os
import subprocess

import curlify
import requests

import urllib3
import json
import logging

from importers.common.config_util import ApiConfig, SaasConfig, SSLConfig

http = urllib3.PoolManager()


def send_graphql_post(body):
    """
     graphql post请求
    :param body: 请求graphql body
    :return: 响应数据
    """
    headers = {'Content-Type': 'application/json', 'Authorization': ApiConfig.token,
               'X-Project-Id': ApiConfig.project_id,
               'X-Product-Unique-Id': 'DC', 'User-Agent': 'gio-importer'}
    r = requests.post(ApiConfig.oauth2_uri+ "/v3/graphql" , headers=headers, data=body, verify=SSLConfig.verify)
    logging.debug('request curl: {}'.format(curlify.to_curl(r.request)))
    if r.status_code == 200:
        content = json.loads(r.content)
        if content["data"] is not None:
            return content['data']
        else:
            logging.error('Graphql请求错误,{}'.format(content['errors']))
            exit(-1)
    else:
        # logging.error(r.status_code)
        logging.error('response content: {}'.format(r.content.decode('utf-8')))
        logging.error('response curl: {}'.format(curlify.to_curl(r.request)))
        re = input("Graphql请求超时或失败,建议检查配置文件的相关token或是否重新请求，请输入yes/no:")
        if str(re).lower() == 'yes':
            send_graphql_post(body)
        else:
            return


def send_restful(url, method, body=None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': ApiConfig.token,
        'X-Project-Id': ApiConfig.project_id,
        'X-Product-Unique-Id': 'DC',
        'User-Agent': 'gio-importer'
    }

    try:
        if method.lower() == 'post':
            response = requests.post(url, headers=headers, json=body, verify=SSLConfig.verify)
        elif method.lower() == 'put':
            response = requests.put(url, headers=headers, json=body, verify=SSLConfig.verify)
        elif method.lower() == 'get':
            response = requests.get(url, headers=headers, verify=SSLConfig.verify)
        else:
            logging.error(f'Unsupported method: {method}')
            return

        # logging.info(f'request curl: {curlify.to_curl(response.request)}')

        if response.status_code == 200:
            content = response.json()
            if content.get("data") is not None:
                return content['data']
            else:
                logging.error(f'restful请求错误, {content.get("errors", "No error message")}')
                exit(-1)
        else:
            logging.error(f'response content: {response.content.decode("utf-8")}')
            logging.error(f'response curl: {curlify.to_curl(response.request)}')
            re = input("restful请求超时或失败,建议检查配置文件的相关token或是否重新请求，请输入yes/no:")
            if str(re).lower() == 'yes':
                send_restful(url, method, body)
            else:
                return
    except requests.exceptions.RequestException as e:
        logging.error(f'Request failed: {e}')
        return


def send_rest_get(url, params):
    """
     http post请求
    :param url: 请求url
    :param params: 请求参数
    :return: 响应数据
    """
    headers = {'Content-Type': 'application/json', 'Authorization': SaasConfig.token}
    # headers = {'Content-Type': 'application/json'}
    r = requests.get(SaasConfig.uri + url, headers=headers, params=params)
    if r.status_code == 200:
        content = json.loads(r.text)
        return content


def put_file_ftp(file_list, target_directory):
    headers = {'Authorization': 'Bearer ' + ApiConfig.token}
    for file in file_list:
        file_splits = file.split('/')
        simple_name = file_splits[len(file_splits) - 1]
        with open(file, 'rb') as fp:
            file_data = fp.read()
            http.request('POST', ApiConfig.oauth2_uri + '/upload', headers=headers,
                         fields={'file': (simple_name, file_data), 'path': target_directory})


def put_file_hdfs(file_list, target_directory):
    for file in file_list:
        os.system(f"hdfs dfs -put {file} {target_directory}")