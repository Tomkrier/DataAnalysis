import requests
import json
from getdata import skill_postion_dict, postion_skill_dict
def ask_ernie(token, flist, temperature, content, function_list, dataset):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-4k-0205?access_token=" + token
    #flist = [skill_postion_dict, postion_skill_dict]
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": content
            },
        ],
        #message中的content总长度、functions和system字段总内容不能超过8000 个字符，且不能超过2048 tokens
        "functions":   flist, #function_dict_list, # List(function)
        "temperature": temperature,
        "top_p": 0.8,
        "penalty_score": 1,
        "disable_search": False,
        "enable_citation": False
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # 将JSON字符串解析为Python字典
    response_data = json.loads(response.text)
    # 检查是否触发了函数调用
    if 'function_call' in response_data:
        function_call = response_data['function_call']
        function_name = function_call['name']
        arguments = json.loads(function_call['arguments'])  # 将arguments字符串解析为Python字典
        if function_name not in function_list:
            print("function_name not in function_list")
        else:
            func = function_list[function_name]
            arguments["dataset"] = dataset
            arguments["prompt"] = content
            return func(**arguments)

    return None

def chat_ernieOnce(token,prompt):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-4k-0205?access_token=" + token

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            },
        ],
        "temperature": 0.8,
        "top_p": 0.8,
        "penalty_score": 1,
        "disable_search": False,
        "enable_citation": False
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = json.loads(response.text)
    return response_data['result']

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    API_KEY = input("请输入百度千帆API_KEY：")
    SECRET_KEY = input("请输入百度千帆SECRET_KEY：")
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

