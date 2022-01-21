# 必须配置此文件才能使代码正常运行

#确保将所有输入图像放入"资产"文件夹中。
# 每层（或每一类）图像必须放在自己的文件夹中。

# CONFIG 是一个对象数组，其中每个对象表示一个层
# 这些层必须有序。

# 每层需要指定以下内容
# 1.id：表示特定图层的数字
# 2.名称：图层的名称。不一定必须与包含图层图像的目录名称相同。
# 3.directory：包含特定图层特征的资产中的文件夹
# 4.必需：如果特定图层是必需的（真）或可选的（假）。第一层必须始终设置为 true。
# 5.rarity_weights：表示性状的稀有性分布。它可以采用三种类型的值。
# - 无：这使得图层中定义的所有特征都同样罕见（或常见）
# - "随机"：随机分配稀有度权重。
# - array：一个数字数组，其中每个数字表示一个权重。
# 如果需要为 True，则此数组必须等于层目录中的图像数。第一个数字是第一个图像的权重（按字母顺序），依此类推...
# 如果需要为 False，则此数组必须等于 1 加上层目录中的图像数。第一个数字是此图层根本没有图像的权重。第二个数字是第一个图像的权重，依此类推...

CONFIG = [
    {
        'id': 1,
        'name': 'background',
        'directory': 'Background',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 2,
        'name': 'Clothes',
        'directory': 'Clothes',
        'required': True,
        'rarity_weights': [1,2,3,4,5,6,7,8],
    },
    {
        'id': 3,
        'name': 'Face',
        'directory': 'Face',
        'required': True,
        'rarity_weights': 'random',
    },
    {
        'id': 4,
        'name': 'Eye',
        'directory': 'Eye',
        'required': True,
        'rarity_weights': 'random',
    },
    {
        'id': 5,
        'name': 'Tattoo',
        'directory': 'Tattoo',
        'required': False,
        'rarity_weights': None,
    },
    {
        'id': 6,
        'name': 'JEWELRY1',
        'directory': 'JEWELRY1',
        'required': False,
        'rarity_weights': 'random',
    },
    {
        'id': 7,
        'name': 'JEWELRY2',
        'directory': 'JEWELRY2',
        'required': False,
        'rarity_weights': 'random',
    },
    {
        'id': 8,
        'name': 'JEWELRY3',
        'directory': 'JEWELRY3',
        'required': False,
        'rarity_weights': 'random',
    },
]
