import requests
import json

def init_kimiai(key):
    return input(key)
def ask_kimiOnce(key, content):
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key
    }
    data = {
        "model": "moonshot-v1-8k",
        "temperature": 0.5,
        "messages": [ {  "role":"user", "content": content} ],
    }

    response = requests.post(url, headers=headers, json=data)
    response = response.json()
    if 'error' in response:
        print(response['error']['message'])
        return None
    return response['choices'][0]['message']['content']

def ask_kimi(key, tools, temperature, content, function_list, dataset):
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key
    }
    data = {
        "model": "moonshot-v1-8k",
        "temperature": temperature,
        "messages":  [ {  "role":"user", "content": content} ],
        "tools": tools
    }
    response = requests.post(url, headers=headers, json=data)
    response = response.json()
    if 'error' in response:
        print(response['error'])
        return None
    ack = response['choices'][0]
    if ack['finish_reason'] == "tool_calls":
        tool_call = ack['message']['tool_calls'][0]['function']
        function_name = tool_call['name']
        function_args_str = tool_call['arguments']
        try:
            function_args_dict = json.loads(function_args_str)  # Convert the string to a dictionary
        except json.JSONDecodeError:
            print("Invalid JSON string encountered for function arguments.")
        else:
            print(f"function_name:{function_name}")
            if function_name not in function_list:
                print("function_name not in function_list")
            else:
                func = function_list[function_name]
                function_args_dict["dataset"] = dataset
                function_args_dict["prompt"] = content
                return func(**function_args_dict)
    return None