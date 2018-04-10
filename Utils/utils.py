import os, json, re


def parse_pedestrian_json(id, j, data_id, version):
    d = dict()
    try:
        d['id'] = id
        d['image_key'] = j['image_key']
        d['data_id'] = data_id
        d['version'] = version
        try:
            d['year'], d['time'], d['hour'] = parse_year_time_hour(d['image_key'])
        except:
            return None
        try:
            d['rect_num'] = len(j['person'])
        except:
            d['rect_num'] = 0
        d['weather'] = None
        d['road'] = None
        d['daynight'] = None
    except:
        print('parse_pedestrian_json error, json is ', j)
    return d


def parse_year_time_hour(image_key):
    image_name = os.path.splitext(image_key)[0].lower()
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


# 每次返回一个json的文件路径
def get_json_file(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if not os.path.isdir(file_path):
            yield file_path


def parse_id_version(file_path):
    # data_id = os.path.splitext(file_path.split('\\')[-1])[0].split('_')[0]
    file_name = os.path.splitext(os.path.split(file_path)[1])[0]
    data_id = re.search(r'\d*', file_name).group(0)
    # try:
    #     if not file_path.split('\\')[-1].find('_') == -1:
    #         version = int(file_path.split('\\')[-1].split('_')[1].split('.')[0].replace('v', ''))
    #     else:
    #         version = None
    # except:
    #     print('version error,file_path is ', file_path)
    #     raise
    if re.match(r'\d*_v?(\d)', file_name):
        version = re.search(r'\d*_v?(\d*)', file_name).group(1)
    else:
        version = None
    return data_id, version


# return each json in this file as a list
def get_each_json_list(file_path):
    l = list()
    with open(file_path, 'r')as f:
        for line in f.readlines():
            try:
                l.append(json.loads(line))
            except:

                continue
    return l


def get_json(js, key):
    try:
        return js[key]
    except KeyError:
        return None
