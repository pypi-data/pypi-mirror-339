import json
import os
import time

from pymysql import OperationalError, MySQLError
from importers.common.common_util import mysql_connect, get_all_file, remove_file, getVariables
from importers.common.config_util import get_temp_dir_from_config
from importers.common.http_util import send_restful_get
from importers.common.log_util import logger, my_logger
from importers.data_import.data_events import events_import_send
from importers.data_import.data_format_util import validate_data_event, load_sql_queries
from importers.data_import.data_item_variable import item_variables_import_send
from importers.data_import.data_model import EventsJson, DataEvent, DataUser, UserVariablesJson, DataItem, \
    ItemVariablesJson
from importers.data_import.data_user_variable import user_variables_import_send
from importers.meta.data_center import getBindEvent, getdataCenterUserVariables, getdataCenterEventVariables


def event_mysql_import(args, start, end):
    """
       行为数据导入 ，MYSQL数据源
    """
    try:
        conn = mysql_connect(user=args.get('user'), password=args.get('password'), host=args.get('host'),
                             port=int(args.get('port')), database=args.get('database'))
    except (MySQLError, OperationalError):
        logger.error(" MYSQL连接失败。")
        exit(-1)
    temp_dir = get_temp_dir_from_config()  # 获取临时存储目录
    current_tmp_path = os.path.join(temp_dir, str(int(round(time.time() * 1000))))
    if not os.path.exists(current_tmp_path):
        os.makedirs(current_tmp_path)
    my_logger.info(f"临时存储Json文件目录：[{current_tmp_path}]")
    job_name = args.get('jobName') or f"Python_events_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}"
    # 检查是否传入SQL文件或单条SQL
    sql_queries = load_sql_queries(args.get('sql_file'), args.get('sql'))
    total_count = 0
    cursor = conn.cursor()
    for index, sql in enumerate(sql_queries):
        sql = sql.strip()
        if not sql:
            continue
        my_logger.info(f"执行第 {index + 1} 条SQL: {sql}")
        try:
            cursor.execute(sql)
            my_logger.info(f"SQL执行成功: {sql}")
        except (MySQLError, OperationalError) as e:
            logger.error(f"请检查 SQL 语句: {sql}, 错误信息: {e}")
            exit(-1)
        desc = cursor.description
        desc_list = [d[0] for d in desc]
        if 'event' not in desc_list or 'timestamp' not in desc_list:
            logger.error("event或timestamp字段不存在")
            exit(-1)
        if 'userId' not in desc_list and 'userkey' not in desc_list:
            logger.error("缺少userId需指定\n若传主体事件,则数据需字段userKey,且值为‘$notuser’")
            exit(-1)

        json_file_abs_path = os.path.join(current_tmp_path, f'tmp_events_{index + 1}.json')
        event = getBindEvent()
        cstm_keys = {i['key']: [a['key'] for a in i['attributes']] for i in event['dataCenterCustomEvents']}
        cstm_attr_keys = getVariables(getdataCenterEventVariables())
        attr_all = send_restful_get()

        try:
            start_time = time.time()
            wf = open(json_file_abs_path, 'w')
            cnt = 0
            count = 0
            while True:
                batch = cursor.fetchmany(size=args.get('batch'))
                cnt += 1
                if len(batch) == 0 and cnt == 1:
                    my_logger.info(f"该任务{job_name}查询数据为空")
                    break
                elif len(batch) == 0:
                    end_time = time.time()
                    cost_time = end_time - start_time
                    my_logger.info(f"读取SQL数据,并写入{count}条数据临时文件，耗时: {cost_time:.3f}秒")
                    break
                else:
                    for row in batch:
                        tmp = {}
                        var = {}
                        userId_present = True
                        for a in range(len(row)):
                            if desc_list[a] == 'event' or desc_list[a] == 'timestamp':
                                tmp[desc_list[a]] = row[a]
                            elif desc_list[a] == 'userId':
                                userId_present = False
                                tmp['userId'] = row[a]
                            elif desc_list[a] == 'eventId' and row[a] != '':
                                tmp['eventId'] = row[a]
                            elif desc_list[a] == 'userKey' and row[a] != '':
                                tmp['userKey'] = row[a]
                            else:
                                var[desc_list[a]] = row[a]
                        tmp['attrs'] = var
                        if userId_present:
                            if tmp['userKey'] == '$notuser':
                                tmp['userId'] = ''
                            else:
                                logger.error("导入主体事件时,userKey的值不是$notuser")
                                exit(-1)

                        data_event = DataEvent(
                            userId=tmp.get('userId', ''),
                            event=tmp['event'],
                            timestamp=tmp['timestamp'],
                            attrs=tmp['attrs'],
                            userKey=tmp.get('userKey', ''),
                            eventId=tmp.get('eventId', None)
                        )
                        if args.get('debug'):
                            is_valid, error_message = validate_data_event(
                                data_event, start, end, attr_all, cstm_keys, cstm_attr_keys)
                            if not is_valid:
                                logger.error(f"{error_message}")
                                exit(-1)
                        wf.write(json.dumps(data_event.__dict__, ensure_ascii=False))
                        wf.write('\n')
                        count += 1
                        if count % 2000000 == 0:
                            my_logger.info(f"已经写入{count}条数据进临时文件......")
                    wf.flush()
            total_count += count
        finally:
            wf.close()

    cursor.close()
    conn.close()
    if total_count > 0:
        events_import_send(
            EventsJson(name='events',
                       path=get_all_file(current_tmp_path),
                       format='JSON',
                       debug=False,
                       eventStart=start,
                       eventEnd=end,
                       datasourceId=args.get('datasource_id'),
                       jobName=job_name,
                       clear=False
                       )
        )
    else:
        my_logger.info("本次任务数据为空，故不生成导数任务。")
    remove_file(current_tmp_path)


def user_mysql_import(args):
    """
       用户属性导入，MYSQL数据源
    """
    try:
        conn = mysql_connect(user=args.get('user'), password=args.get('password'), host=args.get('host'),
                             port=int(args.get('port')), database=args.get('database'))
    except (MySQLError, OperationalError):
        logger.error("MYSQL连接失败。")
        exit(-1)

    temp_dir = get_temp_dir_from_config()  # 获取临时存储目录
    current_tmp_path = os.path.join(temp_dir, str(int(round(time.time() * 1000))))
    if not os.path.exists(current_tmp_path):
        os.makedirs(current_tmp_path)
    my_logger.info(f"临时存储Json文件目录：[{current_tmp_path}]")
    # 检查是否传入SQL文件或单条SQL
    sql_queries = load_sql_queries(args.get('sql_file'), args.get('sql'))

    keys = getVariables(getdataCenterUserVariables())
    job_name = args.get('jobName') or f"Python_user_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}"
    total_count = 0
    cursor = conn.cursor()

    for index, sql in enumerate(sql_queries):
        sql = sql.strip()
        if not sql:
            continue
        my_logger.info(f"执行第 {index + 1} 条SQL: {sql}")

        try:
            cursor.execute(sql)
            my_logger.info(f"SQL执行成功: {sql}")
        except (MySQLError, OperationalError) as e:
            logger.error(f"请检查 SQL 语句: {sql}, 错误信息: {e}")
            exit(-1)

        desc = cursor.description
        desc_list = [d[0] for d in desc]
        if 'userId' not in desc_list:
            logger.error("userId字段不存在")
            exit(-1)
        json_file_abs_path = os.path.join(current_tmp_path, f'tmp_user_{index + 1}.json')
        try:
            start_time = time.time()
            wf = open(json_file_abs_path, 'w')
            cnt = 0
            count = 0
            first_row_checked = False
            while True:
                cnt += 1
                data = cursor.fetchmany(size=args.get('batch'))
                if len(data) == 0 and cnt == 1:
                    my_logger.info(f"该sql查询结果为空")
                    break
                elif len(data) == 0:
                    end_time = time.time()
                    cost_time = end_time - start_time
                    my_logger.info(f"读取SQL数据,并写入{count}条数据临时文件，耗时: {cost_time:.3f}秒")
                    break
                else:
                    for row in data:
                        res = {}
                        var = {}
                        for a in range(len(row)):
                            if desc_list[a] == 'userId':
                                res['userId'] = row[a]
                            elif desc_list[a] == 'userKey' and row[a] != '':
                                res['userKey'] = row[a]
                            else:
                                var[desc_list[a]] = row[a]
                        res['attrs'] = var
                        if args.get('debug') and not first_row_checked:
                            # 校验未定义的用户属性
                            for key in res['attrs']:
                                if key not in keys and not key.startswith("$"):
                                    logger.error(f"用户属性 {key} 在GIO平台未定义")
                                    exit(-1)
                            if 'userKey' in res and res['userKey'] == '$notuser':
                                logger.error("用户属性导入不支持用户身份为‘$notuser’")
                                exit(-1)
                            first_row_checked = True
                        data_event = DataUser(userId=res['userId'], userKey=res.get('userKey', ''), attrs=res['attrs'])
                        wf.write(json.dumps(data_event.__dict__, ensure_ascii=False))
                        wf.write('\n')
                        count += 1
                        if count % 2000000 == 0:
                            my_logger.info(f"已经写入{count}条数据进临时文件......")
                    wf.flush()
            total_count += count
        finally:
            wf.close()

    cursor.close()
    conn.close()
    if total_count > 0:
        user_variables_import_send(
            UserVariablesJson(name='user_variables',
                              path=get_all_file(current_tmp_path),
                              debug=False,
                              format='JSON',
                              datasourceId=args.get('datasource_id'),
                              jobName=job_name,
                              clear=False)
        )
    else:
        my_logger.info("本次任务数据为空，故不生成导数任务。")
    remove_file(current_tmp_path)


def item_mysql_import(args):
    """
       主体导入，MYSQL数据源
    """
    try:
        conn = mysql_connect(user=args.get('user'), password=args.get('password'), host=args.get('host'),
                             port=int(args.get('port')), database=args.get('database'))
    except (MySQLError, OperationalError):
        logger.error("MYSQL连接失败。")
        exit(-1)

    temp_dir = get_temp_dir_from_config()  # 获取临时存储目录
    current_tmp_path = os.path.join(temp_dir, str(int(round(time.time() * 1000))))
    if not os.path.exists(current_tmp_path):
        os.makedirs(current_tmp_path)
    my_logger.info(f"临时存储Json文件目录：[{current_tmp_path}]")
    if len(str(args.get('jobName'))) == 0 or args.get('jobName') is None:
        job_name = f"Python_item_{time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))}"
    else:
        job_name = args.get('jobName')
    # 检查是否传入SQL文件或单条SQL
    sql_queries = load_sql_queries(args.get('sql_file'), args.get('sql'))
    total_count = 0
    cursor = conn.cursor()

    for index, sql in enumerate(sql_queries):
        sql = sql.strip()
        if not sql:
            continue
        my_logger.info(f"执行第 {index + 1} 条SQL: {sql}")

        try:
            cursor.execute(sql)
            my_logger.info(f"SQL执行成功: {sql}")
        except (MySQLError, OperationalError) as e:
            logger.error(f"请检查 SQL 语句: {sql}, 错误信息: {e}")
            exit(-1)

        desc = cursor.description
        desc_list = [d[0] for d in desc]
        if 'item_id' not in desc_list:
            logger.error("item_id字段不存在")
            exit(-1)
        json_file_abs_path = os.path.join(current_tmp_path, f'{args.get("item_key")}_{index + 1}.json')
        try:
            start_time = time.time()
            wf = open(json_file_abs_path, 'w')
            cnt = 0
            count = 0
            while True:
                cnt += 1
                batch = cursor.fetchmany(size=args.get('batch'))
                if len(batch) == 0 and cnt == 1:
                    my_logger.info(f"该任务{job_name}查询数据为空")
                    break
                elif len(batch) == 0:
                    end_time = time.time()
                    cost_time = end_time - start_time
                    my_logger.info(f"读取SQL数据,并写入{count}条数据临时文件，耗时: {cost_time:.3f}秒")
                    break
                else:
                    for row in batch:
                        res = {}
                        var = {}
                        for a in range(len(row)):
                            if desc_list[a] == 'item_id' and row[a] != '':
                                res['item_id'] = row[a]
                            else:
                                var[desc_list[a]] = row[a]
                        res['attrs'] = var
                        data_item = DataItem(item_id=res['item_id'], attrs=res['attrs'])
                        wf.write(json.dumps(data_item.__dict__, ensure_ascii=False))
                        wf.write('\n')
                        count += 1
                        if count % 2000000 == 0:
                            my_logger.info(f"已经写入{count}条数据进临时文件......")
                    wf.flush()
            total_count += count
        finally:
            wf.close()

    cursor.close()
    conn.close()
    if total_count > 0:
        item_variables_import_send(
            ItemVariablesJson(name='item_variables',
                              path=get_all_file(current_tmp_path),
                              debug=args.get('debug'),
                              format='JSON',
                              datasourceId=args.get('datasource_id'),
                              itemKey=args.get('item_key'),
                              jobName=job_name,
                              clear=False,
                              outputContent=args.get('item_output'))
        )
    else:
        my_logger.info("本次任务数据为空，故不生成导数任务。")
    remove_file(current_tmp_path)
