import random
import dashscope
from Extension.LLM.setting import Qwen_API_KEY

dashscope.api_key = Qwen_API_KEY


def qwen(prompt, ai_name, ai_role):
    messages = [
        {'role': 'system', 'content': ai_name+' '+ai_role},
        {'role': 'user', 'content': prompt}
    ]
    response = dashscope.Generation.call(
        "qwen-turbo",
        messages=messages,
        # set the random seed, optional, default to 1234 if not set
        seed=random.randint(1, 10000),
        # set the result to be "message" format.
        result_format='message',
    )

    usage = response.usage

    data = response.output.choices
    result = {
        "reply": data[0].message.content,
        "prompt_tokens": usage.input_tokens,
        "completion_tokens": usage.output_tokens,
        "total_tokens": usage.total_tokens
    }

    return result
