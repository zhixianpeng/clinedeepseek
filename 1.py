#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
故障工单明细导出 - 测试爬取程序
==================================
原则：绝不增加服务器负担
- pageSize 改为 1（仅获取 1 条数据测试）
- 只发一次请求，不做分页/循环
- 单线程同步请求
- 设置合理的 User-Agent
"""

import json
import os
import sys
import time
from datetime import datetime

import requests

# ============================================================
# 配置
# ============================================================
CONFIG_FILE = "config.json"
OUTPUT_DIR = "output"


def load_config():
    """加载配置文件"""
    if not os.path.exists(CONFIG_FILE):
        print(f"[错误] 配置文件 {CONFIG_FILE} 不存在！")
        print(f"请先复制 config.json.example 为 {CONFIG_FILE}，并填入 Cookie。")
        sys.exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    cookie = config.get("cookie", "")
    if not cookie or cookie == "填入从浏览器复制的 Cookie 字符串":
        print("[错误] 请在 config.json 中填入有效的 Cookie！")
        print("获取方式：浏览器 F12 -> Network -> 请求头中复制 Cookie 字段。")
        sys.exit(1)

    return config


def build_payload():
    """构建请求负载（pageSize 改为 1，最小化服务器负担）"""
    payload = {
        "qryCondition": [
            {
                "conditionType": ">=",
                "conditionValue": "20260601",
                "fieldKey": "C202461_1",
                "conditionField": "C202461",
                "physicalColName": "create_date",
                "tableCode": "aaa",
                "accountPeriodFlag": None,
                "keepingTree": False,
                "conditionName": "创建日期",
                "conditionId": 202461,
                "useInWhere": "true",
                "controlType": None,
                "fieldValue": None,
                "dateConditionShow": False,
                "queryAllChildren": False,
                "dateType": 1,
                "dateExportFormat": "yyyyMMdd",
                "dateFlag": "Y",
                "valueAccountFlag": False,
                "dateDisplayFormat": "",
                "rangeType": "month",
                "conditionFieldAliasName": "故障时间_开始时间",
                "conditionAliasName": "create_date_start",
                "dateFormatToDisplay": "YYYYMMDD"
            },
            {
                "conditionType": "<=",
                "conditionValue": "20260630",
                "fieldKey": "C202461_1",
                "conditionField": "C202461",
                "physicalColName": "create_date",
                "tableCode": "aaa",
                "accountPeriodFlag": None,
                "keepingTree": False,
                "conditionName": "创建日期",
                "conditionId": 202461,
                "useInWhere": "true",
                "controlType": None,
                "fieldValue": None,
                "dateConditionShow": False,
                "queryAllChildren": False,
                "dateType": 1,
                "dateExportFormat": "yyyyMMdd",
                "dateFlag": "Y",
                "valueAccountFlag": False,
                "dateDisplayFormat": "",
                "rangeType": "month",
                "conditionFieldAliasName": "故障时间_结束时间",
                "conditionAliasName": "create_date_end",
                "dateFormatToDisplay": "YYYYMMDD"
            }
        ],
        "qryFields": [
            {
                "componentType": "TB",
                "qryField": {
                    "rowHead": [
                        {"rowId": 202413, "rowName": "工单标题", "fieldCode": "C202413", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202414, "rowName": "工单流水号", "fieldCode": "C202414", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202415, "rowName": "告警名称", "fieldCode": "C202415", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202416, "rowName": "告警编码", "fieldCode": "C202416", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202418, "rowName": "告警专业", "fieldCode": "C202418", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202419, "rowName": "告警地市", "fieldCode": "C202419", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202420, "rowName": "告警区县", "fieldCode": "C202420", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202421, "rowName": "告警乡镇", "fieldCode": "C202421", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202422, "rowName": "告警局站地址", "fieldCode": "C202422", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202423, "rowName": "告警局站机房", "fieldCode": "C202423", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202424, "rowName": "告警设备名称", "fieldCode": "C202424", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202425, "rowName": "告警设备所属专业子网", "fieldCode": "C202425", "cycleCode": "", "axle": "C", "sortType": "ASC", "rowFunction": ""},
                        {"rowId": 202426, "rowName": "告警设备所属网络层级", "fieldCode": "C202426", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202427, "rowName": "告警设备厂家", "fieldCode": "C202427", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202428, "rowName": "告警设备资源信息", "fieldCode": "C202428", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202429, "rowName": "告警接收时间", "fieldCode": "C202429", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202430, "rowName": "告警首次发生时间", "fieldCode": "C202430", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202431, "rowName": "告警最近发生时间", "fieldCode": "C202431", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202432, "rowName": "告警详细描述", "fieldCode": "C202432", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202433, "rowName": "告警级别", "fieldCode": "C202433", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202434, "rowName": "故障级别", "fieldCode": "C202434", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202435, "rowName": "告警补充信息", "fieldCode": "C202435", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202436, "rowName": "告警影响业务类型", "fieldCode": "C202436", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202437, "rowName": "告警影响业务名称", "fieldCode": "C202437", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202438, "rowName": "告警影响客户名称", "fieldCode": "C202438", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202439, "rowName": "告警影响客户等级", "fieldCode": "C202439", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202440, "rowName": "是否群障", "fieldCode": "C202440", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202441, "rowName": "告警关联类型", "fieldCode": "C202441", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202442, "rowName": "关联告警", "fieldCode": "C202442", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202443, "rowName": "预判告警原因", "fieldCode": "C202443", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202444, "rowName": "告警处理截止时间", "fieldCode": "C202444", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202445, "rowName": "告警处理时限倒计时", "fieldCode": "C202445", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202446, "rowName": "智能处理过程", "fieldCode": "C202446", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202473, "rowName": "工单状态", "fieldCode": "C202473", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202447, "rowName": "故障原因一级类别", "fieldCode": "C202447", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202448, "rowName": "故障原因二级类别", "fieldCode": "C202448", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202449, "rowName": "故障原因三级类别", "fieldCode": "C202449", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202450, "rowName": "责任方", "fieldCode": "C202450", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202462, "rowName": "故障处理描述", "fieldCode": "C202462", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202451, "rowName": "派单时间", "fieldCode": "C202451", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202452, "rowName": "接单时间", "fieldCode": "C202452", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202468, "rowName": "综调收到恢复消息时间", "fieldCode": "C202468", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202453, "rowName": "故障恢复时间", "fieldCode": "C202453", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202454, "rowName": "回单时间", "fieldCode": "C202454", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202455, "rowName": "接单时限", "fieldCode": "C202455", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202456, "rowName": "处理时限", "fieldCode": "C202456", "cycleCode": "", "axle": "C", "dateType": 2, "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowFunction": ""},
                        {"rowId": 202467, "rowName": "接单超时", "fieldCode": "C202467", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202472, "rowName": "恢复超时", "fieldCode": "C202472", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202469, "rowName": "接单人单位", "fieldCode": "C202469", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202457, "rowName": "接单人部门", "fieldCode": "C202457", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202458, "rowName": "接单人", "fieldCode": "C202458", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202470, "rowName": "回单人单位", "fieldCode": "C202470", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202459, "rowName": "回单人部门", "fieldCode": "C202459", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202460, "rowName": "回单人", "fieldCode": "C202460", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202463, "rowName": "影响的宽带业务接入号数量", "fieldCode": "C202463", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202464, "rowName": "影响的专线业务接入号数量", "fieldCode": "C202464", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202465, "rowName": "影响的IPTV业务接入号数量", "fieldCode": "C202465", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202466, "rowName": "影响的语音业务接入号数量", "fieldCode": "C202466", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202474, "rowName": "故障回单描述", "fieldCode": "C202474", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 202476, "rowName": "是否上传照片", "fieldCode": "C202476", "cycleCode": "", "axle": "C", "rowFunction": ""},
                        {"rowId": 208160, "rowName": "管控范围", "fieldCode": "C208160", "cycleCode": "", "axle": "C", "rowFunction": ""}
                    ],
                    "columnHead": [
                        {"columnId": 202471, "columnName": "处理时长_分钟", "fieldCode": "C202471", "cycleCode": "", "axle": "C", "columnFunction": "", "fieldAliasCode": "C202471"}
                    ],
                    "summaryHead": [
                        {"summaryName": "处理时长_分钟", "summaryFunction": "SUM", "summaryId": "C202471"}
                    ]
                },
                "filterSql": "",
                "queryType": 0,
                "pageIndex": 1,
                # 关键变更：pageSize 改为 1（原为 7557），绝不增加服务器负担
                "pageSize": 1
            }
        ],
        "fieldIds": "202413,202414,202415,202416,202418,202419,202420,202421,202422,202423,202424,202425,202426,202427,202428,202429,202430,202431,202432,202433,202434,202435,202436,202437,202438,202439,202440,202441,202442,202443,202444,202445,202446,202473,202447,202448,202449,202450,202462,202451,202452,202468,202453,202454,202455,202456,202467,202472,202469,202457,202458,202470,202459,202460,202463,202464,202465,202466,202471,202474,202476,208160",
        "modelId": 50136,
        "tableStructure": [
            {"title": "工单标题", "fieldKey": "C202413", "physicalColName": "fault_title", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "工单流水号", "fieldKey": "C202414", "physicalColName": "order_code", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警名称", "fieldKey": "C202415", "physicalColName": "ALARM_NAME", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警编码", "fieldKey": "C202416", "physicalColName": "ALARM_CODE", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警专业", "fieldKey": "C202418", "physicalColName": "fault_kind_name", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警地市", "fieldKey": "C202419", "physicalColName": "alarm_city", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警区县", "fieldKey": "C202420", "physicalColName": "ALARM_COUNTY", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警乡镇", "fieldKey": "C202421", "physicalColName": "WARNINGCOUNTY", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警局站地址", "fieldKey": "C202422", "physicalColName": "WARNINGADDRESS", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警局站机房", "fieldKey": "C202423", "physicalColName": "ALARM_EXCH", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警设备名称", "fieldKey": "C202424", "physicalColName": "ALARM_EQUIPMENT", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警设备所属专业子网", "fieldKey": "C202425", "physicalColName": "ALARM_NETEQUIPGRADE", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警设备所属网络层级", "fieldKey": "C202426", "physicalColName": "ALARM_NETGRADE", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警设备厂家", "fieldKey": "C202427", "physicalColName": "ALARM_DEVFACTORY", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警设备资源信息", "fieldKey": "C202428", "physicalColName": "ALARM_DEVRESINFO", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警接收时间_秒", "fieldKey": "C202429", "physicalColName": "CREATE_DATE", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "告警首次发生时间_秒", "fieldKey": "C202430", "physicalColName": "ALARM_FIRSTDATE", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "告警最近发生时间_秒", "fieldKey": "C202431", "physicalColName": "ALARM_LASTDATE", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "告警详细描述", "fieldKey": "C202432", "physicalColName": "ALARM_DES", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警级别", "fieldKey": "C202433", "physicalColName": "ALARM_FAULTGRADE", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "故障级别", "fieldKey": "C202434", "physicalColName": "fault_grade_text", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警补充信息", "fieldKey": "C202435", "physicalColName": "ALARM_ADDITIONALINFO", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警影响业务类型", "fieldKey": "C202436", "physicalColName": "ALARM_EFFECTBUSTYPE", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警影响业务名称", "fieldKey": "C202437", "physicalColName": "ALARM_EFFECTBUSNAME", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警影响客户名称", "fieldKey": "C202438", "physicalColName": "ALARM_EFFECTCUSTNAME", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警影响客户等级", "fieldKey": "C202439", "physicalColName": "ALARM_EFFECTCUSTGRADE", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "是否群障", "fieldKey": "C202440", "physicalColName": "IS_LARGE_FAULT", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警关联类型", "fieldKey": "C202441", "physicalColName": "ALARM_RELATETYPE", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "关联告警", "fieldKey": "C202442", "physicalColName": "ALARM_RELATED", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "预判告警原因", "fieldKey": "C202443", "physicalColName": "ALARM_PREDICTREASON", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "告警处理截止时间_秒", "fieldKey": "C202444", "physicalColName": "ALARM_LIMITDATE", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "告警处理时限倒计时", "fieldKey": "C202445", "physicalColName": "ALARM_COUNTDOWN", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "智能处理过程", "fieldKey": "C202446", "physicalColName": "INTELIGENCE_DEAL", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "工单状态", "fieldKey": "C202473", "physicalColName": "CASE \n\tWHEN no2.fault_order_state = '10I' THEN '待接单'\n\tWHEN no2.fault_order_state = '10N' THEN '待回单'\n\tWHEN no2.fault_order_state = '10A' THEN '待结单'\n\tWHEN no2.fault_order_state = '10F' THEN '已完成'\nEND", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "故障原因一级类别", "fieldKey": "C202447", "physicalColName": "fault_kind_text", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "故障原因二级类别", "fieldKey": "C202448", "physicalColName": "reason_text", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "故障原因三级类别", "fieldKey": "C202449", "physicalColName": "sub_reason_text", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "责任方", "fieldKey": "C202450", "physicalColName": "responsible_party_text", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "故障处理描述", "fieldKey": "C202462", "physicalColName": "work_detail", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "派单时间_秒", "fieldKey": "C202451", "physicalColName": "fault_create_date", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "接单时间_秒", "fieldKey": "C202452", "physicalColName": "create_date", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "综调收到恢复消息时间_秒", "fieldKey": "C202468", "physicalColName": "create_date", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "故障恢复时间_秒", "fieldKey": "C202453", "physicalColName": "recover_date", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "回单时间_秒", "fieldKey": "C202454", "physicalColName": "create_date", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "接单时限_秒", "fieldKey": "C202455", "physicalColName": "sign_ask_date", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "处理时限_秒", "fieldKey": "C202456", "physicalColName": "limit_date", "rowNum": 1, "colNum": 1, "dateType": 2, "dataType": "D", "dateExportFormat": "yyyyMMdd HH:mm:ss", "rowSpan": False, "fieldType": 1},
            {"title": "接单超时", "fieldKey": "C202467", "physicalColName": "CASE \n\tWHEN coalesce(nr.create_date, now()) > no2.sign_ask_date THEN '是'\n\tELSE '否'\nEND", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "恢复超时", "fieldKey": "C202472", "physicalColName": "CASE \n\tWHEN nd.is_new_snwl = '100'\n\tAND coalesce(coalesce(nr2.recover_date, nf.create_date), now()) > io.limit_date THEN '是'\n\tWHEN nd.is_new_snwl = '100'\n\tAND coalesce(coalesce(nr2.recover_date, nf.create_date), now()) <= io.limit_date THEN '否'\n\tWHEN nd.is_new_snwl <> '100'\n\tAND coalesce(nr2.recover_date, now()) > io.limit_date THEN '是'\n\tELSE '否'\nEND", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "接单人单位", "fieldKey": "C202469", "physicalColName": "CASE \n\tWHEN nr.id IS NOT NULL THEN coalesce(dg1.dw_company_name, '电信自维')\n\tELSE ''\nEND", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "接单人部门", "fieldKey": "C202457", "physicalColName": "org_path_name", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "接单人", "fieldKey": "C202458", "physicalColName": "receive_staff", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "回单人单位", "fieldKey": "C202470", "physicalColName": "CASE \n\tWHEN nf.id IS NOT NULL THEN coalesce(dg2.dw_company_name, '电信自维')\n\tELSE ''\nEND", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "回单人部门", "fieldKey": "C202459", "physicalColName": "org_path_name", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "回单人", "fieldKey": "C202460", "physicalColName": "deal_staff", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "影响的宽带业务接入号数量", "fieldKey": "C202463", "physicalColName": "affect_content", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "影响的专线业务接入号数量", "fieldKey": "C202464", "physicalColName": "affect_content", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "影响的IPTV业务接入号数量", "fieldKey": "C202465", "physicalColName": "affect_content", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "影响的语音业务接入号数量", "fieldKey": "C202466", "physicalColName": "affect_content", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "故障时长", "fieldKey": "C202471", "physicalColName": "CASE \n\tWHEN nr2.id IS NOT NULL\n\tAND nr2.recover_date > io.create_date THEN round(CAST(date_part('epoch', nr2.recover_date - io.create_date) AS numeric) / 60)\n\tWHEN nr2.id IS NOT NULL\n\tAND nr2.recover_date < io.create_date THEN round(CAST(date_part('epoch', nr2.create_date - io.create_date) AS numeric) / 60)\n\tWHEN nr2.id IS NULL\n\tAND nf.id IS NOT NULL THEN round(CAST(date_part('epoch', nf.create_date - io.create_date) AS numeric) / 60)\n\tELSE NULL\nEND", "rowNum": 1, "colNum": 1, "dataType": "R", "dateExportFormat": "", "rowSpan": False, "fieldType": 2},
            {"title": "故障回单描述", "fieldKey": "C202474", "physicalColName": "故障回单描述", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "是否上传照片", "fieldKey": "C202476", "physicalColName": "CASE \n\tWHEN aaa IS NULL THEN '否'\n\tELSE '是'\nEND ", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1},
            {"title": "管控范围", "fieldKey": "C208160", "physicalColName": "管控范围", "rowNum": 1, "colNum": 1, "dataType": "S", "dateExportFormat": "", "rowSpan": False, "fieldType": 1}
        ],
        "sumStyle": {},
        "tableStyle": {
            "fontFamily": "Microsoft YaHei",
            "fontSize": 14,
            "color": "#333333",
            "alignment": "1",
            "borderColor": "#e8e8e8",
            "borderStyle": "border1",
            "rowColor": "#FFFFFF",
            "pagingPositon": "right",
            "parityRowShow": False,
            "rowOddColor": "#ffffff",
            "rowEvenColor": "#F5F7FA",
            "columnSort": True,
            "italic": False,
            "bold": False,
            "underline": False,
            "strikeout": False,
            "headerItalic": False,
            "headerBold": False,
            "headerUnderline": False,
            "headerStrikeout": False,
            "bodyItalic": False,
            "bodyBold": False,
            "bodyUnderline": False,
            "bodyStrikeout": False,
            "titleColor": "#333333",
            "titleFontFamily": "Microsoft YaHei",
            "titleFontSize": 14,
            "titlePosition": 1,
            "headerFontFamily": "Microsoft YaHei",
            "headerFontSize": 14,
            "headerFontColor": "#000000",
            "headerColor": "#F5F7FA",
            "wordWrap": False,
            "headerAlignment": "1",
            "expertSheetFlag": 0
        },
        "fieldSettings": [
            {"otherName": "故障时长", "thSeparator": True, "indexFormat": "origin", "fieldKey": "C202471"}
        ],
        "fileFormat": "xlsx",
        "fileName": f"测试导出_20260601_20260630",
        "headName": " ",
        "widthList": [108, 122, 108, 171, 108, 108, 108, 108, 136, 136, 136, 192, 192, 136, 164, 156, 184, 184, 136, 108, 108, 136, 164, 164, 164, 164, 108, 136, 108, 136, 184, 178, 136, 108, 164, 164, 164, 100, 136, 128, 128, 212, 156, 128, 128, 128, 108, 108, 122, 122, 100, 122, 122, 100, 220, 220, 222, 220, 108, 136, 136, 108],
        "qryComponentName": "",
        "language": "zh-CN",
        "envType": ""
    }
    return payload


def main():
    print("=" * 60)
    print("故障工单明细 - 测试爬取程序")
    print("=" * 60)
    print()

    # 1. 加载配置
    config = load_config()
    cookie_str = config["cookie"]
    output_dir = config.get("output_dir", OUTPUT_DIR)

    # 2. 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 3. 构建请求
    url = config["url"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cookie": cookie_str,
        "Origin": "https://zhdd.sd-oss.cn:28880",
        "Referer": "https://zhdd.sd-oss.cn:28880/DtStudio/dap/dapmanager/",
    }

    payload = build_payload()

    # 4. 发送请求（仅一次！）
    print(f"[信息] 目标 URL : {url}")
    print(f"[信息] 请求方式 : POST")
    print(f"[信息] pageSize  : 1（仅测试，绝不增加服务器负担）")
    print(f"[信息] 开始发送请求...")
    print()

    start_time = time.time()

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60,
            verify=False,  # 自签名证书，跳过验证
        )
    except requests.exceptions.SSLError as e:
        print(f"[错误] SSL 证书验证失败: {e}")
        print("提示：该服务器使用自签名证书，脚本已默认跳过验证。")
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"[错误] 连接失败: {e}")
        print("提示：请检查网络是否可达，或确认 VPN 是否已连接。")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("[错误] 请求超时（60秒）")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"[错误] 请求异常: {e}")
        sys.exit(1)

    elapsed = time.time() - start_time
    print(f"[信息] 请求耗时 : {elapsed:.2f} 秒")
    print(f"[信息] 状态码   : {response.status_code}")
    print()

    # 5. 处理响应
    content_type = response.headers.get("Content-Type", "")
    content_disposition = response.headers.get("Content-Disposition", "")

    print(f"[信息] Content-Type       : {content_type}")
    print(f"[信息] Content-Disposition : {content_disposition}")
    print()

    # 判断是否为 Excel 文件
    is_xlsx = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in content_type
        or ".xlsx" in content_disposition
        or response.content[:4] == b"PK\x03\x04"  # ZIP/XLSX magic number
    )

    if response.status_code == 200 and is_xlsx:
        # 提取文件名
        filename = "downloaded.xlsx"
        if "filename=" in content_disposition:
            raw = content_disposition.split("filename=")[-1].strip().strip('"').strip("'")
            if raw:
                # 尝试 URL 解码
                from urllib.parse import unquote
                filename = unquote(raw)

        filepath = os.path.join(output_dir, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)

        file_size_kb = len(response.content) / 1024
        print(f"[成功] 文件已保存至: {os.path.abspath(filepath)}")
        print(f"[成功] 文件大小     : {file_size_kb:.2f} KB")
        print()
        print("测试成功！该接口可以正常下载目标文件。")
    else:
        print("[失败] 未能获取到预期的 xlsx 文件。")
        print()
        print("响应内容预览（前 500 字符）:")
        print("-" * 60)
        try:
            body = response.text[:500]
        except Exception:
            body = str(response.content[:500])
        print(body)
        print("-" * 60)
        print()
        print("可能的原因：")
        print("1. Cookie 已过期，请从浏览器重新复制")
        print("2. 服务器返回了错误信息（如上所示）")
        print("3. 查询条件无数据（2026年数据尚未生成）")

    print()
    print("=" * 60)
    print("程序执行完毕。")


if __name__ == "__main__":
    # 禁用 SSL 警告（自签名证书）
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    main()