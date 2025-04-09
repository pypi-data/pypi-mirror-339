#!/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (c) 2020 growingio.com, Inc.  All Rights Reserved

import ftplib
import json
import csv
import time
import paramiko

from importers.common.common_util import time_format
from importers.common.config_util import FTPConfig, BaseConfig, ApiConfig, FILE_UPLOAD_TYPE, SFTPConfig
from collections import Counter
from importers.common.log_util import logger, my_logger
from importers.data_import.data_model import DataEvent


def check_sv_header_col_value(attr_header_list):
    """
       校验CSV/TSV格式数据头-固定列数的值
    """
    error_list = []

    required_cols = ['event', 'timestamp']

    for col in required_cols:
        if col not in attr_header_list:
            error_list.append(col)

    return error_list


def check_sv_header_col_count(attr_header_list, data_header_list):
    """
       校验CSV/TSV格式数据头-列数
    """
    if len(attr_header_list) != len(data_header_list):
        return False


def check_sv_header_col_order(attr_header_list, data_header_list):
    """
       校验CSV/TSV格式数据头-不为''的顺序
    """
    try:
        for i in range(len(attr_header_list)):
            if attr_header_list[i] != '' and attr_header_list[i] != data_header_list[i]:
                return False
    except Exception:
        return False


def check_sv_col_duplicate(data_list):
    """
       校验CSV/TSV格式数据列名是否重复
    """
    for item in Counter([i for i in data_list if i != '']).items():
        if item[1] > 1:
            return item[0]


def check_csv_header_col_count(cols, line, separator):
    # 创建一个CSV reader
    csv_reader = csv.reader([line], delimiter=separator, quotechar='"')
    columns = next(csv_reader)
    if len(columns) != len(cols):
        return False

    for col_index, col_value in enumerate(columns):
        try:
            json.loads(col_value)
            return True  # 如果成功解析JSON数据，则返回True
        except json.JSONDecodeError:
            continue

    return False


def get_separator(file_type: str, separator: str) -> str:
    """
    根据文件类型 (CSV/TSV) 和用户指定的分隔符

    :param file_type: 文件类型 ('CSV' 或 'TSV')
    :param separator: 用户提供的分隔符
    :return: 默认分隔符
    """
    if file_type == 'CSV':
        return separator.replace("\\t", "\t") if separator == "\\t" else (',' if separator == '' else separator)
    elif file_type == 'TSV':
        return '\t' if separator == '' else separator
    return separator


def add_header_to_file(file_path, header_columns, separator):
    """
    向文件添加表头。

    :param file_path: 要修改的文件路径。
    :param header_columns: 表头列名的列表。
    :param separator: 列分隔符。
    """
    with open(file_path, 'r', encoding='utf8') as file:
        original_content = file.read()

    with open(file_path, 'w', encoding='utf8') as file:
        header = separator.join(header_columns) + '\n'
        file.write(header + original_content)


def remove_first_line_from_csv(original_file, output_file=None):
    """
    删除向文件添加的表头。
    """
    if output_file is None:
        output_file = original_file

    with open(original_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(lines[1:])


def load_sql_queries(sql_file=None, sql=None):
    """
    从文件路径或SQL字符串中加载SQL查询。
    """
    if sql_file is not None and sql_file.strip() != '':
        with open(sql_file, 'r') as file:
            sql_queries = file.read().split(';')
    else:
        sql_queries = [sql]

    return sql_queries


def replace_first_line_with_header(file_path, header_columns, separator):
    """
    替换文件的第一行为新的表头。

    :param file_path: 要修改的文件路径。
    :param header_columns: 新表头列名的列表。
    :param separator: 列分隔符。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 生成新的表头
    header = separator.join(header_columns) + '\n'
    # 替换第一行
    lines[0] = header
    # 将修改后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def put_file(file_list, target_directory, max_retries=3, retry_interval=5):
    """
    FTP/SFTP上传文件，并在失败时重试
    :param file_list: 待上传文件列表
    :param target_directory: 目标目录
    :param max_retries: 最大重试次数
    :param retry_interval: 重试间隔时间（秒）
    :return:
    """

    def upload_via_ftp(file_list, target_directory):
        """通过FTP上传文件"""
        for file in file_list:
            retries = 0
            while retries <= max_retries:
                try:
                    with ftplib.FTP() as ftp:
                        ftp.connect(host=FTPConfig.host, port=int(FTPConfig.port))
                        ftp.login(user=FTPConfig.user, passwd=FTPConfig.password)
                        file_name = file.split('/')[-1]
                        with open(file, 'rb') as fp:
                            ftp.storbinary(f'STOR {target_directory}/{file_name}', fp)
                    break
                except Exception as e:
                    logger.error(f'上传文件{file}至FTP失败: {e}')
                    retries += 1
                    if retries > max_retries:
                        logger.error(f'文件{file}达到最大重试次数，上传失败。')
                        raise e
                    else:
                        my_logger.info(f'重试上传文件{file}, 尝试次数: {retries}')
                        time.sleep(retry_interval)

    def upload_via_sftp(file_list, target_directory):
        """通过SFTP上传文件"""
        for file in file_list:
            retries = 0
            while retries <= max_retries:
                try:
                    with paramiko.Transport((SFTPConfig.host, int(SFTPConfig.port))) as transport:
                        transport.connect(username=SFTPConfig.user, password=SFTPConfig.password)
                        with paramiko.SFTPClient.from_transport(transport) as sftp:
                            file_name = file.split('/')[-1]
                            sftp.put(file, f'/admin{target_directory}/{file_name}')
                    break
                except Exception as e:
                    logger.error(f"上传文件 {file} 至 SFTP 失败: {e}")
                    retries += 1
                    if retries > max_retries:
                        logger.error(f'文件{file}达到最大重试次数，上传失败。')
                        raise e
                    else:
                        my_logger.info(f'重试上传文件{file}, 尝试次数: {retries}')
                        time.sleep(retry_interval)

    upload_via_ftp_flag = FILE_UPLOAD_TYPE.upload_choose.lower() == 'true'

    if upload_via_ftp_flag:
        ftp_start_time = time.time()
        upload_via_ftp(file_list, target_directory)
        ftp_end_time = time.time()
        ftp_cost_time = ftp_end_time - ftp_start_time
        my_logger.info("文件上传至FTP耗时: %.3f秒" % ftp_cost_time)
    else:
        sftp_start_time = time.time()
        upload_via_sftp(file_list, target_directory)
        sftp_end_time = time.time()
        sftp_cost_time = sftp_end_time - sftp_start_time
        my_logger.info("文件上传至SFTP耗时: %.3f秒" % sftp_cost_time)


def delete_file(file_list, target_directory):
    """
    删除FTP/SFTP服务器上的文件
    :param file_list: 待删除文件列表
    :param target_directory: 目标目录
    :return:
    """

    def delete_via_ftp(file_list, target_directory):
        """通过FTP删除文件"""
        try:
            with ftplib.FTP() as ftp:
                ftp.connect(host=FTPConfig.host, port=int(FTPConfig.port))
                ftp.login(user=FTPConfig.user, passwd=FTPConfig.password)
                for file in file_list:
                    file_name = file.split('/')[-1]
                    ftp.delete(f'{target_directory}/{file_name}')
        except Exception as e:
            logger.error(f'从FTP删除文件失败: {e}')
            raise e

    def delete_via_sftp(file_list, target_directory):
        """通过SFTP删除文件"""
        try:
            with paramiko.Transport((SFTPConfig.host, int(SFTPConfig.port))) as transport:
                transport.connect(username=SFTPConfig.user, password=SFTPConfig.password)
                with paramiko.SFTPClient.from_transport(transport) as sftp:
                    for file in file_list:
                        file_name = file.split('/')[-1]
                        sftp.remove(f'/admin{target_directory}/{file_name}')
        except Exception as e:
            logger.error(f'从SFTP删除文件失败: {e}')
            raise e

    delete_via_ftp_flag = FILE_UPLOAD_TYPE.upload_choose.lower() == 'true'

    if delete_via_ftp_flag:
        delete_via_ftp(file_list, target_directory)
    else:
        delete_via_sftp(file_list, target_directory)


def extract_and_validate_data(json_data):
    error_message = ""
    # 检查 userKey 字段，如果存在且值为 $notuser，则不需要 userId
    if json_data.get('userKey') != '$notuser' and 'userId' not in json_data and 'anonymousId' not in json_data:
        error_message += f"缺少userId需指定\n若传主体事件,则数据需字段userKey, 且值为‘$notuser’\n"
        return None, error_message
    # 确保 event,timestamp 字段存在
    elif 'event' not in json_data or 'timestamp' not in json_data:
        error_message += "event或timestamp字段不存在\n"
        return None, error_message

        # 提取字段并创建 DataEvent 对象
    data_event = DataEvent(
        userId=json_data.get('userId', json_data.get('anonymousId', '')),
        event=json_data['event'],
        timestamp=json_data['timestamp'],
        attrs=json_data.get('attrs', {}),
        userKey=json_data.get('userKey', ''),
        eventId=json_data.get('eventId', None),
        dataSourceId=json_data.get('dataSourceId', None)
    )
    return data_event, error_message


def validate_data_event(data_event, eventStart, eventEnd, var_attr_all, cstm_keys, cstm_attr_keys):
    error_message = ""
    normal = True

    event = data_event.event
    var_keys = cstm_keys.get(event)

    if event in ['$exit', '$bounce']:
        normal = False
        error_message += f"事件[{event}]为t+1离线计算生成，不支持导入\n"
    elif event not in cstm_keys:
        normal = False
        error_message += f"事件[{event}]在GIO平台未定义，请先在系统中定义\n"

    if hasattr(data_event, 'attrs'):
        error_message, normal = check_event_attributes(data_event, event, var_attr_all, cstm_attr_keys, var_keys)

    if not hasattr(data_event, 'timestamp'):
        normal = False
        error_message += "缺少timestamp需指定\n"
    else:
        timestamp = 0
        try:
            timestamp = time_format(str(data_event.timestamp), BaseConfig.timezone)
        except Exception:
            normal = False
            error_message += "timestamp格式错误，请参考数据导入帮助文档\n"

        if (timestamp < eventStart or timestamp > eventEnd) and timestamp != 0:
            normal = False
            error_message += "timestamp时间范围不合法\n"

    return normal, error_message


def check_event_attributes(data_event, event, attr_all, cstm_attr_keys, var_keys):
    error_message = ""
    normal = True
    attrs_customize_error = []
    attrs_bind_error = []
    for key in data_event.attrs:
        if key not in attr_all:
            if key not in cstm_attr_keys:
                attrs_customize_error.append(key)
            elif var_keys is not None and key not in var_keys and key is not None:
                attrs_bind_error.append(key)
    if attrs_customize_error:
        error_message += f"事件属性[{attrs_customize_error}]在GIO平台未定义，请先在系统中定义\n"
    if attrs_bind_error:
        error_message += f"不存在事件属性[{attrs_bind_error}]与事件[{event}]的绑定关系\n"
    if len(attrs_customize_error) > 0 or len(attrs_bind_error) > 0:
        normal = False
    return error_message, normal


def count_lines_in_file(paths):
    total_lines = 0
    for path in paths:
        with open(path, 'r') as file:
            lines = sum(1 for line in file)
        total_lines += lines

    return total_lines


def portal_token(new_token):
    """更新 token"""
    ApiConfig.update_token(new_token)
