# -*- encode = utf-8 -*-
import os
import logging
from check_photo_flask import fill_used_list
import win32com.client
from config import DB_PATH, ROOT_PATH, TABLE_NAME, TEMP_PATH
from check_photo_flask import Weather

used_key_list = list()


# from each folder get all the images ,each time grab one img_path
# return image_path
def get_img_url(folder_path):
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        if not os.path.isdir(img_path):
            yield img_path
        else:
            yield None
    return folder_path


# get each folder's path ( data id )
def get_folder_path_list():
    folder_path_list = list()
    for folder_name in os.listdir(ROOT_PATH):
        folder_path = os.path.join(ROOT_PATH, folder_name)
        if os.path.isdir(folder_path):
            folder_path_list.append(folder_path)
    return folder_path_list


def parse_img_path(image_path):
    image_name = image_path.split('.')[0]
    return parse_img_name(image_name)  # return (image_name,year,hour)


# from image name get year and hour , if year and hour is the same , then fill all
def parse_img_name(image_name):
    try:
        if image_name.find('ADAS') == -1:
            print('not find ADAS')
            year = image_name.split('_')[0]
            hour = image_name.split('_')[1][:2]
        else:
            print('find ADAS', image_name)
            year = image_name.split('_')[1].split('-')[0]
            hour = image_name.split('_')[1].split('-')[1][:2]
        return image_name, year, hour
    except:
        logging.error('get img time error , image_name is', image_name)
        raise


def grab_img_url():
    folder_path_list = get_folder_path_list()
    for folder_path in folder_path_list:
        # check if folder path used
        # if check_folder_used(folder_path):
        #     print('continue')
        #     continue
        g = get_img_url(folder_path)
        while True:
            try:
                # if not check_folder_used(folder_path):
                #     yield next(g)
                img_url = next(g)
                data_id = parse_data_id(img_url)
                year, time, hour = parse_year_time_hour(img_url)
                key = data_id + "_" + year + "_" + str(int(hour))
                if check_key_used(key):
                    continue
                else:
                    used_key_list.append(key)
                    yield img_url
            except StopIteration as e:
                logging.info(e, '-----已结束')
                # 这里要把已完成的数据id记录下来，后面就不用再用了
                save_used_folder(folder_path)
                break


def parse_year_time_hour(image_key):
    file_name = os.path.split(image_key)[1]
    image_name = os.path.splitext(file_name)[0].lower()
    if image_name.find('michigan') != -1:
        return None
    if image_name.find('._') != -1:
        year = image_name.split('_')[1]
        time = image_name.split('_')[2]
        hour = time[:2].replace('.', '')
        return year, time, hour

    if image_name.find('adas') != -1:
        image_key = image_name.split('_')[1].replace('-', '_')
    else:
        image_key = image_name

    time_list = image_key.split('_')
    year = time_list[0]
    time = time_list[1]
    hour = int(time[:2])
    return year, time, hour


def save_used_folder(folder_path):
    data_id = folder_path.split('\\')[-1].split('_')[0]
    with open(TEMP_PATH, 'a') as f:
        f.write(data_id + '\n')


def check_key_used(key):
    global used_key_list
    if used_key_list == []:
        used_key_list = fill_used_list()
        print(used_key_list)
    else:
        pass
    if key in used_key_list:
        return True
    else:
        return False


def check_folder_used(folder_path):
    data_id = folder_path.split('\\')[-1].split('_')[0]
    data_id_set = get_used_data_id()
    print('data_id_set', data_id_set)
    if data_id in data_id_set:
        return True
    else:
        return False


def get_used_data_id():
    data_id_set = set()
    if os.path.isfile(TEMP_PATH):
        # 如果有就读取其中保存的已完成的data_id
        with open(TEMP_PATH, 'r') as f:
            for line in f.readlines():
                line = line[:-1]
                data_id_set.add(line)
    else:
        # 如果没有这个文件，就创建
        with open(TEMP_PATH, 'w')as f:
            f.write('')
    return data_id_set


def save_to_db(image_url, weather, road, daynight):
    # 按照image_url，提取出  数据id、年份、时间，把数据库中这三个属性相同的行全部填充
    data_id = parse_data_id(image_url)
    print('image_url', image_url)
    if image_url.find('ADAS') == -1:
        print('cant find adas')
        year = parse_year(image_url)
        hour = parse_hour(image_url)
    else:
        # ADAS_20180125-170148_542_000000.png
        print('find adas')
        year = image_url.split('\\')[-1].split('_')[1].split('-')[0]
        hour = image_url.split('\\')[-1].split('_')[1].split('-')[1][:2]
        print('find adas , year={0},hour={1}'.format(year, hour))
    where = (data_id, year, hour)
    values = (weather, road, daynight)
    update_access(where, values)


def update_access(where, values):
    # init adodb connection
    conn = win32com.client.Dispatch(r'ADODB.Connection')
    DSN = 'PROVIDER=Microsoft.ACE.OLEDB.12.0;DATA SOURCE={};'.format(DB_PATH)
    conn.Open(DSN)
    update_sql = "UPDATE {0} SET weather='{1}',road='{2}',daynight='{3}' " \
                 "WHERE data_id='{4}' AND year='{5}' AND hour={6};".format(
        TABLE_NAME, values[0], values[1], values[2], where[0], where[1], where[2])
    print(update_sql)
    cmd = win32com.client.Dispatch(r'ADODB.Command')
    cmd.ActiveConnection = conn
    # test_sql = "Delete * FROM Sheet WHERE data_id='726'"
    cmd.CommandText = update_sql
    cmd.Execute()





def parse_data_id(image_path):
    # D:\GitHub\check_photo_flask\static\726_v15_d\20161012_185232_433.png
    return image_path.split('\\')[-2].split('_')[0]


def parse_year(image_path):
    return image_path.split('\\')[-1][:8]


def parse_hour(image_path):
    return int(image_path.split('\\')[-1].split('_')[1][:2])
