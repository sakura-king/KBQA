# -*- coding:utf-8 -*-
import os
import re
import json
import requests
import random
from py2neo import Graph

from knowledge_extraction.bilstm_crf.app import MedicalNerModel
from nlu.bert_intent_recognition.app import BertIntentModel
from nlu.sklearn_Classification.clf_model import CLFModel
from utils.json_utils import dump_user_dialogue_context, load_user_dialogue_context
from config import *

graph = Graph(host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="20010520")

clf_model = CLFModel('./nlu/sklearn_Classification/model_file')
BIM = BertIntentModel("./nlu/bert_intent_recognition")
NER = MedicalNerModel('./knowledge_extraction/bilstm_crf')

def entity_link(mention,etype):
    """
    对于识别到的实体mention,如果其不是知识库中的标准称谓
    则对其进行实体链指，将其指向一个唯一实体（待实现）
    """
    return mention

def classifier(text):
    """
    判断是否是闲聊意图，以及是什么类型闲聊
    """
    return clf_model.predict(text)


# 自己写的不用部署的方案

def semantic_parser_my(text):
    """
        对文本进行解析
        intent = {"name":str,"confidence":float}
    """
    # 对医疗意图进行二分类
    # intent_receive得到的数据{'intent': '临床表现(病症表现)', 'confidence': 0.9673966765403748}
    intent_receive = BIM.predict(text)
    print("intent_receive: ", intent_receive)

    # 实体识别
    # slot_receive得到的数据如下(是列表的形式):
    # [{'string': '淋球菌性尿道炎的症状', 'entities': [{'word': '球菌性尿道炎', 'type': 'disease'}]},
    # {'string': '上消化道出血的常见病与鉴别', 'entities': [{'word': '上消化道出血', 'type': 'disease'}]}]
    text_l = text.split(" ", 1)
    slot_receive = NER.predict(text_l)
    # slot_receive = [{'string': '淋球菌性尿道炎有什么症状', 'entities': [{'word': '球菌性尿道炎', 'type': 'disease'}]}]
    print("slot_receive: ", slot_receive)

    # if intent_receive == -1 or slot_receive == -1 or intent_receive.get("name") == "其他":
    if intent_receive.get("intent") == "其他":
        return semantic_slot.get("unrecognized")

    slot_info = semantic_slot.get(intent_receive.get("intent")) # 判断是哪个槽位，如“病因”，详情见config.py

    if slot_info == None:
        return slot_info

    # 填槽
    slots = slot_info.get("slot_list") # "slot_list" : ["Disease"]
    slot_values = {}
    for slot in slots:
        slot_values[slot] = None
        for ent_info in slot_receive:
            for e in ent_info["entities"]:
                if slot.lower() == e['type']:
                    # slot_values[slot] = entity_link(e['word'], e['type'])
                    slot_values[slot] = e['word']
    print("slot_values: ", slot_values)
    # 下面这还不知道是干啥,先注释掉看看会不会出错(下面代码是开启多轮对话用的，但是如果一开始json文件里没有任何东西就会报错)
    with open("./utils/logs/sakura.json", 'r', encoding="utf-8")as f:
        data = json.load(f)
        if data:
            last_slot_values = load_user_dialogue_context()["slot_values"]
            for k in slot_values.keys():
                if slot_values[k] is None:
                    slot_values[k] = last_slot_values.get(k, None)

    slot_info["slot_values"] = slot_values

    # 根据意图强度来确认回复策略
    conf = intent_receive.get("confidence")
    if conf >= intent_threshold_config["accept"]:
        slot_info["intent_strategy"] = "accept"
    elif conf >= intent_threshold_config["deny"]:
        slot_info["intent_strategy"] = "clarify"
    else:
        slot_info["intent_strategy"] = "deny"

    return slot_info

def neo4j_searcher(cql_list):
    """
    知识图谱查询
    :param cql_list:
    :return:
    """
    ress = ""
    if isinstance(cql_list, list):
        for cql in cql_list:
            rst = []
            data = graph.run(cql).data()
            if not data:
                continue
            for item in data:
                item_values = list(item.values())
                if isinstance(item_values[0], list):
                    rst.extend(item_values[0])
                else:
                    rst.extend(item_values)
            data = "、".join([str(i) for i in rst])
            ress += data + "\n"
    else:
        data = graph.run(cql_list).data()
        # 这里要分情况：1、查到了，且不为空；2、查到了，但是结果是None([{'p.desc': None}] )；3、直接连不上数据库
        # 三种情况都要有对应的兜底处理
        if not data:
            return ress
        rst = []
        for item in data:
            item_values = list(item.values())
            if isinstance(item_values[0], list):
                rst.extend(item_values[0])
            else:
                rst.extend(item_values)
        data = "、".join([str(i) for i in rst])
        ress += data

    return ress


def get_answer_my(slot_info, text):

    if slot_info == None:
        return slot_info

    cql_template = slot_info.get("cql_template")
    reply_template = slot_info.get("reply_template")
    ask_template = slot_info.get("ask_template")
    slot_values = slot_info.get("slot_values")
    strategy = slot_info.get("intent_strategy")
    if not slot_values:
        return slot_info

    pattern = []

    if strategy == "accept":
        cql_list = []
        if isinstance(cql_template, list):
            for cql in cql_template:
                cql_list.append(cql.format(**slot_values)) # 通过字典设置参数
        else:
            cql_list = cql_template.format(**slot_values)

        answer = neo4j_searcher(cql_list)
        print("neo4j result for accept:", answer)

        # not answer指的是在数据库中没有查到该实体，而answer==None指的是有该实体但是有某些信息不清楚比如治愈率什么的
        if not answer:
            slot_info["reply_answer"] = "抱歉我不太知道您说的这种病，您可以问我其它的病哦"
        elif answer == "None":
            slot_info["reply_answer"] = "抱歉我不知道" + slot_values + "的" + BIM.predict(text).get("intent")
        else:
            pattern = reply_template.format(**slot_values)
            slot_info["reply_answer"] = pattern + answer
        print("pattern for accept:",  slot_info["reply_answer"])
    elif strategy == "clarify":
        # 0.2 < 意图置信度 < 0.8时，进行问题澄清
        pattern = ask_template.format(**slot_values)
        print("pattern for clarity:", pattern)

        slot_info["reply_answer"] = pattern
        # 得到肯定意图之后，需要给出用户回复的答案
        cql_list = []
        if isinstance(cql_template, list):
            for cql in cql_template:
                cql_list.append(cql.format(**slot_values))
        else:
            cql_list = cql_template.format(**slot_values)

        answer = neo4j_searcher(cql_list)

        if not answer:
            slot_info["reply_answer"] = "抱歉我不太知道您说的这种病，您可以问我其它的病哦"

        elif answer == "None":
            slot_info["choice_answer"] = "抱歉我不知道" + slot_values + "的" + BIM.predict(text).get("intent")

        else:
            pattern = reply_template.format(**slot_values)
            slot_info["choice_answer"] = pattern + answer

    elif strategy == "deny":
        slot_info["reply_answer"] = slot_info.get("deny_response")

    return slot_info


def gossip_robot(intent):
    return random.choice(
                gossip_corpus.get(intent)
            )


def medical_robot_my(text):
    """
    如果确定是诊断意图则使用该方法进行诊断问答
    """
    semantic_slot = semantic_parser_my(text)
    # if semantic_slot == None:
    #     answer = "非常抱歉，我还不知道如何回答您，我正在努力学习中~"
    #     return answer
    answer = get_answer_my(semantic_slot, text)
    return answer

def dump_user_dialogue_context(data):
    path = "./utils/logs/sakura.json"
    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(data, sort_keys=True, indent=4,
                separators=(', ', ': '), ensure_ascii=False))

def load_user_dialogue_context():
    path = "./utils/logs/sakura.json"
    if not os.path.exists(path):
        return {"choice_answer": "hi，机器人小智很高心为您服务", "slot_values": None}
    else:
        with open(path, 'r', encoding='utf8') as f:
            data = f.read()
            return json.loads(data)


def text_reply_my(msg):
    user_intent = classifier(msg)
    print(user_intent)
    if user_intent in ["greet", "goodbye", "deny", "isbot", "accept"]:
        reply = gossip_robot(user_intent)
    elif user_intent == "accept1":
        reply = load_user_dialogue_context()
        reply = reply.get("choice_answer")
    else:
        reply = medical_robot_my(msg)
        # if reply == "非常抱歉，我还不知道如何回答您，我正在努力学习中~":
        #     return reply
        # elif reply["slot_values"]:
        if reply["slot_values"]:
            dump_user_dialogue_context(reply)
        reply = reply.get("reply_answer")

    return reply


if __name__ == '__main__':
    with open("./utils/logs/sakura.json", 'w', encoding="utf-8")as f:
        json.dump({}, f)
    while 1:
        question =input('风间琉璃: ')
        answer = text_reply_my(question)
        print("小助手: ", answer)
        # print(medical_robot_my("过敏性鼻炎的症状"))

    # text_replay("发烧的原因是啥")