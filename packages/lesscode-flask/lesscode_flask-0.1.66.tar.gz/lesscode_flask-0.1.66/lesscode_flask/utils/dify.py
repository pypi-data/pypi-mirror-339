import json
import uuid

import requests
from flask import current_app

from lesscode_flask.model.user import flask_login
from lesscode_flask.utils.helpers import app_config


# def dify_messages(dify_server_url: str, api_key, query: str = None, inputs: dict = None, response_mode="streaming",
#                   mode: str = "chat", user_id: str = None, conversation_id: str = ""):
#     """
#     调用dify 的应用api接口
#
#     :param dify_server_url: dify服务地址
#     :param api_key: api key
#     :param query: 用户查询语句
#     :param inputs: 调用参数
#     :param response_mode: 响应类型 streaming:流式
#     :param mode: 应用类型(# 聊天助手:chat 文本生成:completion 聊天流程:advanced-chat 工作流:workflow Agent:agent-chat)
#     :param user_id: 调用人user_id
#     :return:
#     """
#     if user_id is None:
#         user_id = uuid.uuid4().hex
#     data = {
#         "inputs": inputs,
#         "response_mode": response_mode,
#         "user": user_id,
#         "conversation_id": conversation_id
#     }
#     if "chat" in mode:  # 聊天
#         data["query"] = query
#         server_url = dify_server_url + "/v1/chat-messages"
#     elif mode == "completion":  # 文本生成
#         if inputs is None:
#             inputs = {"query": query}
#         data["inputs"] = inputs
#         server_url = dify_server_url + "/v1/completion-messages"
#     elif mode == "workflow":  # 工作流
#         server_url = dify_server_url + "/v1/workflows/run"
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json'
#     }
#     try:
#         response = requests.post(server_url, headers=headers, json=data, stream=True)
#         for line in response.iter_lines(decode_unicode=True):
#             if line and line != "event: ping":  # 过滤掉空行和ping事件
#                 if not line.startswith("data: "):
#                     message_error = {"event": "message_error", "message": line}
#                     yield f'data: {json.dumps(message_error)}\n\n'
#                     break
#                 yield f"{line}\n\n"
#     except Exception as e:
#         print(f"Error: {e}")
#         yield 'data: {"event": "message_end"}'


# def get_app_key(app_id):
#     difyAppKey = DifyAppKeyService().get_item(app_id)
#     if difyAppKey is None:
#         return "应用不存在"
#     API_KEY = difyAppKey.get("dify_api_key")
#     return API_KEY


def dify_chat_messages(api_key, query: str = None, inputs: dict = None, conversation_id: str = "", files=None,
                       response_mode="streaming", user_id: str = None, server_url: str = None):
    """
    发送对话消息
    :param api_key: API 秘钥
    :param query: 用户查询语句
    :param inputs: 调用参数
    :param conversation_id: 会话 ID
    :param files: 文件列表，适用于传入文件结合文本理解并回答问题
    :param server_url:模型服务地址
    :param response_mode: 响应类型 streaming:流式 ，blocking 阻塞式
    :param user_id: 调用人user_id
    :return:
    """
    if server_url is None:
        server_url = app_config.get("DIFY_SERVER_URL")
    if user_id is None:
        user_id = uuid.uuid4().hex
    data = {
        "inputs": inputs,
        "query": query,
        "response_mode": response_mode,
        "conversation_id": conversation_id,
        "user": user_id,
        "files": files
        # "files": [
        #     {
        #         "type": "image",
        #         "transfer_method": "remote_url",
        #         "url": "https://cloud.dify.ai/logo/logo-site.png"
        #     }
        # ]
    }
    # if files is not None:
    #     data["files"] = files
    # if "chat" in mode:  # 聊天
    #     data["query"] = query
    #     server_url = server_url + "/v1/chat-messages"
    # elif mode == "completion":  # 文本生成
    #     if inputs is None:
    #         inputs = {"query": query}
    #     data["inputs"] = inputs
    #     server_url = server_url + "/v1/completion-messages"
    # elif mode == "workflow":  # 工作流
    #     server_url = server_url + "/v1/workflows/run"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(f"{server_url}/v1/chat-messages", headers=headers, json=data, stream=True)
        if "streaming" == response_mode:
            pass
            for line in response.iter_lines(decode_unicode=True):
                if line and line != "event: ping":  # 过滤掉空行和ping事件
                    if not line.startswith("data: "):
                        message_error = {"event": "message_error", "message": line}
                        yield f'data: {json.dumps(message_error)}\n\n'
                        break
                    yield f"{line}\n\n"
        else:  # blocking
            res = response.text
            yield res
    except Exception as e:
        if "streaming" == response_mode:
            print(f"Error: {e}")
            yield 'data: {"event": "message_end"}'
        else:  # blocking
            return f'{{"event": "message", "answer": "{e}"}}'


def dify_stop_messages(api_key: str, task_id: str, user_id=None, server_url: str = None):
    """
    停止响应 仅支持流式模式。
    :param api_key: API 秘钥
    :param task_id: 任务 ID，可在流式返回 Chunk 中获取
    :param user_id: 调用人user_id
    :param server_url: 模型服务地址
    :return:
    """

    if user_id is None:
        user_id = uuid.uuid4().hex
    data = {
        "user": user_id
    }
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    if server_url is None:
        server_url = app_config.get("DIFY_SERVER_URL")
    try:
        requests.post(f"{server_url}/v1/chat-messages/{task_id}/stop", headers=headers, json=data, stream=False)
    finally:
        # 接口固定返回success
        return {
            "result": "success"
        }


def dify_feedbacks(api_key: str, messages_id: str, rating: int, user_id=None, server_url: str = None):
    """
    用户反馈  点赞
    :param api_key: API 秘钥
    :param messages_id: 消息id
    :param rating: 评价 0：取消 1：like 2：dislike
    :param user_id: 调用人user_id
    :param server_url: 模型服务地址
    :return:
    """
    if user_id is None:
        user_id = uuid.uuid4().hex
    data = {
        "user": user_id
    }
    if server_url is None:
        server_url = app_config.get("DIFY_SERVER_URL")
    if rating == 0:
        data["rating"] = None
    elif rating == 1:
        data["rating"] = "like"
    elif rating == 2:
        data["rating"] = "dislike"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(f"{server_url}/v1/messages/{messages_id}/feedbacks", headers=headers, json=data, stream=False)
    finally:
        # 接口固定返回success
        return {
            "result": "success"
        }


def dify_history_messages(api_key: str, conversation_id: str, limit: int = 20, first_id: str = None, user_id=None,
                          server_url: str = None):
    """
    获取会话历史消息
    :param api_key: API 秘钥
    :param conversation_id: 会话 ID
    :param first_id: 当前页第一条聊天记录的 ID，默认 null
    :param limit: 一次请求返回多少条聊天记录，默认 20 条。
    :param user_id: 调用人user_id
    :param server_url: 模型服务地址
    :return:
    """
    if user_id is None:
        user_id = uuid.uuid4().hex
    data = {
        "user": user_id,
        "conversation_id": conversation_id,
        "limit": limit,
        "first_id": first_id
    }
    if server_url is None:
        server_url = app_config.get("DIFY_SERVER_URL")
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{server_url}/v1/messages", headers=headers, params=data)
    return response.json()


def dify_history_conversations(api_key: str, conversation_id: str, limit: int = 20, last_id: str = None, user_id=None,
                               server_url: str = None):
    """
    获取历史会话列表
    获取当前用户的会话列表，默认返回最近的 20 条。
    :param api_key: API 秘钥
    :param conversation_id: 会话 ID
    :param last_id: （选填）当前页最后面一条记录的 ID，默认 null
    :param limit: 一次请求返回多少条记录，默认 20 条，最大 100 条，最小 1 条。
    :param sort_by: 排序字段，默认 -updated_at(按更新时间倒序排列) 可选值：created_at, -created_at, updated_at, -updated_at 字段前面的符号代表顺序或倒序，-代表倒序
    :param user_id: 调用人user_id
    :param server_url: 模型服务地址
    :return:
    """
    if user_id is None:
        user_id = uuid.uuid4().hex
    data = {
        "user": user_id,
        "conversation_id": conversation_id,
        "limit": limit,
        "last_id": last_id
    }
    if server_url is None:
        server_url = app_config.get("DIFY_SERVER_URL")
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{server_url}/v1/conversations", headers=headers, params=data)
    return response.json()


def dify_delete_conversations(api_key: str, conversation_id: str, user_id=None,
                              server_url: str = None):
    """
    删除会话
    获取当前用户的会话列表，默认返回最近的 20 条。
    :param api_key: API 秘钥
    :param conversation_id: 会话 ID
    :param user_id: 调用人user_id
    :param server_url: 模型服务地址
    :return:
    """
    if user_id is None:
        user_id = uuid.uuid4().hex
    data = {
        "user": user_id,
        "conversation_id": conversation_id
    }
    if server_url is None:
        server_url = app_config.get("DIFY_SERVER_URL")
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.delete(f"{server_url}/v1/conversations", headers=headers, params=data)
    return response.json()


def dify_conversations_rename(api_key: str, conversation_id: str, name: str = None, auto_generate=False, user_id=None,
                              server_url: str = None):
    """
    会话重命名
    :param api_key: API 秘钥
    :param conversation_id: 会话 ID
    :param name: （选填）名称，若 auto_generate 为 true 时，该参数可不传。
    :param auto_generate: （选填）自动生成标题，默认 false。
    :param user_id: 调用人user_id
    :param server_url: 模型服务地址
    :return:
    """
    if user_id is None:
        user_id = uuid.uuid4().hex
    data = {
        "name": name,
        "auto_generate": auto_generate,
        "user": user_id
    }
    if server_url is None:
        server_url = app_config.get("DIFY_SERVER_URL")
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{server_url}/v1/conversations/{conversation_id}/name", headers=headers, params=data)
    return response.json()


def dify_files_upload(api_key: str, file, user_id=None,
                      server_url: str = None):
    """
    会话重命名
    :param api_key: API 秘钥
    :param conversation_id: 会话 ID
    :param name: （选填）名称，若 auto_generate 为 true 时，该参数可不传。
    :param auto_generate: （选填）自动生成标题，默认 false。
    :param user_id: 调用人user_id
    :param server_url: 模型服务地址
    :return:
    """
    if user_id is None:
        user_id = uuid.uuid4().hex
    data = {
        "user": user_id
    }
    files = [
        ('file', (file.filename, file, file.content_type))
    ]
    if server_url is None:
        server_url = app_config.get("DIFY_SERVER_URL")
    headers = {
        'Authorization': f'Bearer {api_key}',
        # 'Content-Type': 'multipart/form-data'
    }
    response = requests.post(f"{server_url}/v1/files/upload", headers=headers, data=data, files=files)
    return response.json()
