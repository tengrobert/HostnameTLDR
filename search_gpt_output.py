import csv
import json
import os
import time
from duckduckgo_search import ddg
from langchain import PromptTemplate
import pandas as pd
from tqdm.auto import tqdm
import config

from mLabAPIHub import mLabAPIHub
api_hub = mLabAPIHub(config.api_key)

df = pd.read_csv('./top_20_merged.csv')
hostname_list = df['hostname'][250:].values

company_template = """Search results: {search_results}
Response in JSON format {{"company": String //Best possible company associated with *.{hostname}}} without any explanation
"""
company_prompt = PromptTemplate(
    input_variables=["search_results", "hostname"],
    template=company_template,
)
company_keywords_template = 'whois {} organization'

ads_template = """Search results: {search_results}
Response in JSON format:{{"company": String, //Best possible company associated with *.{hostname} "ads": "True" or "False", //Is *.{hostname} associated with any ads service? True or False}} without any explanation
"""
ads_prompt = PromptTemplate(
    input_variables=["search_results", "hostname"],
    template=ads_template,
)
ads_keywords_template = '{} ads service'

filename = './search_output.csv'
if not os.path.isfile(filename):
    with open(filename, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['hostname', 'company', 'ads'])

for i in tqdm(range(len(hostname_list))):
    hostname = hostname_list[i]
    print(hostname)
    keywords = ads_keywords_template.format(hostname)
    # keywords = company_keywords_template.format(i)
    search_results = ddg(keywords, region='us-en', safesearch='Off', max_results=10)
    mod_search_results = [s['body'] for s in search_results]
    # prompt = company_prompt.format(search_results=mod_search_results, hostname=i)
    prompt = ads_prompt.format(search_results=mod_search_results, hostname=hostname)

    openai_result = api_hub.call_api(
        'openai_completion',
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    # print(openai_result['choices'][0]['text'])
    data_to_write = json.loads(openai_result['choices'][0]['text'])
    # print(data_to_write)
    with open(filename, "a", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([hostname, data_to_write['company'], data_to_write['ads']])
    time.sleep(0.5)