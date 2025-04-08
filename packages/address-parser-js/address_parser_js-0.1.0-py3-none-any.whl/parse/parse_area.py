# -*- coding: utf-8 -*-
"""
address-parse
MIT License
By www.asseek.com

Python conversion of the original JavaScript logic.
"""

import functools
from src.parse.area import area as AREA  # 从上一级目录导入 area 字典
from src.parse import utils as Utils  # 从当前目录导入 utils 模块

# 定义关键字常量
PROVINCE_KEYS = [
    '特别行政区', '古自治区', '维吾尔自治区', '壮族自治区', '回族自治区', '自治区', '省省直辖', '省', '市'
]

CITY_KEYS = [
    '布依族苗族自治州', '苗族侗族自治州', '藏族羌族自治州', '哈尼族彝族自治州', '壮族苗族自治州', '傣族景颇族自治州', '蒙古族藏族自治州',
    '傣族自治州', '白族自治州', '藏族自治州', '彝族自治州', '回族自治州', '蒙古自治州', '朝鲜族自治州', '地区', '哈萨克自治州', '盟', '市'
]

AREA_KEYS = [
    '满族自治县', '满族蒙古族自治县', '蒙古族自治县', '朝鲜族自治县',
    '回族彝族自治县', '彝族回族苗族自治县', '彝族苗族自治县', '土家族苗族自治县', '布依族苗族自治县', '苗族布依族自治县', '苗族土家族自治县',
    '彝族傣族自治县', '傣族彝族自治县', '仡佬族苗族自治县', '黎族苗族自治县', '苗族侗族自治县', '哈尼族彝族傣族自治县', '哈尼族彝族自治县',
    '彝族哈尼族拉祜族自治县', '傣族拉祜族佤族自治县', '傣族佤族自治县', '拉祜族佤族布朗族傣族自治县', '苗族瑶族傣族自治县', '彝族回族自治县',
    '独龙族怒族自治县', '保安族东乡族撒拉族自治县', '回族土族自治县', '撒拉族自治县', '哈萨克自治县', '塔吉克自治县',
    '回族自治县', '畲族自治县', '土家族自治县', '布依族自治县', '苗族自治县', '瑶族自治县', '侗族自治县', '水族自治县', '傈僳族自治县',
    '仫佬族自治县', '毛南族自治县', '黎族自治县', '羌族自治县', '彝族自治县', '藏族自治县', '纳西族自治县', '裕固族自治县', '哈萨克族自治县',
    '哈尼族自治县', '拉祜族自治县', '佤族自治县',
    '达斡尔族区', '达斡尔族自治旗',
    '左旗', '右旗', '中旗', '后旗', '联合旗', '自治旗', '旗', '自治县',
    '街道办事处',
    '新区', '区', '县', '市'
]

class ParseArea:
    is_init = False
    province_short_list = []
    province_short = {}
    city_short = {}
    area_short = {}

    @staticmethod
    def init():
        """初始化简称词典"""
        if ParseArea.is_init:
            return

        province_list = AREA.get("province_list", {})
        city_list = AREA.get("city_list", {})
        area_list = AREA.get("area_list", {})

        for code, province in province_list.items():
            short_province = province
            for key in PROVINCE_KEYS:
                short_province = short_province.replace(key, '')
            ParseArea.province_short[code] = short_province
            ParseArea.province_short_list.append(short_province)

        for code, city in city_list.items():
            if len(city) > 2:
                short_city = city
                for key in CITY_KEYS:
                    short_city = short_city.replace(key, '')
                ParseArea.city_short[code] = short_city

        for code, area in area_list.items():
            # 特殊处理
            if area == '雨花台区': area = '雨花区'
            if area == '神农架林区': area = '神农架'

            if len(area) > 2 and area != '高新区':
                short_area = area
                for key in AREA_KEYS:
                    # 只有当关键字不在名称开头时才移除，避免 "市辖区" 被错误缩短
                    if short_area.find(key) > 0: # 原JS逻辑是 > 1，但似乎 > 0 更合理？ 暂时保持 > 0
                         short_area = short_area.replace(key, '')
                ParseArea.area_short[code] = short_area

        ParseArea.is_init = True

    def __init__(self):
        """构造函数，确保初始化"""
        if not ParseArea.is_init:
            ParseArea.init()
        self.results = []

    def parse(self, address, parse_all=False):
        """
        开始解析地址
        :param address: str, 待解析的地址字符串
        :param parse_all: bool, 是否执行全部解析，默认识别到city终止
        :returns: list, 解析结果列表，按可信度排序
        """
        self.results = []
        address = address or "" # 确保 address 是字符串

        # 正向解析
        self.results.extend(ParseArea.parse_by_province(address))

        # 检查是否需要进一步解析
        needs_more_parsing = parse_all or not self.results or not self.results[0].get('__parse', False)

        if needs_more_parsing:
            # 逆向城市解析
            city_results = ParseArea.parse_by_city(address)
            # 避免重复添加相同 code 的结果
            existing_codes = {res.get('code') for res in self.results if res.get('code')}
            self.results.extend([res for res in city_results if res.get('code') not in existing_codes])

            # 再次检查是否需要进一步解析
            # 使用排序后的结果判断
            current_best_parse = self.results[0].get('__parse', 0.0) if self.results else 0.0
            needs_more_parsing = parse_all or not current_best_parse

            if needs_more_parsing:
                 # 逆向地区解析
                area_results = ParseArea.parse_by_area(address)
                existing_codes = {res.get('code') for res in self.results if res.get('code')}
                self.results.extend([res for res in area_results if res.get('code') not in existing_codes])


        # 更新 __parse 分数
        if len(self.results) > 1:
            for result in self.results:
                _address = address
                # 确保 __parse 是数值类型，默认为 0
                result['__parse'] = float(result.get('__parse', 0))

                province = result.get('province', '')
                city = result.get('city', '')
                area = result.get('area', '')

                # 只有当初始解析成功时才增加分数 (避免给完全不匹配的结果加分)
                if result['__parse'] > 0:
                    if province and province in _address:
                        _address = _address.replace(province, '', 1) # 只替换第一个匹配项
                        result['__parse'] += 1
                        if city:
                            city_matched_in_remaining = False
                            if city in _address:
                                # 特殊处理 "县"
                                if city != '县' or _address.find(city) != 0:
                                    _address = _address.replace(city, '', 1)
                                    result['__parse'] += 1
                                    city_matched_in_remaining = True

                                if area and area in _address:
                                    result['__parse'] += 1 # 市和区都在剩余地址中
                                elif area and len(area) >= 2 and area[:2] in _address:
                                     result['__parse'] += 0.5 # 区的前缀在剩余地址中

                            elif city in address: # 城市名在原始地址中，但不在去除省份后的地址中
                                result['__parse'] += 0.5
                                # 即使市不在剩余地址，区也可能在
                                if area and area in _address:
                                    result['__parse'] += 1
                                elif area and len(area) >= 2 and area[:2] in _address:
                                     result['__parse'] += 0.5

                            # 如果市匹配了，但区没有在市匹配的逻辑中加分，在这里检查
                            if city_matched_in_remaining:
                                if area and area not in _address and len(area) >= 2 and area[:2] in _address:
                                     result['__parse'] += 0.5 # 区的前缀在剩余地址中 (市匹配后)

                        # 如果只有省没有市，但区县在地址中
                        elif area and area in _address:
                             result['__parse'] += 1
                        elif area and len(area) >= 2 and area[:2] in _address:
                             result['__parse'] += 0.5


        # 可信度排序
        def compare_results(a, b):
            a_parse = a.get('__parse', 0.0)
            b_parse = b.get('__parse', 0.0)
            a_city = bool(a.get('city'))
            b_city = bool(b.get('city'))
            a_type = a.get('__type')
            b_type = b.get('__type')
            a_name_len = len(a.get('name', ''))
            b_name_len = len(b.get('name', ''))

            # 主要按 __parse 分数降序
            if a_parse > b_parse: return -1
            if a_parse < b_parse: return 1

            # 分数相同，按解析类型优先级 (Province > City > Area)
            type_priority = {'parseByProvince': 3, 'parseByCity': 2, 'parseByArea': 1}
            a_priority = type_priority.get(a_type, 0)
            b_priority = type_priority.get(b_type, 0)
            if a_priority > b_priority: return -1
            if a_priority < b_priority: return 1

            # 分数和类型都相同，优先有市的结果
            if a_city and not b_city: return -1
            if not a_city and b_city: return 1

            # 最后按名字长度（JS是长名优先，这里改为短名优先，表示匹配更精确？）
            # 保持 JS 逻辑：长名优先
            if a_name_len > b_name_len: return -1
            if a_name_len < b_name_len: return 1

            return 0

        self.results.sort(key=functools.cmp_to_key(compare_results))

        # 过滤掉 code 为空的无效结果
        self.results = [res for res in self.results if res.get('code')]

        return self.results

    @staticmethod
    def parse_by_province(address_base):
        """1.1 通过省份正向解析"""
        province_list = AREA.get("province_list", {})
        results = []
        address = address_base

        # 按省份名称长度降序排序，优先匹配长名称（如 "内蒙古自治区" 优先于 "内蒙古"）
        sorted_provinces = sorted(province_list.items(), key=lambda item: len(item[1]), reverse=True)

        for code, province in sorted_provinces:
            result = { # 循环内初始化
                'province': '', 'city': '', 'area': '',
                'details': '', 'name': '', 'code': '',
                '__type': 'parseByProvince', '__parse': False
            }
            current_address = address # 使用临时变量处理当前省份的解析

            index = current_address.find(province)
            short_province = ""
            province_len = 0
            is_short = False

            if index == -1:
                short_province = ParseArea.province_short.get(code, "")
                if short_province:
                    index = current_address.find(short_province)
                    if index > -1:
                        province_len = len(short_province)
                        is_short = True
            else:
                province_len = len(province)

            if index > -1:
                # 如果省份不是第一位 在省份之前的字段识别为名称
                if index > 0:
                    result['name'] = current_address[:index].strip()
                    current_address = current_address[index:].strip() # 更新 address

                result['province'] = province
                result['code'] = code
                address_after_province = current_address[province_len:]

                # 如果是简称匹配，尝试移除关键字后缀
                if is_short:
                    for key in PROVINCE_KEYS:
                        if address_after_province.startswith(key):
                            address_after_province = address_after_province[len(key):]
                            break # 通常只匹配一个

                # 尝试解析市和区
                address_after_city = ParseArea.parse_city_by_province(address_after_province, result)
                if not result.get('city'): # 如果没找到市，尝试直接找区
                    address_after_area = ParseArea.parse_area_by_province(address_after_province, result)
                    # 如果通过省份直接找到了区，更新剩余地址
                    if result.get('area'):
                        final_address = address_after_area
                    else:
                        final_address = address_after_city # 保持 parse_city_by_province 的结果
                else:
                     final_address = address_after_city # 更新剩余地址

                if result.get('city') or result.get('area'): # 成功匹配到市或区
                    result['__parse'] = 1.0 # 初始可信度设为 1.0
                    result['details'] = final_address.strip()

                    # 边界问题处理：名称中包含其他省份简称
                    # (这部分逻辑在 Python 中可能需要更健壮的处理，暂时简化)
                    # if index > 4 and result.get('name') and any(sp in result['name'] for sp in ParseArea.province_short_list):
                    #     # 尝试解析 name 部分，如果成功，可能需要合并或选择
                    #     pass # 暂时忽略复杂合并逻辑

                    results.insert(0, result) # 找到一个有效匹配，加入结果列表头部
                    # 找到一个省份匹配后，通常可以停止，因为省份列表已排序
                    # 但为了兼容原JS可能存在的逻辑（虽然不清晰），这里也 break
                    break
                else:
                    # 未找到市/区，缓存当前结果，但不设置 __parse=True
                    results.append({**result, 'details': address_after_province.strip()})
                    # 不重置 address，继续尝试其他省份（因为省份已排序，理论上第一个匹配是最好的）

        # 如果循环结束都没有 break，results 可能包含多个未完全匹配的结果或为空
        return results


    @staticmethod
    def parse_city_by_province(address, result):
        """1.2 在省份确定的情况下提取城市"""
        province_code = result.get('code', '')
        if not province_code or not address: return address

        city_list = Utils.get_target_area_list_by_code('city', province_code)
        _best_match = {
            'city': '', 'code': '', 'index': -1, 'address': address, 'is_short': False, 'len': 0
        }

        # 按市名称长度降序排序，优先匹配长名称
        sorted_cities = sorted(city_list, key=lambda item: len(item['name']), reverse=True)

        for city in sorted_cities:
            index = address.find(city['name'])
            short_city = ""
            city_len = 0
            is_short = False

            if index == -1:
                short_city = ParseArea.city_short.get(city['code'], "")
                if short_city:
                    index = address.find(short_city)
                    if index > -1:
                        city_len = len(short_city)
                        is_short = True
            else:
                city_len = len(city['name'])

            if index > -1:
                current_address_after = address[index + city_len:]
                # 如果是简称匹配，尝试移除关键字
                if is_short:
                    original_len = len(current_address_after)
                    for key in CITY_KEYS:
                        # 排除几个会导致异常的解析: 市北区, 市南区, 市中区, 市辖区
                        if current_address_after.startswith(key) and \
                           key != '市' and \
                           not any(current_address_after.startswith(v) for v in ['市北区', '市南区', '市中区', '市辖区']):
                            current_address_after = current_address_after[len(key):]
                            break
                    # 如果关键字被移除，更新 city_len (这部分逻辑在原JS中不明确，可能不需要更新len)
                    # city_len += (original_len - len(current_address_after))


                # 更新最佳匹配的条件：优先位置靠前，其次非简称，再次匹配长度
                if _best_match['index'] == -1 or \
                   index < _best_match['index'] or \
                   (index == _best_match['index'] and not is_short and _best_match['is_short']) or \
                   (index == _best_match['index'] and is_short == _best_match['is_short'] and city_len > _best_match['len']):
                    _best_match['city'] = city['name']
                    _best_match['code'] = city['code']
                    _best_match['index'] = index
                    _best_match['address'] = current_address_after # 使用移除关键字后的地址
                    _best_match['is_short'] = is_short
                    _best_match['len'] = city_len # 使用匹配到的名称长度

                # 原JS中 index < 3 的逻辑被移除，统一使用最佳匹配逻辑

        # 循环结束后，如果找到了最佳匹配，则使用它
        if _best_match['index'] > -1:
            result['city'] = _best_match['city']
            result['code'] = _best_match['code'] # 更新省份的 code 为市的 code
            # 尝试解析区县
            address_after_area = ParseArea.parse_area_by_city(_best_match['address'], result)
            return address_after_area

        return address # 没有找到城市，返回原地址

    @staticmethod
    def parse_area_by_city(address, result):
        """1.3 & 2.2 在城市确定的情况下提取地区"""
        city_code = result.get('code', '')
        if not city_code or not address: return address

        area_list = Utils.get_target_area_list_by_code('area', city_code)
        _best_match = {
            'area': '', 'code': '', 'index': -1, 'address': address, 'is_short': False, 'len': 0
        }

        # 按区县名称长度降序排序
        sorted_areas = sorted(area_list, key=lambda item: len(item['name']), reverse=True)

        for area in sorted_areas:
            index = -1
            short_area = ""
            area_len = 0
            is_short = False
            match_name = area['name'] # 默认是全名

            # 优先尝试全名匹配
            index = address.find(area['name'])
            if index > -1:
                area_len = len(area['name'])
            else:
                # 全名未匹配，尝试简称
                short_area_base = ParseArea.area_short.get(area['code'], "")
                if short_area_base:
                    # short_index_of 返回匹配到的名称和索引
                    short_match_info = Utils.short_index_of(address, short_area_base, area['name'])
                    if short_match_info['index'] > -1:
                        index = short_match_info['index']
                        match_name = short_match_info['matchName'] # 可能匹配到的是部分或全部全名
                        area_len = len(match_name)
                        is_short = True # 标记为通过简称逻辑找到的

            if index > -1:
                current_address_after = address[index + area_len:]
                # 如果是简称匹配，尝试移除关键字
                if is_short:
                    original_len = len(current_address_after)
                    for key in AREA_KEYS:
                        if current_address_after.startswith(key):
                            current_address_after = current_address_after[len(key):]
                            break
                    # area_len += (original_len - len(current_address_after))

                # 更新最佳匹配逻辑 (同 parse_city_by_province)
                if _best_match['index'] == -1 or \
                   index < _best_match['index'] or \
                   (index == _best_match['index'] and not is_short and _best_match['is_short']) or \
                   (index == _best_match['index'] and is_short == _best_match['is_short'] and area_len > _best_match['len']):
                    _best_match['area'] = area['name'] # 存储标准全名
                    _best_match['code'] = area['code']
                    _best_match['index'] = index
                    _best_match['address'] = current_address_after
                    _best_match['is_short'] = is_short
                    _best_match['len'] = area_len

        # 循环结束后，如果找到了最佳匹配
        if _best_match['index'] > -1:
            result['area'] = _best_match['area']
            result['code'] = _best_match['code'] # 更新市的 code 为区的 code
            return _best_match['address'] # 返回剩余地址

        return address # 没有找到区县，返回原地址

    @staticmethod
    def parse_area_by_province(address, result):
        """1.4 在只确定省份的情况下，尝试通过区县反推城市"""
        province_code = result.get('code', '')
        if not province_code or not address: return address

        # 获取该省下的所有区县
        city_list = Utils.get_target_area_list_by_code('city', province_code)
        area_list = []
        for city in city_list:
            area_list.extend(Utils.get_target_area_list_by_code('area', city['code']))

        _best_match = {
             'area': '', 'code': '', 'index': -1, 'address': address, 'is_short': False, 'len': 0, 'city': None
        }

        # 按区县名称长度降序排序
        sorted_areas = sorted(area_list, key=lambda item: len(item['name']), reverse=True)

        for area in sorted_areas:
            index = -1
            short_area = ""
            area_len = 0
            is_short = False
            match_name = area['name']

            index = address.find(area['name'])
            if index > -1:
                area_len = len(area['name'])
            else:
                short_area_base = ParseArea.area_short.get(area['code'], "")
                if short_area_base:
                    short_match_info = Utils.short_index_of(address, short_area_base, area['name'])
                    if short_match_info['index'] > -1:
                        index = short_match_info['index']
                        match_name = short_match_info['matchName']
                        area_len = len(match_name)
                        is_short = True

            # 限制匹配位置不能太靠后 (index < 6)
            if index > -1 and index < 6:
                current_address_after = address[index + area_len:]
                if is_short:
                    original_len = len(current_address_after)
                    for key in AREA_KEYS:
                        if current_address_after.startswith(key):
                            current_address_after = current_address_after[len(key):]
                            break
                    # area_len += (original_len - len(current_address_after))

                # 找到区县后，反查城市
                city_info_list = Utils.get_target_area_list_by_code('city', area['code'], parent=True)
                # city 在索引 1 (province, city, area) -> 不对，应该是索引 0
                # get_target_parent_area_list_by_code 返回 [province, city, area]
                # get_target_area_list_by_code('city', area_code, parent=True) 返回 [province, city]
                city = city_info_list[1] if len(city_info_list) > 1 else None


                 # 更新最佳匹配逻辑 (优先匹配位置靠前，其次非简称，再次匹配长度)
                if city and (_best_match['index'] == -1 or \
                   index < _best_match['index'] or \
                   (index == _best_match['index'] and not is_short and _best_match['is_short']) or \
                   (index == _best_match['index'] and is_short == _best_match['is_short'] and area_len > _best_match['len'])):
                    _best_match['area'] = area['name']
                    _best_match['code'] = area['code']
                    _best_match['index'] = index
                    _best_match['address'] = current_address_after
                    _best_match['is_short'] = is_short
                    _best_match['len'] = area_len
                    _best_match['city'] = city


        # 循环结束，如果找到最佳匹配
        if _best_match['index'] > -1 and _best_match['city']:
            result['city'] = _best_match['city']['name']
            result['area'] = _best_match['area']
            result['code'] = _best_match['code'] # 更新省的 code 为区的 code
            return _best_match['address'] # 返回剩余地址

        return address # 未找到合适的区县，返回原地址

    @staticmethod
    def parse_by_city(address_base):
        """2.1 通过城市逆向解析"""
        city_list = AREA.get("city_list", {})
        results = []
        address = address_base

        # 优先匹配长名称城市
        sorted_cities = sorted(city_list.items(), key=lambda item: len(item[1]), reverse=True)

        processed_indices = set() # 记录已处理过的地址段起始索引，避免重复解析

        for code, city in sorted_cities:
            if len(city) < 2: continue # 跳过单字市名

            # 查找所有可能的匹配位置
            current_index = -1
            while True:
                try:
                    current_index = address.find(city, current_index + 1)
                except: # 捕获可能的异常
                    break
                if current_index == -1:
                    break

                # 尝试简称匹配 (仅当全名未找到或需要在不同位置查找时)
                # 简化：只在全名查找失败后尝试一次简称查找所有位置
                # 或者，对每个全名匹配位置，都检查是否可能是简称匹配的一部分？太复杂
                # 暂时只处理找到的全名匹配

                if current_index in processed_indices: continue # 跳过已处理段

                result = { # 为每个匹配位置创建独立 result
                    'province': '', 'city': '', 'area': '',
                    'details': '', 'name': '', 'code': '',
                    '__type': 'parseByCity', '__parse': False
                }
                is_short = False # 当前只处理全名匹配
                city_len = len(city)

                # 获取省份信息
                province_info_list = Utils.get_target_area_list_by_code('province', code, parent=True)
                if not province_info_list: continue
                province = province_info_list[0]

                result['province'] = province['name']
                result['city'] = city
                result['code'] = code

                # 处理左侧地址
                left_address = address[:current_index].strip()
                province_name_in_left = ""
                if left_address:
                    if province['name'] in left_address:
                        province_name_in_left = province['name']
                    else:
                        short_p_name = ParseArea.province_short.get(province['code'], "")
                        if short_p_name and short_p_name in left_address:
                            province_name_in_left = short_p_name

                    if province_name_in_left:
                        name_part = left_address.replace(province_name_in_left, '').strip()
                        if name_part: result['name'] = name_part
                    else:
                         result['name'] = left_address

                # 处理右侧地址
                address_after_city = address[current_index + city_len:]
                # 移除关键字 (如果需要，但这里是全名匹配，通常不移除)

                # 解析区县
                address_after_area = ParseArea.parse_area_by_city(address_after_city, result)

                # 判断是否为有效匹配 (左侧匹配到省份 或 右侧匹配到区县)
                if province_name_in_left or result.get('area'):
                    result['__parse'] = 1.0 # 初始可信度
                    result['details'] = address_after_area.strip()
                    results.append(result) # 添加到结果列表
                    # 标记处理过的段 (从匹配开始到剩余地址结束)
                    # 这个逻辑不完善，可能标记过多或过少
                    # 暂时只标记当前匹配的起始点
                    processed_indices.add(current_index)
                else:
                    # 缓存不可靠匹配
                    results.append({**result, 'details': address_after_area.strip()})
                    processed_indices.add(current_index)


            # 尝试简称匹配 (查找所有位置)
            short_city = ParseArea.city_short.get(code, "")
            if short_city:
                current_index = -1
                while True:
                    try:
                        current_index = address.find(short_city, current_index + 1)
                    except:
                        break
                    if current_index == -1:
                        break

                    if current_index in processed_indices: continue

                    result = { # 独立 result
                        'province': '', 'city': '', 'area': '',
                        'details': '', 'name': '', 'code': '',
                        '__type': 'parseByCity', '__parse': False
                    }
                    is_short = True
                    city_len = len(short_city)

                    province_info_list = Utils.get_target_area_list_by_code('province', code, parent=True)
                    if not province_info_list: continue
                    province = province_info_list[0]

                    result['province'] = province['name']
                    result['city'] = city # 存全名
                    result['code'] = code

                    left_address = address[:current_index].strip()
                    province_name_in_left = ""
                    # ... (同上处理 left_address) ...
                    if left_address:
                        if province['name'] in left_address: province_name_in_left = province['name']
                        else:
                            short_p_name = ParseArea.province_short.get(province['code'], "")
                            if short_p_name and short_p_name in left_address: province_name_in_left = short_p_name
                        if province_name_in_left:
                            name_part = left_address.replace(province_name_in_left, '').strip()
                            if name_part: result['name'] = name_part
                        else: result['name'] = left_address

                    address_after_city = address[current_index + city_len:]
                    # 移除关键字
                    original_len = len(address_after_city)
                    for key in CITY_KEYS:
                        if address_after_city.startswith(key) and key != '市' and \
                           not any(address_after_city.startswith(v) for v in ['市北区', '市南区', '市中区', '市辖区']):
                            address_after_city = address_after_city[len(key):]
                            break

                    address_after_area = ParseArea.parse_area_by_city(address_after_city, result)

                    if province_name_in_left or result.get('area'):
                        result['__parse'] = 1.0 # 简称匹配成功也给初始分
                        result['details'] = address_after_area.strip()
                        results.append(result)
                        processed_indices.add(current_index)
                    else:
                        results.append({**result, 'details': address_after_area.strip()})
                        processed_indices.add(current_index)

        # 返回所有找到的可能匹配，让主 parse 函数排序
        return results


    @staticmethod
    def parse_by_area(address_base):
        """3. 通过地区逆向解析"""
        area_list = AREA.get("area_list", {})
        results = []
        address = address_base

        # 优先匹配长名称地区
        sorted_areas = sorted(area_list.items(), key=lambda item: len(item[1]), reverse=True)
        processed_indices = set()

        for code, area in sorted_areas:
            if len(area) < 2: continue

            # 查找所有全名匹配位置
            current_index = -1
            while True:
                try:
                    current_index = address.find(area, current_index + 1)
                except: break
                if current_index == -1: break

                if current_index in processed_indices: continue

                result = { # 独立 result
                    'province': '', 'city': '', 'area': '',
                    'details': '', 'name': '', 'code': '',
                    '__type': 'parseByArea', '__parse': False
                }
                is_short = False
                area_len = len(area)

                parent_info = Utils.get_target_area_list_by_code('province', code, parent=True)
                if len(parent_info) < 2: continue
                province = parent_info[0]
                city = parent_info[1]

                result['province'] = province['name']
                result['city'] = city['name']
                result['area'] = area
                result['code'] = code

                # 处理左侧
                left_address = address[:current_index].strip()
                province_name_in_left = ""
                city_name_in_left = ""
                # ... (同 parse_by_city 中的 left_address 处理逻辑) ...
                if left_address:
                    if province['name'] in left_address: province_name_in_left = province['name']
                    else:
                        short_p_name = ParseArea.province_short.get(province['code'], "")
                        if short_p_name and short_p_name in left_address: province_name_in_left = short_p_name
                    if province_name_in_left: left_address = left_address.replace(province_name_in_left, '').strip()

                    if city['name'] in left_address: city_name_in_left = city['name']
                    else:
                        short_c_name = ParseArea.city_short.get(city['code'], "")
                        if short_c_name and short_c_name in left_address: city_name_in_left = short_c_name
                    if city_name_in_left: left_address = left_address.replace(city_name_in_left, '').strip()

                    if left_address: result['name'] = left_address

                # 处理右侧
                address_after_area = address[current_index + area_len:]
                # 移除关键字 (如果需要)

                # 边界处理 (同原JS)
                boundary_fixed = False
                if province_name_in_left and not city_name_in_left and result.get('name'):
                    _name_results = ParseArea.parse_by_area(result['name'])
                    if _name_results and _name_results[0].get('__parse'):
                        _res = _name_results[0]
                        original_details = address[current_index:].strip()
                        result.update(_res)
                        result['details'] = original_details
                        result['__parse'] = 2.0
                        results.append(result)
                        processed_indices.add(current_index)
                        boundary_fixed = True


                if not boundary_fixed:
                    if province_name_in_left or city_name_in_left:
                        result['__parse'] = 1.0
                        result['details'] = address_after_area.strip()
                        results.append(result)
                        processed_indices.add(current_index)
                    else:
                        results.append({**result, 'details': address_after_area.strip()})
                        processed_indices.add(current_index)

            # 尝试简称匹配
            short_area_base = ParseArea.area_short.get(code, "")
            if short_area_base:
                current_index = -1
                while True:
                    try:
                        # 使用 utils 中的 short_index_of
                        # 注意：short_index_of 需要地址和基础简称，它会尝试匹配更长的全名部分
                        # 这里逻辑需要调整，我们是在找简称本身的位置
                        current_index = address.find(short_area_base, current_index + 1)
                    except: break
                    if current_index == -1: break

                    if current_index in processed_indices: continue

                    # 确认找到的是简称，而不是全名的一部分
                    # (简单检查：匹配位置+简称长度 不等于 全名长度)
                    # if address[current_index : current_index + len(area)] == area:
                    #     continue # 这是全名匹配，上面已处理

                    # 使用 short_index_of 获取实际匹配的名称和长度
                    short_match_info = Utils.short_index_of(address, short_area_base, area)
                    if short_match_info['index'] != current_index:
                        # short_index_of 可能找到了不同的位置或更长的匹配，跳过当前简单的 find 结果
                        # 或者只处理 short_index_of 返回的结果？
                        continue # 简化：只处理简单的 find 结果，假设它就是简称匹配

                    result = { # 独立 result
                        'province': '', 'city': '', 'area': '',
                        'details': '', 'name': '', 'code': '',
                        '__type': 'parseByArea', '__parse': False
                    }
                    is_short = True
                    # area_len = len(short_area_base) # 使用简称长度
                    area_len = len(short_match_info['matchName']) # 使用 short_index_of 匹配的长度


                    parent_info = Utils.get_target_area_list_by_code('province', code, parent=True)
                    if len(parent_info) < 2: continue
                    province = parent_info[0]
                    city = parent_info[1]

                    result['province'] = province['name']
                    result['city'] = city['name']
                    result['area'] = area # 存全名
                    result['code'] = code

                    # 处理左侧
                    left_address = address[:current_index].strip()
                    province_name_in_left = ""
                    city_name_in_left = ""
                    # ... (同上) ...
                    if left_address:
                        if province['name'] in left_address: province_name_in_left = province['name']
                        else:
                            short_p_name = ParseArea.province_short.get(province['code'], "")
                            if short_p_name and short_p_name in left_address: province_name_in_left = short_p_name
                        if province_name_in_left: left_address = left_address.replace(province_name_in_left, '').strip()

                        if city['name'] in left_address: city_name_in_left = city['name']
                        else:
                            short_c_name = ParseArea.city_short.get(city['code'], "")
                            if short_c_name and short_c_name in left_address: city_name_in_left = short_c_name
                        if city_name_in_left: left_address = left_address.replace(city_name_in_left, '').strip()

                        if left_address: result['name'] = left_address


                    # 处理右侧
                    address_after_area = address[current_index + area_len:]
                    # 移除关键字
                    original_len = len(address_after_area)
                    for key in AREA_KEYS:
                        if address_after_area.startswith(key):
                            address_after_area = address_after_area[len(key):]
                            break

                    # 边界处理 (同上)
                    boundary_fixed = False
                    if province_name_in_left and not city_name_in_left and result.get('name'):
                         _name_results = ParseArea.parse_by_area(result['name'])
                         if _name_results and _name_results[0].get('__parse'):
                             _res = _name_results[0]
                             original_details = address[current_index:].strip()
                             result.update(_res)
                             result['details'] = original_details
                             result['__parse'] = 2.0
                             results.append(result)
                             processed_indices.add(current_index)
                             boundary_fixed = True


                    if not boundary_fixed:
                        if province_name_in_left or city_name_in_left:
                            result['__parse'] = 1.0
                            result['details'] = address_after_area.strip()
                            results.append(result)
                            processed_indices.add(current_index)
                        else:
                            results.append({**result, 'details': address_after_area.strip()})
                            processed_indices.add(current_index)

        return results

# Example usage (optional)
if __name__ == '__main__':
    parser = ParseArea()
    test_addresses = [
        "上海市徐汇区漕溪北路100号",
        "新疆维吾尔自治区伊犁哈萨克自治州奎屯市乌鲁木齐西路55号",
        "内蒙古自治区兴安盟科尔沁右翼前旗察尔森镇政府",
        "广东省广州市天河区体育西路101号",
        "北京市朝阳区三里屯街道雅秀大厦",
        "河北省石家庄市桥西区中山西路100号",
        "江苏省南京市雨花台区软件大道", # 特殊处理 '雨花台区' -> '雨花区'
        "湖北省神农架林区松柏镇", # 特殊处理 '神农架林区' -> '神农架'
        "四川省成都市武侯区高新大道", # '高新区' 不应被缩短
        "山东青岛市市北区", # 避免 '市' 关键字移除错误
        "广东省惠来县惠城镇", # 边界测试
        "地址：北京市海淀区中关村南大街27号",
        "收件人：张三 电话：13800138000 地址：福建省厦门市思明区软件园二期望海路10号",
        "湖南长沙岳麓区麓谷街道",
    ]
    for addr in test_addresses:
        print(f"Parsing: {addr}")
        parsed_results = parser.parse(addr)
        print(f"Result: {parsed_results[0] if parsed_results else 'No match'}\n")
