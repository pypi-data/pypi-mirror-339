#!/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (c) 2020 growingio.com, Inc.  All Rights Reserved
import argparse
import pathlib
import sys

project_root = str(pathlib.Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from importers.db_import.database_import import events, user_variables, item_variables
from importers.common.config_util import ApiConfig
from importers.common.log_util import logger, my_logger
from importers.meta.meta_create import *


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m',
                        help='必填参数. 事件events，用户属性user_variables，主体数据导入item_variables.',
                        required=True,
                        type=str)
    parser.add_argument('-ds', '--datasource_id',
                        help='必填参数. 数据源ID.',
                        required=True,
                        type=str)
    parser.add_argument('-item_key',
                        help='必填参数. item_key',
                        required=False,  # 根据-m参数判断是否必填
                        default='',
                        type=str)
    parser.add_argument('-f', '--format',
                        help='可选参数. 导入数据格式,目前支持mysql、hive格式.',
                        type=str,
                        metavar="")
    parser.add_argument('-db_host', '--host',
                        help='必填参数. 客户数据源地址',
                        metavar="")
    parser.add_argument('-db_user', '--user',
                        help='必填参数. 客户数据源用户',
                        type=str,
                        metavar="")
    parser.add_argument('-db_pass', '--password',
                        help='必填参数. 客户数据源密码',
                        type=str,
                        metavar="")
    parser.add_argument('-db_port', '--port',
                        help='必填参数. 客户数据源端口',
                        metavar="")
    parser.add_argument('-sql', '--sql',
                        help='可选参数. sql语句',
                        type=str,
                        metavar="")
    parser.add_argument('-sf', '--sql_file',
                        help='可选参数. sql语句文件',
                        default='',
                        type=str)
    parser.add_argument('-b', '--batch',
                        help='可选参数. hive模式下每批次处理多少条数据',
                        type=int,
                        default=1000,
                        metavar="")
    parser.add_argument('-s', '--start_time',
                        help='用户行为数据必选参数. 开始时间',
                        metavar="")
    parser.add_argument('-e', '--end_time',
                        help='用户行为数据必选参数. 结束时间',
                        metavar="")
    parser.add_argument('-j', '--jobName',
                        help='指定导入任务名称',
                        metavar="")
    parser.add_argument('-c', '--clear',
                        help='可选参数. True-导入数据成功后清理掉FTP上数据,False-导入数据成功后不清理掉FTP上数据.',
                        default=False)
    parser.add_argument('-at', '--auth',
                        help='可选参数. hive认证方式',
                        type=str,
                        default=None,
                        metavar="")
    parser.add_argument('-db', '--database',
                        help='可选参数. 指定数据库',
                        type=str,
                        default='',
                        metavar="")
    parser.add_argument('-pc', '--principal',
                        help='可选参数. Kerberos 主体名称',
                        type=str,
                        default="",
                        metavar="")
    parser.add_argument('-kt', '--keytab',
                        help='可选参数. Kerberos凭证',
                        type=str,
                        default='',
                        metavar="")
    parser.add_argument('-item_op', '--item_output',
                        help='可选参数. True-主体属性为空打印输出,false-主体属性为空不打印',
                        default=True)
    parser.add_argument('-pi', '--projectId',
                        help='可选参数. 选择导入项目',
                        default='',
                        type=str)
    parser.add_argument('-token', '--token',
                        help='可选参数. 选择账号token',
                        default='',
                        type=str)
    parser.add_argument('-d', '--debug',
                        help='可选参数. True-导入数据全量校验,false-不校验数据是否平台定义立即创建导入任务进入导入队列.',
                        default=True)
    args = parser.parse_args()
    return args.__dict__


def execute_importer(args):
    ApiConfig.load_from_args(token=args.get('token'), project_id=args.get('projectId'))

    tunnels = getTunnels()
    m = args.get('m')
    if args.get('datasource_id') not in tunnels:
        logger.error("数据源不存在")
        exit(-1)
    args['datasource_id'] = [args.get('datasource_id'), tunnels[args.get('datasource_id')]]
    # 2. 校验Debug参数
    d = str(args.get('debug')).upper()
    if 'TRUE'.__eq__(d):
        d = True
    elif 'FALSE'.__eq__(d):
        my_logger.info("离线导入工具该任务数据跳过校验")
        d = False
    else:
        logger.error("[-d/--debug]参数值不对")
        exit(-1)
    args['debug'] = d
    f = args.get('format')
    database = args.get("database")
    if 'MYSQL'.__eq__(str(f).upper()):
        database = 'information_schema' if database == '' else database
    elif 'HIVE'.__eq__(str(f).upper()):
        database = 'default' if database == '' else database
        auth = args.get("auth")
        password = args.get('password') if auth in ['LDAP', 'CUSTOM'] else None
        args['password'] = password
    else:
        logger.error("format不在取值范围内")
        exit(-1)
    args['database'] = database

    op = str(args.get('item_output')).upper()
    if 'TRUE'.__eq__(op):
        op = True
    elif 'FALSE'.__eq__(op):
        op = False
    else:
        logger.error("[-item_op/--item_output]参数值不对")
        exit(-1)
    args['item_output'] = op
    if 'events'.__eq__(m):
        events(args)
    elif 'user_variables'.__eq__(m):
        user_variables(args)
    elif 'item_variables'.__eq__(m):
        item_variables(args)
    else:
        logging.error("请确认填写项目名！")
        exit(-1)


def do_importer(params):
    my_logger.info("Data Importer Start")
    # 设置默认参数值
    default_params = {
        'm': None,  # 必填参数, 没有默认值
        'datasource_id': None,  # 必填参数, 没有默认值
        'item_key': '',  # 默认为空字符串
        'format': None,  # 可选参数, 没有默认值
        'host': None,  # 必填参数, 没有默认值
        'user': None,  # 必填参数, 没有默认值
        'password': None,  # 必填参数, 没有默认值
        'port': None,  # 必填参数, 没有默认值
        'sql': None,  # 可选参数, 没有默认值
        'sql_file': None,  # 可选参数, 没有默认值
        'batch': 100000,  # 默认为 100000
        'start_time': None,  # 用户行为数据必选参数, 没有默认值
        'end_time': None,  # 用户行为数据必选参数, 没有默认值
        'jobName': None,  # 可选参数, 没有默认值
        'clear': False,  # 默认为 False
        'auth': None,  # 可选参数, 默认值为None
        'database': '',  # 默认为空字符串
        'principal': '',  # 默认为空字符串
        'keytab': '',  # 默认为空字符串
        'item_output': True,
        'token': '',  # 默认为空字符串
        'projectId': '',  # 默认为空字符串
        'debug': True # 默认为 True
    }

    combined_params = {**default_params, **params}
    # 如果 params 中有相同的键，则 params 的值会覆盖 default_params 中的默认值
    execute_importer(combined_params)
    my_logger.info("Data Importer Finish")


def main():
    args = parse_args()
    execute_importer(args)


if __name__ == '__main__':
    my_logger.info("Data Importer Start")
    main()
    my_logger.info("Data Importer Finish")
