import openai
from Extensions.Privatization.LLM.setting import ChatGPT_API_KEY


def chatgpt(prompt, ai_name, ai_role):
    openai.api_key = ChatGPT_API_KEY

    # Use the ChatCompletion to interact with the chat model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ai_name+' '+ai_role},
            {"role": "user", "content": prompt}
        ]
    )

    # Extracting the message content from the response
    usage = response['usage']

    result = {
        "reply": response['choices'][0]['message']['content'],
        "prompt_tokens": usage['prompt_tokens'],
        "completion_tokens": usage['completion_tokens'],
        "total_tokens": usage['total_tokens']
    }

    return result
