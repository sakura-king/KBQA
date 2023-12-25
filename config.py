# -*- coding:utf-8 -*-

semantic_slot = {
    "定义":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.desc",
        "reply_template" : "'{Disease}' 是这样的：\n",
        "ask_template" : "您问的是 '{Disease}' 的定义吗？",
        "intent_strategy" : "",
        "deny_response":"很抱歉没有理解你的意思呢~"
    },
    "病因":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.cause",
        "reply_template" : "'{Disease}' 疾病的原因是：\n",
        "ask_template" : "您问的是疾病 '{Disease}' 的原因吗？",
        "intent_strategy" : "",
        "deny_response":"您说的我有点不明白，您可以换个问法问我哦~"
    },
    "预防":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.prevent",
        "reply_template" : "关于 '{Disease}' 疾病您可以这样预防：\n",
        "ask_template" : "请问您问的是疾病 '{Disease}' 的预防措施吗？",
        "intent_strategy" : "",
        "deny_response":"额~似乎有点不理解你说的是啥呢~"
    },
    "临床表现(病症表现)":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病)-[r:has_symptom]->(q:症状) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template" : "'{Disease}' 疾病的病症表现一般是这样的：\n",
        "ask_template" : "您问的是疾病 '{Disease}' 的症状表现吗？",
        "intent_strategy" : "",
        "deny_response":"人类的语言太难了！！"
    },
    "相关病症":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病)-[r:acompany_with]->(q:疾病) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template" : "'{Disease}' 疾病的具有以下并发疾病：\n",
        "ask_template" : "您问的是疾病 '{Disease}' 的并发疾病吗？",
        "intent_strategy" : "",
        "deny_response":"人类的语言太难了！！~"
    },
    "治疗方法":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : ["MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.cure_way",
                        "MATCH(p:疾病)-[r:recommand_drug]->(q) WHERE p.name='{Disease}' RETURN q.name",
                        "MATCH(p:疾病)-[r:recommand_recipes]->(q) WHERE p.name='{Disease}' RETURN q.name"],
        "reply_template" : "'{Disease}' 疾病的治疗方式、可用的药物、推荐菜肴有：\n",
        "ask_template" : "您问的是疾病 '{Disease}' 的治疗方法吗？",
        "intent_strategy" : "",
        "deny_response":"没有理解您说的意思哦~"
    },
    "所属科室":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病)-[r:cure_department]->(q:科室) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template" : "得了 '{Disease}' 可以挂这个科室哦：\n",
        "ask_template" : "您想问的是疾病 '{Disease}' 要挂什么科室吗？",
        "intent_strategy" : "",
        "deny_response":"您说的我有点不明白，您可以换个问法问我哦~"
    },
    "传染性":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.easy_get",
        "reply_template" : "'{Disease}' 较为容易感染这些人群：\n",
        "ask_template" : "您想问的是疾病 '{Disease}' 会感染哪些人吗？",
        "intent_strategy" : "",
        "deny_response":"没有理解您说的意思哦~"
    },
    "治愈率":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.cured_prob",
        "reply_template" : "得了'{Disease}' 的治愈率为：",
        "ask_template" : "您想问 '{Disease}' 的治愈率吗？",
        "intent_strategy" : "",
        "deny_response":"您说的我有点不明白，您可以换个问法问我哦~"
    },
    "治疗时间":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病) WHERE p.name='{Disease}' RETURN p.cure_lasttime",
        "reply_template" : "疾病 '{Disease}' 的治疗周期为：",
        "ask_template" : "您想问 '{Disease}' 的治疗周期吗？",
        "intent_strategy" : "",
        "deny_response":"很抱歉没有理解你的意思呢~"
    },
    "化验/体检方案":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病)-[r:need_check]->(q:检查) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template" : "得了 '{Disease}' 需要做以下检查：\n",
        "ask_template" : "您是想问 '{Disease}' 要做什么检查吗？",
        "intent_strategy" : "",
        "deny_response":"您说的我有点不明白，您可以换个问法问我哦~"
    },
    "禁忌":{
        "slot_list" : ["Disease"],
        "slot_values":None,
        "cql_template" : "MATCH(p:疾病)-[r:not_eat]->(q:食物) WHERE p.name='{Disease}' RETURN q.name",
        "reply_template" : "得了 '{Disease}' 切记不要吃这些食物哦：\n",
        "ask_template" : "您是想问 '{Disease}' 不可以吃的食物是什么吗？",
        "intent_strategy" : "",
        "deny_response":"额~似乎有点不理解你说的是啥呢~~"
    },
    "unrecognized":{
        "slot_values":None,
        "reply_answer" : "非常抱歉，我不太知道您在说什么，可能您描述的不是很清楚，您可以换个问法问我哦",
    }
}

intent_threshold_config = {
    "accept": 0.8,
    "deny": 0.2
}

default_answer = """很抱歉我还不知道回答你这个问题\n
                    你可以问我一些有关疾病的\n
                    定义、原因、治疗方法、注意事项、挂什么科室\n
                    预防、禁忌等相关问题哦~"""

gossip_corpus = {
    "greet": [
            "hi",
            "你好呀",
            "hi，你好，你可以叫我小智",
            "你好呀，很高兴认识你"
        ],
    "goodbye": [
            "再见，很高兴为您服务",
            "bye",
            "再见，感谢使用我的服务",
            "再见啦，祝你健康"
        ],
    "deny": [
            "很抱歉没帮到您",
            "I am sorry",
            "那您可以试着问我其他问题哟"
        ],
    "isbot":[
            "我是小智，你的智能健康顾问",
            "你可以叫我小智哦~",
            "我是智能医疗诊断机器人，有什么可以帮助你吗",
            "我是医疗诊断机器人小智"
        ],
    "accept":[
            "没关系，还有其它问题要问么",
            "嗯嗯好的",
            "不客气呢！"
        ]
}

# def semantic_parser(text,user):
#     """
#     对文本进行解析
#     intent = {"name":str,"confidence":float}
#     """
#     # 对医疗意图进行二分类
#     # intent_rst得到的数据{'confidence': 0.8997645974159241, 'intent': '治疗方法'}
#     intent_rst = intent_classifier(text)
#
#     slot_rst = slot_recognizer(text)
#     if intent_rst == -1 or slot_rst == -1 or intent_rst.get("name") == "其他":
#         return semantic_slot.get("unrecognized")
#
#     slot_info = semantic_slot.get(intent_rst.get("name"))
#
#     # 填槽
#     slots = slot_info.get("slot_list")
#     slot_values = {}
#     for slot in slots:
#         slot_values[slot] = None
#         for ent_info in slot_rst:
#             for e in ent_info["entities"]:
#                 if slot.lower() == e['type']:
#                     slot_values[slot] = entity_link(e['word'], e['type'])
#
#     last_slot_values = load_user_dialogue_context(user)["slot_values"]
#     for k in slot_values.keys():
#         if slot_values[k] is None:
#             slot_values[k] = last_slot_values.get(k,None)
#
#     slot_info["slot_values"] = slot_values
#
#     # 根据意图强度来确认回复策略
#     conf = intent_rst.get("confidence")
#     if conf >= intent_threshold_config["accept"]:
#         slot_info["intent_strategy"] = "accept"
#     elif conf >= intent_threshold_config["deny"]:
#         slot_info["intent_strategy"] = "clarify"
#     else:
#         slot_info["intent_strategy"] = "deny"
#
#     return slot_info

# clf_model = CLFModel('./nlu/sklearn_Classification')
# def intent_classifier(text):
#     url = 'http://127.0.0.1:60062/service/api/bert_intent_recognize'
#     data = {"text": text}
#     headers = {'Content-Type':'application/json;charset=utf8'}
#     reponse = requests.post(url, data=json.dumps(data), headers=headers)
#     if reponse.status_code == 200:
#         reponse = json.loads(reponse.text)
#         return reponse['data']
#     else:
#         return -1
#
# def slot_recognizer(text):
#     url = 'http://127.0.0.1:60061/service/api/medical_ner'
#     data = {"text_list": [text]}
#     headers = {'Content-Type': 'application/json;charset=utf8'}
#     reponse = requests.post(url, data=json.dumps(data), headers=headers)
#     if reponse.status_code == 200:
#         reponse = json.loads(reponse.text)
#         return reponse['data']
#     else:
#         return -1


# def neo4j_searcher(cql_list):
#     ress = ""
#     if isinstance(cql_list, list):
#         for cql in cql_list:
#             rst = []
#             data = graph.run(cql).data()
#             if not data:
#                 continue
#             for d in data:
#                 d = list(d.values())
#                 if isinstance(d[0], list):
#                     rst.extend(d[0])
#                 else:
#                     rst.extend(d)
#
#             data = "、".join([str(i) for i in rst])
#             ress += data+"\n"
#     else:
#         data = graph.run(cql_list).data()
#         if not data:
#             return ress
#         rst = []
#         for d in data:
#             d = list(d.values())
#             if isinstance(d[0],list):
#                 rst.extend(d[0])
#             else:
#                 rst.extend(d)
#
#         data = "、".join([str(i) for i in rst])
#         ress += data
#
#     return ress


# def get_answer(slot_info):
#     """
#     根据语义槽获取答案回复
#     """
#     cql_template = slot_info.get("cql_template")
#     reply_template = slot_info.get("reply_template")
#     ask_template = slot_info.get("ask_template")
#     slot_values = slot_info.get("slot_values")
#     strategy = slot_info.get("intent_strategy")
#
#     if not slot_values:
#         return slot_info
#
#     if strategy == "accept":
#         cql = []
#         if isinstance(cql_template, list):
#             for cqlt in cql_template:
#                 cql.append(cqlt.format(**slot_values))
#         else:
#             cql = cql_template.format(**slot_values)
#             # print(cql)
#         answer = neo4j_searcher(cql)
#         if not answer:
#             slot_info["replay_answer"] = "唔~我装满知识的大脑此刻很贫瘠accept"
#         else:
#             pattern = reply_template.format(**slot_values)
#             slot_info["replay_answer"] = pattern + answer
#     elif strategy == "clarify":
#         # 澄清用户是否问该问题
#         pattern = ask_template.format(**slot_values)
#         slot_info["replay_answer"] = pattern
#         # 得到肯定意图之后需要给用户回复的答案
#         cql = []
#         if isinstance(cql_template, list):
#             for cqlt in cql_template:
#                 cql.append(cqlt.format(**slot_values))
#         else:
#             cql = cql_template.format(**slot_values)
#         answer = neo4j_searcher(cql)
#         if not answer:
#             slot_info["replay_answer"] = "唔~我装满知识的大脑此刻很贫瘠clarify"
#         else:
#             pattern = reply_template.format(**slot_values)
#             slot_info["choice_answer"] = pattern + answer
#     elif strategy == "deny":
#         slot_info["replay_answer"] = slot_info.get("deny_response")
#
#     return slot_info


# def text_replay(msg):
#     user_intent = classifier(msg)
#     print(user_intent)
#     if user_intent in ["greet", "goodbye", "deny", "isbot"]:
#         reply = gossip_robot(user_intent)
#     elif user_intent == "accept":
#         reply = load_user_dialogue_context()
#         reply = reply.get("choice_answer")
#     else:
#         reply = medical_robot(msg, "sakura")
#         if reply["slot_values"]:
#             dump_user_dialogue_context("sakura", reply)
#         reply = reply.get("replay_answer")
#     print(reply)


# def medical_robot(text, user):
#     """
#     如果确定是诊断意图则使用该方法进行诊断问答
#     """
#     semantic_slot = semantic_parser_my(text)
#     answer = get_answer(semantic_slot)
#     return answer