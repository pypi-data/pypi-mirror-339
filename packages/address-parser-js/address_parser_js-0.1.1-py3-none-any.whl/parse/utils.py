# -*- coding: utf-8 -*-

import re
from src.parse.area import area as AREA  # 假设 area.py 在上一级目录


# 通过地区编码返回省市区对象
def get_area_by_code(code):
    """
    通过地区编码返回省市区对象
    :param code: 地区编码 (字符串)
    :returns: {'code': str, 'province': str, 'city': str, 'area': str}
    """
    code = str(code)
    p_code = f"{code[:2]}0000"
    c_code = f"{code[:4]}00"
    return {
        "code": code,
        "province": AREA.get("province_list", {}).get(p_code, ""),
        "city": AREA.get("city_list", {}).get(c_code, ""),
        "area": AREA.get("area_list", {}).get(code, ""),
    }


# 通过code取父省市对象
def get_target_parent_area_list_by_code(target, code):
    """
    通过code取父省市对象
    :param target: 'province'/'city'/'area'
    :param code: 地区编码 (字符串)
    :returns: list [{'code': str, 'name': str}] [province, city, area]
    """
    code = str(code)
    result = []
    area_list = AREA.get("area_list", {})
    city_list = AREA.get("city_list", {})
    province_list = AREA.get("province_list", {})

    result.insert(
        0,
        {
            "code": code,
            "name": area_list.get(code, ""),
        },
    )
    if target in ["city", "province"]:
        c_code = f"{code[:4]}00"
        result.insert(
            0,
            {
                "code": c_code,
                "name": city_list.get(c_code, ""),
            },
        )
    if target == "province":
        p_code = f"{code[:2]}0000"
        result.insert(
            0,
            {
                "code": p_code,
                "name": province_list.get(p_code, ""),
            },
        )
    return result


# 根据省市县类型和对应的`code`获取对应列表
def get_target_area_list_by_code(target, code=None, parent=False):
    """
    根据省市县类型和对应的`code`获取对应列表
    只能逐级获取 province->city->area OK  province->area ERROR
    :param target: String 'province', 'city', 'area'
    :param code: 父级编码 (字符串), province 时可不传
    :param parent: 默认获取子列表 如果要获取的是父对象 传True
    :returns: list [{'code': str, 'name': str}]
    """
    if parent:
        return get_target_parent_area_list_by_code(target, code)

    result = []
    list_map = {
        "province": "province_list",
        "city": "city_list",
        "area": "area_list",
    }
    target_list_key = list_map.get(target)
    if not target_list_key:
        return result

    current_list = AREA.get(target_list_key, {})
    if not current_list:
        return result

    # 如果没有提供 code，则返回目标类型的整个列表
    if code is None:
        if target == "province":
            return [{"code": c, "name": n} for c, n in current_list.items()]
        else:
            # city 和 area 必须有上级 code
            return result

    code = str(code)
    province_code_prefix = code[:2]
    city_code_prefix = code[:4]

    if target == "city":
        # 获取省下面的所有市
        if code.endswith("0000"):
            for c_code, name in current_list.items():
                if (
                    c_code.startswith(province_code_prefix)
                    and c_code.endswith("00")
                    and c_code != code
                ):
                    result.append({"code": c_code, "name": name})
        else:
            # code 不是省级代码，无法获取市列表
            return result
    elif target == "area":
        # 获取市下面的所有区县
        if code.endswith("00") and not code.endswith("0000"):
            for a_code, name in current_list.items():
                if a_code.startswith(city_code_prefix) and a_code != code:
                    result.append({"code": a_code, "name": name})
        else:
            # code 不是市级代码，无法获取区县列表
            return result
    else:  # target == 'province'
        # 省份列表不需要 code 参数来获取子列表，已在 code is None 时处理
        pass

    return result


# 通过省市区非标准字符串转换为标准对象
def get_area_by_address(province, city, area=None):
    """
    通过省市区非标准字符串转换为标准对象
    旧版识别的隐藏省份后缀的对象可通过这个函数转换为新版支持对象
    :param province: 省份名 (字符串)
    :param city: 城市名 (字符串)
    :param area: 区县名 (字符串, 可选)
    :returns: {'code': str, 'province': str, 'city': str, 'area': str}
    """
    province_list = AREA.get("province_list", {})
    city_list = AREA.get("city_list", {})
    area_list = AREA.get("area_list", {})

    result = {
        "code": "",
        "province": "",
        "city": "",
        "area": "",
    }

    for p_code, p_name in province_list.items():
        if p_name.startswith(province):
            result["code"] = p_code
            result["province"] = p_name
            p_code_prefix = p_code[:2]
            for c_code, c_name in city_list.items():
                if c_code.startswith(p_code_prefix) and c_code.endswith("00"):
                    if c_name.startswith(city):
                        result["code"] = c_code
                        result["city"] = c_name
                        if area:
                            c_code_prefix = c_code[:4]
                            for a_code, a_name in area_list.items():
                                if a_code.startswith(c_code_prefix):
                                    if a_name.startswith(area):
                                        result["code"] = a_code
                                        result["area"] = a_name
                                        return result  # 找到最精确的匹配，直接返回
                            # 如果提供了 area 但没找到匹配，也返回当前市级结果
                            return result
                        else:
                            # 没有提供 area，返回市级结果
                            return result
            # 只找到省，返回省级结果
            return result
    # 完全没找到匹配
    return result


# 字符串占位长度 (近似，中文算2，其他算1)
def str_len(s):
    """
    计算字符串的显示长度 (近似值，非 ASCII 算 2)
    :param s: 输入字符串
    :returns: int 显示长度
    """
    length = 0
    for char in s:
        # 使用 ord() 获取字符的 Unicode 编码
        # CJK 统一表意符号等通常大于 \u00ff (255)
        if ord(char) > 255:
            length += 2
        else:
            length += 1
    return length


# 正则表达式
Reg = {
    "mobile": re.compile(r"(?:86-)?(1[3-9]\d{9})"),  # 简化并优化
    "phone": re.compile(r"(?:(\d{3,4})-)?(\d{7,8})"),  # 匹配区号-号码 或 仅号码
    "zipCode": re.compile(r"([0-9]{6})"),
}


# 查找最短名称在地址中的位置，并尝试匹配更长的名称
def short_index_of(address, short_name, name):
    """
    查找 short_name 在 address 中的索引，并尝试扩展匹配到 name 的最长前缀。
    :param address: 地址字符串
    :param short_name: 短名称 (如 "市")
    :param name: 全名称 (如 "北京市")
    :returns: {'index': int, 'matchName': str} 索引和匹配到的名称，未找到则 index 为 -1
    """
    index = -1
    match_name = ""
    try:
        s_index = address.find(short_name)
    except TypeError:  # address 或 short_name 可能不是字符串
        return {"index": -1, "matchName": ""}

    if s_index > -1:
        index = s_index
        match_name = short_name
        # 从 short_name 的长度开始，尝试匹配 name 的更长前缀
        for i in range(len(short_name), len(name) + 1):
            current_prefix = name[:i]
            try:
                current_index = address.find(current_prefix)
            except TypeError:  # address 或 current_prefix 可能不是字符串
                break  # 无法继续匹配

            if current_index > -1:
                # 如果找到了更长的前缀，更新 index 和 match_name
                # 这里需要考虑是否要求匹配必须包含原始 short_name 的位置
                # 原 JS 代码逻辑似乎是只要找到更长匹配就更新，不强制位置连续性
                # 如果要求位置相关，需要 current_index == s_index
                # 暂时按原 JS 逻辑（可能存在的歧义）处理：找到更长匹配就更新
                index = current_index
                match_name = current_prefix
            else:
                # 一旦找不到更长的前缀，就停止尝试
                break
    return {"index": index, "matchName": match_name}


# 可以选择性地导出或直接使用这些函数
__all__ = [
    "get_area_by_code",
    "get_target_parent_area_list_by_code",
    "get_target_area_list_by_code",
    "get_area_by_address",
    "str_len",
    "Reg",
    "short_index_of",
]
