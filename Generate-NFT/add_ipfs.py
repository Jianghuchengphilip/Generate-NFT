import json
import os
edition_name = "pandas"
CONFIG_JSON_IMAGE = "ipfs://QmTkubxdkZjxcKFnvnLvFm8PGvbC7TFCnPs8i2yhNvRaDk/"
dir_json = os.path.join('output', 'edition ' + str(edition_name),"json")
for root, dirs, files in os.walk(dir_json):
    for file in files:
        print(file)
        filepath = root+"\\"+file
        print(root+"\\"+file)
        with open(filepath, 'rb') as f:
            data = json.load(f)
            print(type(data))
            data["image"] = CONFIG_JSON_IMAGE + str(file)[:-5]+".png"
            print(data["image"])
            after = data
        with open(filepath, 'w') as f:
            data = json.dump(after, f)