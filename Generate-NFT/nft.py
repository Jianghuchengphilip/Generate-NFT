from PIL import Image
import pandas as pd
import numpy as np
import time
import os
import random
import warnings
from logger import Logger
import sys
import check_asset
warnings.simplefilter(action='ignore', category=FutureWarning)
import copy
import yaml
global all_traits_rarities
global zfill_count
zfill_count = 0
all_traits_rarities = {}
def set_config(filename):
    with open(filename, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def parse_config():
    assets_path = 'assets'
    for layer in CONFIG:
        layer_path = os.path.join(assets_path, layer['directory'])
        traits = sorted([trait for trait in os.listdir(layer_path) if trait[0] != '.'])
        check_asset.state(traits,log)
        if not layer['required']:
            traits = [None] + traits
        if layer['rarity_weights'] == 'None':
            rarities = [1 for x in traits]
        elif layer['rarity_weights'] == 'random':
            rarities = [random.random() for x in traits]
        elif type(layer['rarity_weights']) == list:
            assert len(traits) == len(layer['rarity_weights']), f"确保您拥有当前数量的稀有权重(图片数:{len(traits)},权重数:{len(layer['rarity_weights'])},应将config.yaml其中设置相同)"
            if len(traits) != len(layer['rarity_weights']):
                Logger('./log/error.log', level='error').logger.error(f"确保您拥有当前数量的稀有权重(图片数:{len(traits)},权重数:{len(layer['rarity_weights'])},应将config.yaml其中设置相同)")
                sys.exit()
            rarities = layer['rarity_weights']
        else:
            Logger('./log/error.log', level='error').logger.error("无效稀有权重")
            #raise ValueError("无效稀有权重")
            sys.exit()
        rarities = get_weighted_rarities(rarities)
        layer['rarity_weights'] = rarities
        layer['cum_rarity_weights'] = np.cumsum(rarities)
        layer['traits'] = traits
        layer_rarities = []
        for x,y in zip(layer['traits'],layer['rarity_weights']):
            layer_rarities.append([x,y])
        all_traits_rarities[layer['directory']] = layer_rarities

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
        rand_num = random.random()
        idx = select_index(cum_rarities, rand_num)
        trait_set.append(traits[idx])
        if traits[idx] is not None:
            trait_path = os.path.join(layer['directory'], traits[idx])
            trait_paths.append(trait_path)
    return trait_set, trait_paths


def generate_images(edition, count, drop_dup=False):
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
    log.logger.info("生成第 %i 张图片, %i张不同" % (count, rarity_table.shape[0]))
    if drop_dup:
        img_tb_removed = sorted(list(set(range(count)) - set(rarity_table.index)))
        log.logger.info("移除 %i 张图片..." % (len(img_tb_removed)))
        for i in img_tb_removed:
            os.remove(os.path.join(op_path, str(i).zfill(zfill_count) + '.png'))
        for idx, img in enumerate(sorted(os.listdir(op_path))):
            os.rename(os.path.join(op_path, img), os.path.join(op_path, str(idx).zfill(zfill_count) + '.png'))
    rarity_table = rarity_table.reset_index()
    rarity_table = rarity_table.drop('index', axis=1)
    return rarity_table

def main():
    global log
    folder_path = "./log"
    if not os.path.exists(folder_path):  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(folder_path)
    log = Logger('./log/all.log', level='info')
    log.logger.info('检查配置...')
    filename = './config.yaml'
    global CONFIG
    config = set_config(filename)
    CONFIG = config["CONFIG"]
    log.logger.info(filename)
    log.logger.info(config)
    log.logger.info('检查素材...')
    parse_config()
    tot_comb = get_total_combinations()
    log.logger.info("您可以创建总共%i个不同的NFT" % (tot_comb))
    log.logger.info("您希望创建多少个NFT？输入一个大于0的数字:")
    while True:
        num_avatars = int(input())
        if num_avatars > 0:
            break
    log.logger.info(f"创建{num_avatars}个NFT")
    log.logger.info("您想把该NFT项目命名为:")
    edition_name = input()
    log.logger.info(f"存储NFT文件夹名:{edition_name}")
    log.logger.info("开始生成...")
    rt = generate_images(edition_name, num_avatars,config["drop_dup"])
    log.logger.info("保存元数据...")
    rt.to_csv(os.path.join('output', 'edition ' + str(edition_name), 'metadata.csv'))
    log.logger.info("生成成功!")
    log.logger.info("--------------------------------------------------------------------------------------------")
main()
