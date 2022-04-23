def state(traits,log):
    for trait in traits:
        if str.lower(trait[-3:]) != 'png':
            log.logger.warning(f"{trait}不为png格式可能发生合成错误!(请保持asset里文件夹都为png格式)")
