# -*- coding: utf-8 -*-
import logging
import math

logger = logging.getLogger(__name__)

# num --------------------
import re

from cian_flats.settings import GROUP_NUMBER


class Flat:
    """
    Parse info to needed values
    """

    def __init__(self, page_info_json, page_html_json):
        # timer_start = time.time()
        # Group --------------------
        self.group = GROUP_NUMBER

        # Metrdist -------------------- расстояние от метро в минутах
        # Walk -------------------- 1-пешком от метро 0 - на транспорте
        subway = page_info_json.get('subway').get('goby')
        if subway:
            [metrdist, subway_type] = subway.split(u' мин. ')
            self.metrdist = int(metrdist)
            if subway_type == u'на машине':
                self.walk = 0
            elif subway_type == u'пешком':
                self.walk = 1

        # todo Tel --------------------1-есть 0 -нет
        # self.tel=1 if page_info_json.get('phones') else 0

        # N --------------------
        self.n = page_info_json.get('id')

        # Totsp --------------------
        # Livesp --------------------
        # Kitsp --------------------
        # Bal --------------------
        # Floors --------------------
        # NFloors --------------------
        # New --------------------
        self.parse_general_info(page_info_json.get('general'))

        # Rooms --------------------
        title = page_info_json.get('title')
        self.rooms = int(title[:1])

        # Price --------------------
        currency = 1
        self.price = page_info_json.get('total_price_rur') / 1000 / currency

        # Dist --------------------
        [longitude, latitude] = page_info_json.get('center')
        self.dist = self.get_distance(latitude, longitude)

        # Floor -------------------- 1- кроме первого и последнего, 0 иначе
        # floor1 --------------------1 - квартира на первом этаже
        # floor2 --------------------1 - квартира на последнем этаже
        self.floor = 1
        if self.nfloors == 1:
            self.floor = 0
            self.floor1 = 1
        else:
            self.floor1 = 0

        if self.floors == self.nfloors and self.nfloors != None:
            self.floor = 0
            self.floor2 = 1
        else:
            self.floor2 = 0

        self.parse_html(page_html_json)
        # print str(time.clock()-timer_start)+' get flat init'

    def parse_general_info(self, general_info):
        totsp = None
        livesp = None
        kitsp = None
        bal = None
        floor_ratio = None
        house_type = None
        for piece_of_info in general_info:
            title = piece_of_info.get('title')
            value = piece_of_info.get('value')
            if title == u'Общая площадь':
                totsp = value
            if title == u'Жилая площадь':
                livesp = value
            if title == u'Площадь кухни':
                kitsp = value
            if title == u'Балкон':
                bal = value
            if title == u'Этаж':
                floor_ratio = value
            if title == u'Тип дома':
                house_type = value

        if totsp: self.totsp = int(totsp.split()[0])
        if livesp: self.livesp = int(livesp.split()[0])
        if kitsp: self.kitsp = int(kitsp.split()[0])
        if bal:  self.bal = 1 if bal.count(u'балк') > 0 else 0
        self.floors, self.nfloors = None, None
        if floor_ratio:
            floors_ratio_list = floor_ratio.split('/')
            try:
                self.nfloors = int(floors_ratio_list[0])
            except:
                logger.error(str(self.n) + ' bad  floors_ratio_list ' + str(floors_ratio_list))
            if len(floors_ratio_list) == 2:
                self.floors = int(floors_ratio_list[1])
        if house_type == u'вторичка':
            self.new = 0
        elif house_type == u'новостройка':
            self.new = 1

    def get_distance(self, latitude, longitude):
        latitude_center_moscow, longitude_center_moscow = 55.7522200, 37.6155600
        distance_on_unit = self.distance_on_unit_sphere(float(latitude), float(longitude), latitude_center_moscow,
                                                        longitude_center_moscow)
        return round(distance_on_unit * 6373)

    def distance_on_unit_sphere(self, lat1, long1, lat2, long2):

        # Convert latitude and longitude to
        # spherical coordinates in radians.
        degrees_to_radians = math.pi / 180.0

        # phi = 90 - latitude
        phi1 = (90.0 - lat1) * degrees_to_radians
        phi2 = (90.0 - lat2) * degrees_to_radians

        # theta = longitude
        theta1 = long1 * degrees_to_radians
        theta2 = long2 * degrees_to_radians

        # Compute spherical distance from spherical coordinates.

        # For two locations in spherical coordinates
        # (1, theta, phi) and (1, theta', phi')
        # cosine( arc length ) =
        # sin phi sin phi' cos(theta-theta') + cos phi cos phi'
        # distance = rho * arc length

        cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
               math.cos(phi1) * math.cos(phi2))
        arc = math.acos(cos)

        # Remember to multiply arc by the radius of the earth
        # in your favorite set of units to get length.
        return arc

    def parse_html(self, html):
        p = re.compile(u"Телефон:</th>\\n\s*<td>(.*?)</td>", re.DOTALL)
        phone_flg = p.findall(html)
        self.tel = None
        if phone_flg:
            phone_flg = phone_flg[0].strip()
            if phone_flg == u"да":
                self.tel = 1
            elif phone_flg == u"нет":
                self.tel = 0

        p = re.compile(u"Площадь кухни:.*?</i>(.*?)&", re.DOTALL)
        kitsp = p.findall(html)
        self.kitsp = None
        if kitsp and kitsp != ['']:
            self.kitsp = float(kitsp[0].replace(",", "."))

        p = re.compile(u"Жилая площадь:.*?</i>(.*?)&", re.DOTALL)
        livesp = p.findall(html)
        self.livesp = None
        if livesp and livesp != ['']:
            self.livesp = float(livesp[0].replace(",", "."))

        p = re.compile(u"Общая площадь:.*?</i>(.*?)&", re.DOTALL)
        totsp = p.findall(html)
        self.totsp = None
        try:
            self.totsp = float(totsp[0].replace(',', '.'))
        except:
            logger.error('Problems totsp' + str(self.n))
            self.totsp = float(totsp[1].replace(',', '.'))

        # Brick -------------------- 1-кирпичный, монолит ж/б, 0-другой
        p = re.compile(u"Тип дома:</th>\\n\s*<td>(.*?)</td>", re.DOTALL)
        house_type = p.findall(html)
        self.brick = None
        if house_type:
            self.brick = 1 if u"монолитный" in house_type[0] or u"кирпичный" in house_type[0] else 0
