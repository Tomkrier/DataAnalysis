from zhipuai import ZhipuAI
import json


def init_ai():
    api_key = "b9999f11a7109a49cf65b1ad94a61fb0.CSP2pwupHDsldGSl"
    return ZhipuAI(api_key=api_key)  # 请填写您自己的APIKey


def chatTools(client, prompt, tools, temperature=0.6):
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": prompt
            },
        ],
        tools=tools,
        tool_choice="auto",
        temperature=temperature
    )
    return response.choices[0]


def chat_glmOnce(client, prompt):
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        tool_choice="auto",
    )
    return response.choices[0]


def ask_glm(client, tools, temperature, content, function_list, dataset):
    ack = chatTools(client, content, tools, temperature)

    # 调用解析和函数执行过程
    if ack.finish_reason == "tool_calls":
        tool_call = ack.message.tool_calls[0]
        function_name = tool_call.function.name
        function_args_str = tool_call.function.arguments  # Assuming it's a JSON-encoded string
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
    return ack.message
