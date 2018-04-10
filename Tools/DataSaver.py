from Utils.save_to_MySql import MySqlSaver
from Model.FlaskDataModel import DataModel, Head, Person, Vehicle, Traffic_sign
from sqlalchemy.exc import IntegrityError
import math, logging
from Utils.utils import *
from config import data_dict, data_path_dict

logging.basicConfig(filename='logging.txt', format='[%(asctime)s]   %(message)s', datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG, filemode='w')

DATA_TYPE = 'train'
TYPE = 'Pedestrian'
mysql = MySqlSaver('hobot_data_test')


def main(root_path):
    g = get_json_file(root_path)
    while True:
        try:
            file_path = next(g)
            data_id, version = parse_id_version(file_path)
            json_list = get_each_json_list(file_path)
            for js in json_list:
                save_body_data(js, data_id, version)
        except StopIteration:
            mysql.commit()
            break


def save_body_data(js, data_id, version):
    image_key = js['image_key']
    key = TYPE + "_" + data_id + '_' + image_key
    video_name = get_json(js, 'video_name')
    video_index = get_json(js, 'video_index')
    width = js['width']
    height = js['height']
    rects = get_json(js, data_dict[TYPE])
    if TYPE == 'DMS':
        year, time, hour = None, None, None
    else:
        year, time, hour = parse_year_time_hour(image_key)

    if rects:
        rect_num = len(rects)
    else:
        rect_num = 0

    body = DataModel(key=key, data_type=DATA_TYPE, type=TYPE, data_id=data_id, version=version,
                     image_key=image_key, video_name=video_name, video_index=video_index,
                     width=width, height=height, year=year, hour=hour, time=time, rect_num=rect_num)
    try:
        mysql.save(body)
        logging.debug('save body success ({})'.format(str(js)))
    except IntegrityError as e:
        logging.debug('save body error ({})'.format(str(js)))
        logging.debug(e.args)
        if str(e.args).find('Duplicate entry') == -1:
            raise
        else:
            return

    # if rects:
    #     if data_dict[TYPE] == 'person':
    #         save_person(rects, key=key)
    #     elif data_dict[TYPE] == 'vehicle':
    #         save_vehicle(rects, key=key)
    #     elif data_dict[TYPE] == 'head':
    #         save_head(rects, key=key)
    #     elif data_dict[TYPE] == 'traffic_sign':
    #         save_traffic_sign(rects, key=key)


def save_person(persons, key):
    for person in persons:
        try:
            height = abs(round(float(person['data'][3]) - float(person['data'][1]), 1))
            width = abs(round(float(person['data'][2]) - float(person['data'][0]), 1))
            area = int(height * width)
            diagonal = round(math.sqrt((height ** 2 + width ** 2)), 1)
            try:
                h_div_w = round(height / width, 1)
            except ZeroDivisionError:
                h_div_w = None
            hard = person['attrs'].get('hard', None)
            occlusion = person['attrs'].get('occlusion', None)
            ignore = person['attrs'].get('ignore', None)
            blur = person['attrs'].get('blur', None)
            type = person['attrs'].get('type', None)
            pose = person['attrs'].get('pose', None)
            pr = Person(key=key, height=height, width=width, area=area, diagonal=diagonal, h_div_w=h_div_w,
                        pose=pose, type=type, ignore=ignore, blur=blur, occlusion=occlusion, hard=hard)
            mysql.save(pr)
            logging.debug('save person success ({})'.format(str(person)))
        except:
            raise


def save_head(heads, key):
    for head in heads:
        try:
            height = abs(round(float(head['data'][3]) - float(head['data'][1]), 1))
            width = abs(round(float(head['data'][2]) - float(head['data'][0]), 1))
            area = int(height * width)
            diagonal = round(math.sqrt((height ** 2 + width ** 2)), 1)
            try:
                h_div_w = round(height / width, 1)
            except ZeroDivisionError:
                h_div_w = None
            hard = head['attrs'].get('hard', None)
            occlusion = head['attrs'].get('occlusion', None)
            ignore = head['attrs'].get('ignore', None)

            gender = head['attrs'].get('gender', None)
            has_glasses = head['attrs'].get('has_glasses', None)
            hair = head['attrs'].get('hair', None)
            age = head['attrs'].get('age', None)
            new_age = head['attrs'].get('new_age', None)
            has_hat = head['attrs'].get('has_hat', None)
            look = head['attrs'].get('look', None)
            left_eye = head['attrs'].get('left_eye', None)
            right_eye = head['attrs'].get('right_eye', None)
            orientation = head['attrs'].get('orientation', None)

            hd = Head(key=key, height=height, width=width, area=area, diagonal=diagonal, h_div_w=h_div_w,
                      gender=gender, has_glasses=has_glasses, hair=hair, age=age, new_age=new_age, has_hat=has_hat,
                      look=look, left_eye=left_eye, right_eye=right_eye, orientation=orientation
                      , ignore=ignore, occlusion=occlusion, hard=hard)
            mysql.save(hd)
            logging.debug('save head success ({})'.format(str(head)))
        except:
            raise


def save_vehicle(vehicles, key):
    for vehicle in vehicles:
        try:
            height = abs(round(float(vehicle['data'][3]) - float(vehicle['data'][1]), 1))
            width = abs(round(float(vehicle['data'][2]) - float(vehicle['data'][0]), 1))
            area = int(height * width)
            diagonal = round(math.sqrt((height ** 2 + width ** 2)), 1)
            try:
                h_div_w = round(height / width, 1)
            except ZeroDivisionError:
                h_div_w = None
            hard_sample = vehicle['attrs'].get('hard_sample', None)
            occlusion = vehicle['attrs'].get('occlusion', None)
            ignore = vehicle['attrs'].get('ignore', None)
            blur = vehicle['attrs'].get('blur', None)
            type = vehicle['attrs'].get('type', None)
            color = vehicle['attrs'].get('color', None)
            part = vehicle['attrs'].get('part', None)
            light = vehicle['attrs'].get('light', None)
            if vehicle['attrs'].get('score', None) != None:
                score = round(float(vehicle['attrs'].get('score', None)), 1)
            else:
                score = None
            vh = Vehicle(key=key, height=height, width=width, area=area, diagonal=diagonal, h_div_w=h_div_w,
                         hard_sample=hard_sample, ignore=ignore, blur=blur, type=type,
                         color=color, part=part, score=score, light=light, occlusion=occlusion, )
            mysql.save(vh)
            logging.debug('save vehicle success ({})'.format(str(vehicle)))
        except:
            raise


def save_traffic_sign(signs, key):
    for sign in signs:
        try:
            height = abs(round(float(sign['data'][3]) - float(sign['data'][1]), 1))
            width = abs(round(float(sign['data'][2]) - float(sign['data'][0]), 1))
            area = int(height * width)
            diagonal = round(math.sqrt((height ** 2 + width ** 2)), 1)
            h_div_w = round(height / width, 1)
            hard = sign['attrs'].get('hard_sample', None)
            occlusion = sign['attrs'].get('occlusion', None)
            ignore = sign['attrs'].get('ignore', None)
            value = sign['attrs'].get('value', None)
            type = sign['attrs'].get('type', None)
            if type:
                if re.match(r'(.*?)\d', type):
                    type = re.search(r'(.*?)\d', type).group(1)
            tr = Traffic_sign(key=key, height=height, width=width, area=area, diagonal=diagonal, h_div_w=h_div_w,
                              hard=hard, ignore=ignore, type=type, occlusion=occlusion, value=value)
            mysql.save(tr)
            logging.debug('save traffic_sign success ({})'.format(str(sign)))
        except:
            raise


if __name__ == '__main__':
    main(data_path_dict[TYPE + '_' + DATA_TYPE])
