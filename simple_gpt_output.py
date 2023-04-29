from tqdm.auto import tqdm
import pandas as pd
import json
import time
import csv
import os
import config

from mLabAPIHub import mLabAPIHub

api_hub = mLabAPIHub(config.api_key)

prompt_template = 'Give me a best possible company associated with the {} domain. Your response should be in terms of JSON format {{"company": "best possible company", "reason": "your reason in 25 words", "ads": "True" if the url provides advertising/tracking services, otherwise "False"}} without explanation.'

df = pd.read_csv('./hostname.csv')
hostname_list = df['0'].values

if not os.path.isfile('./output.csv'):
    with open('./output.csv', "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['hostname', 'company', 'reason', 'ads'])

for i in tqdm(range(len(hostname_list))):
    input_hostname = hostname_list[i]
    print(input_hostname)
    custome_prompt = prompt_template.format(input_hostname)
    result = api_hub.call_api(
        'openai_completion',
        model="text-davinci-003",
        prompt=custome_prompt,
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    data_to_write = json.loads(result['choices'][0]['text'])
    with open('./output.csv', "a", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([input_hostname, data_to_write['company'], data_to_write['reason'], data_to_write['ads']])
    time.sleep(0.3)
