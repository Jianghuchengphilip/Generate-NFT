from PIL import Image
import pandas as pd
import numpy as np
import time
import os
import random

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


from config import CONFIG

def parse_config():
    assets_path = 'assets'
    for layer in CONFIG:
        layer_path = os.path.join(assets_path, layer['directory'])
        traits = sorted([trait for trait in os.listdir(layer_path) if trait[0] != '.'])

        # 如果不需要图层，请在特性数组的开头添加一个“None”
        if not layer['required']:
            traits = [None] + traits
        if layer['rarity_weights'] is None:
            rarities = [1 for x in traits]
        elif layer['rarity_weights'] == 'random':
            rarities = [random.random() for x in traits]
        elif type(layer['rarity_weights'] == 'list'):
            assert len(traits) == len(layer['rarity_weights']), "确保您拥有当前数量的稀有权重"
            rarities = layer['rarity_weights']
        else:
            raise ValueError("稀有权重无效")
        rarities = get_weighted_rarities(rarities)
        layer['rarity_weights'] = rarities
        layer['cum_rarity_weights'] = np.cumsum(rarities)
        print( layer['cum_rarity_weights'])
        layer['traits'] = traits

def get_weighted_rarities(arr):
    return np.array(arr)/ sum(arr)


def generate_single_image(filepaths, output_filename=None):
    bg = Image.open(os.path.join('assets', filepaths[0]))
    for filepath in filepaths[1:]:
        img = Image.open(os.path.join('assets', filepath))
        bg.paste(img, (0,0), img)
    if output_filename is not None:
        bg.save(output_filename)
    else:
        if not os.path.exists(os.path.join('output', 'single_images')):
            os.makedirs(os.path.join('output', 'single_images'))
        bg.save(os.path.join('output', 'single_images', str(int(time.time())) + '.png'))

def get_total_combinations():
    
    total = 1
    for layer in CONFIG:
        total = total * len(layer['traits'])
    return total


def select_index(cum_rarities, rand):
    cum_rarities = [0] + list(cum_rarities)
    for i in range(len(cum_rarities) - 1):
        if rand >= cum_rarities[i] and rand <= cum_rarities[i+1]:
            return i

    return None


def generate_trait_set_from_config():
    
    trait_set = []
    trait_paths = []
    
    for layer in CONFIG:
        traits, cum_rarities = layer['traits'], layer['cum_rarity_weights']
        print(layer['id'],traits, layer['rarity_weights'])
        rand_num = random.random()

        idx = select_index(cum_rarities, rand_num)

        trait_set.append(traits[idx])

        if traits[idx] is not None:
            trait_path = os.path.join(layer['directory'], traits[idx])
            trait_paths.append(trait_path)
        
    return trait_set, trait_paths



def generate_images(edition, count, drop_dup=True):

    rarity_table = {}
    for layer in CONFIG:
        rarity_table[layer['name']] = []

    op_path = os.path.join('output', 'edition ' + str(edition), 'images')

    zfill_count = len(str(count - 1))

    if not os.path.exists(op_path):
        os.makedirs(op_path)

    for n in range(count):
        image_name = str(n).zfill(zfill_count) + '.png'
        trait_sets, trait_paths = generate_trait_set_from_config()
        generate_single_image(trait_paths, os.path.join(op_path, image_name))
        for idx, trait in enumerate(trait_sets):
            if trait is not None:
                rarity_table[CONFIG[idx]['name']].append(trait[: -1 * len('.png')])
            else:
                rarity_table[CONFIG[idx]['name']].append('none')
    rarity_table = pd.DataFrame(rarity_table).drop_duplicates()
    print("生成第 %i 张图片, %i张不同" % (count, rarity_table.shape[0]))
    
    if drop_dup:
        img_tb_removed = sorted(list(set(range(count)) - set(rarity_table.index)))
        print("移除 %i 张图片..." % (len(img_tb_removed)))
        for i in img_tb_removed:
            os.remove(os.path.join(op_path, str(i).zfill(zfill_count) + '.png'))
        for idx, img in enumerate(sorted(os.listdir(op_path))):
            os.rename(os.path.join(op_path, img), os.path.join(op_path, str(idx).zfill(zfill_count) + '.png'))
    rarity_table = rarity_table.reset_index()
    rarity_table = rarity_table.drop('index', axis=1)
    return rarity_table

def main():

    print("检查素材...")
    parse_config()
    tot_comb = get_total_combinations()
    print("您可以创建总共%i个不同的NFT" % (tot_comb))
    print("您希望创建多少个NFT？输入一个大于0的数字:")
    while True:
        num_avatars = int(input())
        if num_avatars > 0:
            break
    
    print("您想把这些NFT命名为:")
    edition_name = input()

    print("开始生成...")
    rt = generate_images(edition_name, num_avatars)

    print("保存元数据...")
    rt.to_csv(os.path.join('output', 'edition ' + str(edition_name), 'metadata.csv'))

    print("生成成功!")


# Run the main function
main()