
import requests
import json
import os
import time

from config import IAM_TOKEN, APY_KEY

with open('yagpt/json/main.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
f.close()
data['modelUri'] = "gpt://" + IAM_TOKEN + "/yandexgpt-lite"
with open('yagpt/json/main.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
f.close()


headers = {
    'Authorization': f'Api-Key {APY_KEY}',
}


def epi(text):
    """
    Sends a text to the Yandex Language Model API (LLM), and returns the generated response.
    """
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    with open('yagpt/json/main.json', 'r', encoding='utf-8') as f:
        main = json.load(f)
    f.close()
    with open('yagpt/json/epi.json', 'r', encoding='utf-8') as f:
        epi = json.load(f)
    f.close()
    main['messages'] = epi
    main['messages'][-1]['text'] = text
    data = json.dumps(main, ensure_ascii=False, indent=4)
    # pprint(data)
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code != 200:
        raise RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                resp.status_code, resp.text
            )
        )
    res = resp.json()['result']['alternatives'][-1]['message']['text']
    with open('yagpt/json/ref.json', 'r', encoding='utf-8') as f:
        ref = json.load(f)
    f.close()
    main['messages'] = ref
    main['messages'][-1]['text'] = res + 'NikitaDakt'
    data = json.dumps(main, ensure_ascii=False, indent=4)
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code != 200:
        raise RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                resp.status_code, resp.text
            )
        )
    return resp.json()['result']['alternatives'][-1]['message']['text']


def gpt(text):
    """
    A function that sends a text to the Yandex Language Model API (LLM) and returns the generated response.
    """
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    with open('gpt/body.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    f.close()
    data['messages'][-1]['text'] = text
    with open('gpt/body.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()
    with open('gpt/body.json', 'r', encoding='utf-8') as f:
        data = json.dumps(json.load(f))
    resp = requests.post(url, headers=headers, data=data)

    if resp.status_code != 200:
        raise RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                {resp.status_code}, {resp.text}
            )
        )
    return resp.json()['result']['alternatives'][-1]['message']['text']