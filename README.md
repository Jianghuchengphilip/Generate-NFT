# Generate NFT

![](https://img.shields.io/github/downloads/Jianghuchengphilip/Generate-NFT/total)
![](https://img.shields.io/github/license/Jianghuchengphilip/Generate-NFT?color=f05032)
![](https://img.shields.io/github/v/release/Jianghuchengphilip/Generate-NFT?color=important)
![](https://img.shields.io/github/release-date/Jianghuchengphilip/Generate-NFT?color=fcc624)

**克隆这个项目**

```https://github.com/Jianghuchengphilip/Generate-NFT.git```

**安装库**

```pip install Pillow pandas progressbar2 PyYaml -i https://pypi.tuna.tsinghua.edu.cn/simple```

**添加素材**

打开assets文件夹，按目录添加素材并修改config.yaml

**运行**

```python nft.py```

**打赏地址**
```0x92B097fAbADdcE7AFBeFe0962B538B23f7D08622```

**附v2.3软件版使用指南：**
```
config.yaml必知:
1、将素材文件都放到asset中，且最好保证都为png格式。
2、检查asset文件夹里面是否存在隐藏文件，若有请删除。[方法:文件管理器->查看->隐藏文件]
3、asset中不能有空文件夹
4、config.yaml右键选记事本方式打开。
5、config.yaml中CONFIG:[]中的每一个{}都对应asset里面相对应的文件夹。
6、output/rarity_weights_data.json可以查看每个元素出现概率。
config参数规范:
1、键:值
示例：
 'id': 1,       # 数字代表图层，越小越下面
 'name': 'background',   # 命名会出现在metadata.csv中
 'directory': 'Background', # asset对应文件目录，一定要一模一样
 'required': True, # 是否必须需要该组件
 'rarity_weights': random, # 稀有度
2、稀有度设定
'rarity_weights'有三种键值
None 每个元素稀有度都相同，若required为True，该组件None的概率也相同
random 每个元素稀有度都相同，若required为True，该组件None的概率也随机
[w1，w2，w3] 第一个元素稀有度w1  / (w1 + w2 + w3)
	       若required为True，确保[]中的数字与对应directory里的图片数目相同
	       若required为False,  确保[]中的数字与对应directory里的图片数目多一个，例如此情况有3个图片权重可以为[1,2,2,3]，其中1代表None的权重，后面3个分别代表图像权重。```





