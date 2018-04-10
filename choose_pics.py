# 在一个大的文件夹里，选择所有的小文件夹，解析每个小文件夹中的文件名，每个年份、时间只保留一张图片，存储到ROOT_PATH中


from utils import parse_img_path
import os, shutil
from config import ROOT_PATH


def main(origin_root_path):
    for dir in os.listdir(origin_root_path):  # 原根目录
        origin_path = os.path.join(origin_root_path, dir)  # 文件夹名
        new_path = os.path.join(ROOT_PATH, dir)  # 要复制到的文件夹名
        if os.path.isdir(origin_path):
            s = set()
            for pic_name in os.listdir(origin_path):  # 对文件夹中的每张图片进行操作
                # pic_name : 20161012_185235_332.png
                try:
                    img_name, year, hour = parse_img_path(pic_name)
                except:
                    print('文件名解析失败-----', pic_name)
                    continue
                key = year + '_' + hour
                if key in s:
                    continue
                else:
                    print('key',key)
                    move_to_root_path(origin_path, new_path, pic_name)
                    s.add(key)


def move_to_root_path(origin_path, new_path, pic_name):
    # 查询是否有重复文件夹，查询如果有则不进行复制，
    if os.path.isdir(new_path):
        pass
    else:
        # 如果没，先创建这个文件夹，然后再把图片复制到这个文件夹中去
        os.mkdir(new_path)
    shutil.copyfile(os.path.join(origin_path,pic_name),os.path.join(new_path,pic_name))


main(r'F:\Data\vehicle\select_period_time_image')
