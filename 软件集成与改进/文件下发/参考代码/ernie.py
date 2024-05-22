import requests
import json

postion_skill_dict = {
                "name": "cacu_postion_skill_wordcount",
                "description": "根据用户提示的岗位名称或者工作内容，找出学习或者技能要求。用户仅仅给出要从事的工作或者方向也匹配这个函数",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "postionName": {
                            "type": "string",
                            "description": "岗位名称，如果java工程师（输入时将工程师、开发、高级等信息去掉，只留下java关键词）",
                        },
                    },
                    "required": ["postionName"],
                },
            }

skill_postion_dict={
                "name": "cacu_skill_position_wordcount",
                "description": "根据用户给出的技能，查找匹配的岗位",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill": {
                            "type": "string",
                            "description": "技术名，如java,C,C++,linux等",
                        },
                    }
                },
                "required": ["skill"],
            }
            
def main():
    # 调用input（）,让用户控制台输入字符串
    API_KEY = input("请输入API_KEY：")
    SECRET_KEY = input("请输入SECRET_KEY：")
    token = get_access_token(API_KEY, SECRET_KEY)

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-4k-0205?access_token=" + token

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "Java开发所需要的技能是什么？"
            },
        ],
        #message中的content总长度、functions和system字段总内容不能超过8000 个字符，且不能超过2048 tokens
        # examples: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Llsr67q8h#%E7%AC%AC%E4%B8%80%E6%AC%A1%E8%AF%B7%E6%B1%82
        "functions":[skill_postion_dict,
                    postion_skill_dict], # List(function)
        "temperature": 0.6,
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
        print(f"触发了函数调用: {function_name}")
        print(f"参数: {arguments}")


    print(response.text)



def get_access_token(API_KEY, SECRET_KEY):
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    main()
