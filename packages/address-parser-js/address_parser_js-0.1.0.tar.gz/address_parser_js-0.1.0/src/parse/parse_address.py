import re

# 假设 area.py 在 src 目录下，utils.py 和 parse_area.py 在 src/parse 目录下
# 注意：根据您的项目结构，可能需要调整导入路径
from src.parse import area as AREA
from src.parse.utils import Utils
from src.parse.parse_area import ParseArea


class ParseAddress:
    """
    地址解析类，将 JavaScript 版本的功能移植到 Python。
    """

    # 排除的关键字，用于清洗地址字符串
    ExcludeKeys = [
        "发件人",
        "收货地址",
        "收货人",
        "收件人",
        "收货",
        "手机号码",
        "邮编",
        "电话",
        "所在地区",
        "详细地址",
        "地址",
        "：",
        ":",
        "；",
        ";",
        "，",
        ",",
        "。",
        "、",
    ]

    # 创建 ParseArea 的实例
    # 注意：确保 ParseArea 类在 parse_area.py 中已定义并可实例化
    _parse_area_instance = ParseArea()

    # 从 Utils 类获取正则表达式
    # 注意：确保 Utils 类在 utils.py 中定义了 Reg 属性或类似的结构
    Reg = Utils.Reg

    def __init__(self):
        """
        初始化 ParseAddress 实例。
        """
        self.result = {"mobile": "", "zip_code": "", "phone": ""}
        self.address = ""

    def parse(self, address, parse_all=False):
        """
        开始解析地址字符串。

        Args:
            address (str): 需要解析的地址字符串。
            parse_all (bool): 是否进行完全解析（传递给 ParseArea）。

        Returns:
            list: 解析结果列表，每个元素是一个包含地址信息的字典。
        """
        results = []
        if address:
            # 重置实例变量以处理新地址
            self.result = {"mobile": "", "zip_code": "", "phone": ""}
            self.address = str(address)  # 确保是字符串

            self._replace()
            self._parse_mobile()
            self._parse_phone()
            self._parse_zip_code()
            # 替换多个空格为一个空格
            self.address = re.sub(r" {2,}", " ", self.address).strip()

            # 尝试在地址开头解析姓名 (作为备选)
            # 使用一个临时字典调用 parse_name，避免修改 self.result
            temp_result_for_name = {"details": self.address, "name": ""}
            first_name_data = self.parse_name(temp_result_for_name)
            first_name = first_name_data.get("name", "")

            # 调用 ParseArea 进行省市区解析
            results = self._parse_area_instance.parse(self.address, parse_all)

            for result_item in results:
                # 合并手机、电话、邮编信息
                result_item.update(self.result)
                # 清理姓名和详情字段两端的空格
                result_item["name"] = result_item.get("name", "").strip()
                result_item["details"] = result_item.get("details", "").strip()

                # 解析姓名
                self.parse_name(result_item, first_name=first_name)
                # 清洗地址详情
                self.handler_detail(result_item)

            # 如果 ParseArea 没有返回结果，创建一个默认结果
            if not results:
                default_result = {
                    "province": "",
                    "city": "",
                    "area": "",
                    "details": self.address,  # 剩余未解析部分作为详情
                    "name": "",
                    "code": "",
                    "__type": "",  # 保持与 JS 版本一致
                }
                default_result.update(self.result)
                self.parse_name(default_result)  # 尝试解析姓名
                results.append(default_result)

        return results

    def _replace(self):
        """
        替换地址字符串中的无效字符和格式。
        """
        address_temp = self.address
        # 移除排除的关键字
        for key in self.ExcludeKeys:
            address_temp = address_temp.replace(key, " ")

        # 替换换行符、制表符为空格，合并多个空格
        address_temp = (
            address_temp.replace("\r\n", " ").replace("\n", " ").replace("\t", " ")
        )
        address_temp = re.sub(r" {2,}", " ", address_temp)

        # 规范化电话号码格式 (去除分隔符)
        address_temp = re.sub(r"(\d{3})-(\d{4})-(\d{4})", r"\1\2\3", address_temp)
        address_temp = re.sub(r"(\d{3}) (\d{4}) (\d{4})", r"\1\2\3", address_temp)

        self.address = address_temp.strip()

    def _parse_mobile(self):
        """
        提取手机号码。
        """
        # 注意：确保 self.Reg['mobile'] 是一个编译好的 Python 正则表达式对象
        match = re.search(self.Reg["mobile"], self.address)
        if match:
            self.result["mobile"] = match.group(0)
            # 从地址中移除已提取的手机号，替换为空格以保持分隔
            self.address = self.address.replace(match.group(0), " ", 1)

    def _parse_phone(self):
        """
        提取电话号码。
        """
        # 注意：确保 self.Reg['phone'] 是一个编译好的 Python 正则表达式对象
        match = re.search(self.Reg["phone"], self.address)
        if match:
            self.result["phone"] = match.group(0)
            # 从地址中移除已提取的电话号码
            self.address = self.address.replace(match.group(0), " ", 1)

    def _parse_zip_code(self):
        """
        提取邮政编码。
        """
        # 注意：确保 self.Reg['zipCode'] 是一个编译好的 Python 正则表达式对象
        match = re.search(self.Reg["zipCode"], self.address)
        if match:
            self.result["zip_code"] = match.group(0)
            # 从地址中移除已提取的邮编，这里不替换为空格，因为它通常连着地址
            self.address = self.address.replace(match.group(0), "", 1)

    @staticmethod
    def parse_name(result, max_len=11, first_name=None):
        """
        从地址详情中提取姓名。

        Args:
            result (dict): 当前解析结果字典，包含 'details' 和 'name' 键。
            max_len (int): 候选姓名字符串的最大（估计）长度。
                           注意：Utils.str_len 的 Python 实现需要处理中英文混合长度。
            first_name (str, optional): 初始解析地址时可能识别的姓名，用于优先匹配。

        Returns:
            dict: 更新后的 result 字典。
        """
        # 假设 Utils 中有 str_len 方法的 Python 实现
        str_len_func = getattr(
            Utils, "str_len", len
        )  # 如果没有 Utils.str_len，则使用内置 len

        current_name = result.get("name", "")
        details = result.get("details", "")

        # 如果当前没有姓名，或者姓名过长，则尝试从详情中提取
        # 注意：JS 版本中 Utils.strLen(result.name) > 15 的逻辑
        if not current_name or str_len_func(current_name) > 15:
            # 先移除详情开头可能存在的省市区信息，避免干扰姓名提取
            cleaned_details = ParseAddress.handler_detail({"details": details}).get(
                "details", ""
            )
            parts = cleaned_details.split(" ")
            potential_name = ""
            potential_name_index = -1

            if len(parts) > 0:  # 即使只有一个部分也可能尝试提取
                for i, part in enumerate(parts):
                    part = part.strip()
                    if not part:  # 跳过空字符串
                        continue

                    # 检查是否是有效的候选姓名（长度等）
                    is_shorter = (
                        str_len_func(part) < str_len_func(potential_name)
                        if potential_name
                        else False
                    )
                    is_first_name_match = first_name and part == first_name

                    # 优先选择匹配 first_name 的，其次选择更短的，最后选择第一个遇到的
                    if not potential_name or is_shorter or is_first_name_match:
                        # 检查长度是否在合理范围内 (JS 版本是 maxLen=11)
                        if str_len_func(part) <= max_len:
                            potential_name = part
                            potential_name_index = i
                            if is_first_name_match:  # 如果匹配到 first_name，优先选择
                                break

            # 如果找到了合适的姓名
            if potential_name and potential_name_index != -1:
                result["name"] = potential_name
                # 从原始详情（未清洗省市区）中移除姓名部分，以保留省市区信息
                original_parts = details.split(" ")
                # 需要找到 potential_name 在 original_parts 中的确切位置
                try:
                    original_index = -1
                    temp_index = 0
                    cleaned_part_counter = 0
                    for orig_part in original_parts:
                        if orig_part.strip():  # 只考虑非空部分
                            if cleaned_part_counter == potential_name_index:
                                original_index = temp_index
                                break
                            cleaned_part_counter += 1
                        temp_index += 1

                    if original_index != -1:
                        del original_parts[original_index]
                        result["details"] = " ".join(original_parts).strip()
                    else:  # 如果找不到（理论上不应发生），则回退到使用清洗后的详情
                        if potential_name_index < len(parts):  # 确保索引有效
                            del parts[potential_name_index]
                            result["details"] = " ".join(parts).strip()

                except IndexError:
                    # 处理潜在的索引错误，回退
                    if potential_name_index < len(parts):
                        del parts[potential_name_index]
                        result["details"] = " ".join(parts).strip()

            elif len(parts) == 1 and parts[0] and str_len_func(parts[0]) <= max_len:
                # 如果详情只有一个部分且长度合适，也认为是姓名
                result["name"] = parts[0].strip()
                result["details"] = ""

        # 最后再次清理详情中的省市区，以防姓名提取后又暴露出来
        ParseAddress.handler_detail(result)

        return result  # 返回更新后的字典

    @staticmethod
    def handler_detail(result):
        """
        清洗地址详情字段，移除开头的省、市、区名称。

        Args:
            result (dict): 解析结果字典，包含 'province', 'city', 'area', 'details'。

        Returns:
            dict: 更新后的 result 字典。
        """
        details = result.get("details", "")
        if details and len(details) > 1:  # 详情非空且长度大于1才处理
            keys_to_check = ["province", "city", "area"]
            modified = True
            while modified:  # 循环处理，因为移除省后可能暴露市
                modified = False
                for key in keys_to_check:
                    value = result.get(key, "")
                    # 要求 value 至少有一个字符，并且 details 以 value 开头
                    if value and details.startswith(value):
                        # 移除匹配的省/市/区，并去除前导空格
                        details = details[len(value) :].lstrip(" ")
                        modified = True
                        break  # 每次只移除一个，然后重新检查
            result["details"] = details
        return result


# --- 使用示例 ---
# if __name__ == '__main__':
#     # 实例化解析器
#     parser = ParseAddress()
#
#     # 测试地址
#     address1 = "北京市朝阳区姚家园路105号院3号楼10层1001室 张三 13800138000"
#     address2 = "上海市浦东新区张江高科技园区XX路100号 YYY大厦 501室 李四 收件人 电话：021-12345678 邮编 201203"
#     address3 = "广东省深圳市南山区科技园南区ZZZ路1号 18812345678 王五"
#     address4 = "江苏省南京市玄武区 收货人：赵六 手机号码：13987654321 详细地址：中山路10号"
#     address5 = "福建省福州市鼓楼区五一北路1号 力宝天马广场 13512345678 林先生" # 测试姓名在最后
#     address6 = "新疆维吾尔自治区乌鲁木齐市天山区解放北路100号 13098765432 阿凡提" # 测试特殊区域和姓名
#     address7 = "湖北省武汉市洪山区珞喻路1037号华中科技大学东校区 某某某 15811112222" # 测试学校地址
#     address8 = "四川省成都市武侯区人民南路四段1号 邮编:610041 联系电话：028-88888888 陈女士" # 测试邮编电话混杂
#
#     addresses = [address1, address2, address3, address4, address5, address6, address7, address8]
#
#     for i, addr in enumerate(addresses):
#         print(f"\n--- 解析地址 {i+1} ---")
#         print(f"原始地址: {addr}")
#         results = parser.parse(addr)
#         for res in results:
#             print(f"解析结果: {res}")
