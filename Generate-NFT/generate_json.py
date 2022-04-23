import pandas as pd
import os
import json
from copy import deepcopy
import yaml
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def set_config(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)
configfilename = './config.yaml'
CONFIG_JSON_URL = set_config(configfilename)["CONFIG_JSON_URL"]
CONFIG_JSON_NAME = set_config(configfilename)["CONFIG_JSON_NAME"]
CONFIG_JSON_DESCRIPTION = set_config(configfilename)["CONFIG_JSON_DESCRIPTION"]
BASE_JSON = {
    "name": CONFIG_JSON_NAME,
    "description": CONFIG_JSON_DESCRIPTION,
    "image": CONFIG_JSON_URL,
    "attributes": [],
}
def generate_paths(edition_name):
    edition_path = os.path.join('output', 'edition ' + str(edition_name))
    metadata_path = os.path.join(edition_path, 'metadata.csv')
    json_path = os.path.join(edition_path, 'json')
    return edition_path, metadata_path, json_path


def clean_attributes(attr_name):
    clean_name = attr_name.replace('_', ' ')
    clean_name = list(clean_name)
    for idx, ltr in enumerate(clean_name):
        if (idx == 0) or (idx > 0 and clean_name[idx - 1] == ' '):
            clean_name[idx] = clean_name[idx].upper()
    clean_name = ''.join(clean_name)
    return clean_name
def get_attribute_metadata(metadata_path):
    df = pd.read_csv(metadata_path)
    df = df.drop('Unnamed: 0', axis = 1)
    df.columns = [clean_attributes(col) for col in df.columns]
    zfill_count = len(str(df.shape[0])) - 1
    return df, zfill_count


def main():
    print("输入需生成JSON的项目名: Tips:项目名指output中edition + 项目名:")
    while True:
        edition_name = input()
        edition_path, metadata_path, json_path = generate_paths(edition_name)
        print(edition_path, metadata_path, json_path)
        if os.path.exists(edition_path):
            print("项目存在,生成JSON元数据中......")
            break
        else:
            print("项目不存在,检查output文件夹查看存在哪些项目")
            print("输入需生成JSON的项目名: Tips:项目名指output中edition + 项目名")
            continue
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    df, zfill_count = get_attribute_metadata(metadata_path)

    for idx, row in df.iterrows():
        item_json = deepcopy(BASE_JSON)
        item_json['name'] = item_json['name'] + str(idx)
        print(str(idx).zfill(zfill_count))
        item_json['image'] = item_json['image'] + '/' + str(idx).zfill(zfill_count) + '.png'
        attr_dict = dict(row)
        for attr in attr_dict:
            if attr_dict[attr] != 'none':
                item_json['attributes'].append({'trait_type': attr, 'value': attr_dict[attr]})
        item_json_path = os.path.join(json_path, str(idx) + ".json")
        with open(item_json_path, 'w') as f:
            json.dump(item_json, f)

main()