import json
import os
def outputjson(data_csv,edition_name,count,config):
    img_index = 0
    zfill_count = len(str(count - 1))
    for index,row in data_csv.iterrows():
        json_text = {"name": str(config['CONFIG_JSON_NAME']) + "#" + str(img_index) , "description": str(config["CONFIG_JSON_DESCRIPTION"]),"image": "","attributes":[]}
        for i in range(0,len(row)):
            json_text['attributes'].append({'trait_type': row.index[i], 'value': row[i]})
        jsondata = json.dumps(json_text, indent=4, separators=(',', ': '))
        f = open(os.path.join('output', 'edition ' + str(edition_name),"json",str(str(img_index).zfill(zfill_count)) + ".json"), 'w')
        f.write(jsondata)
        f.close()
        img_index += 1


