from typing import Dict, Union, Optional, List, Any
import json
import re

class Data(Dict[str, Union[str, 'DataSet']]):
    """
    Data类是一个字典类型的容器，用于存储键值对数据。
    支持存储字符串值和DataSet类型的值。
    继承自Dict，键为字符串，值可以是字符串或DataSet。
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        初始化Data对象。
        支持从字典或关键字参数创建Data对象。
        
        Args:
            *args: 位置参数，可以是字典
            **kwargs: 关键字参数，键为字符串，值可以是字符串或DataSet
        """
        super().__init__()
        
        # 处理位置参数（字典）
        if args and isinstance(args[0], dict):
            for k, v in args[0].items():
                if isinstance(v, dict):
                    self[k] = Data(v)
                elif isinstance(v, list):
                    if all(isinstance(item, dict) for item in v):
                        self[k] = DataSet(v)
                    else:
                        self[k] = str(v)
                else:
                    self[k] = str(v)
        
        # 处理关键字参数
        for k, v in kwargs.items():
            if isinstance(v, dict):
                self[k] = Data(v)
            elif isinstance(v, list):
                if all(isinstance(item, dict) for item in v):
                    self[k] = DataSet(v)
                else:
                    self[k] = str(v)
            else:
                self[k] = str(v)

    def set_string(self, k: str, v: str) -> None:
        """
        设置字符串值。
        
        Args:
            k: 键
            v: 值
        """
        self[k] = v

    def get_string(self, k: str) -> Optional[str]:
        """
        获取字符串值。
        
        Args:
            k: 键
            
        Returns:
            字符串值，如果不存在则返回None
        """
        return self.get(k)

    def get_int(self, k: str) -> Optional[int]:
        """
        获取整数值。
        
        Args:
            k: 键名
            
        Returns:
            整数值，如果转换失败则返回None
        """
        try:
            return int(self.get(k))
        except (ValueError, TypeError):
            return None

    def get_long(self, k: str) -> Optional[int]:
        """
        获取长整数值。
        
        Args:
            k: 键名
            
        Returns:
            长整数值，如果转换失败则返回None
        """
        try:
            return int(self.get(k))
        except (ValueError, TypeError):
            return None

    def get_float(self, k: str) -> Optional[float]:
        """
        获取浮点数值。
        
        Args:
            k: 键名
            
        Returns:
            浮点数值，如果转换失败则返回None
        """
        try:
            return float(self.get(k))
        except (ValueError, TypeError):
            return None

    def get_bool(self, k: str) -> Optional[bool]:
        """
        获取布尔值。
        
        Args:
            k: 键名
            
        Returns:
            布尔值，如果转换失败则返回None
        """
        try:
            value = self.get(k)
            if value is None:
                return None
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on')
            if isinstance(value, (int, float)):
                return bool(value)
            return None
        except (ValueError, TypeError):
            return None

    def set_dataset(self, k: str, v: 'DataSet') -> None:
        """
        设置数据集。
        
        Args:
            k: 键
            v: 数据集
        """
        self[k] = v

    def get_dataset(self, k: str) -> Optional['DataSet']:
        """
        获取数据集。
        
        Args:
            k: 键名
            
        Returns:
            数据集，如果不存在或类型不匹配则返回None
        """
        value = self.get(k)
        if isinstance(value, DataSet):
            return value
        return None

    def set_dict(self, k: str, v: Dict[str, Any]):
        """
        设置字典值。
        
        Args:
            k: 键名
            v: 字典值
        """
        self[k] = v

    def get_dict(self, k: str) -> Optional[Dict[str, Any]]:
        """
        获取字典值。
        
        Args:
            k: 键名
            
        Returns:
            字典值，如果不存在则返回None
        """
        return self.get(k)

    def set_list(self, k: str, v: List[Any]):
        """
        设置列表值。
        
        Args:
            k: 键名
            v: 列表值
        """
        self[k] = v

    def get_list(self, k: str) -> Optional[List[Any]]:
        """
        获取列表值。
        
        Args:
            k: 键名
            
        Returns:
            列表值，如果不存在则返回None
        """
        return self.get(k)

    def get_string_item(self, k) -> Optional[str]:
        """
        获取字符串值。
        
        Args:
            k: 键名
            
        Returns:
            如果值存在且为字符串类型，返回该值；否则返回None
        """
        item = self.get(k)
        if isinstance(item, str) is False:
            return None
        return item

    def to_json(self) -> str:
        """
        将数据转换为JSON格式字符串。
        
        Returns:
            JSON格式的字符串
        """
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    def to_xml(self) -> str:
        """
        转换为XML格式。
    
        Returns:
            XML格式的字符串
        """
        if not self:
            return ""
            
        xml = []
        for key, value in self.items():
            if isinstance(value, (Data, DataSet, Entity)):
                xml_value = value.to_xml()
                if xml_value:  # 只有当子节点有内容时才添加
                    xml.append(f"<{key}>{xml_value}</{key}>")
            elif isinstance(value, str) and value.startswith('<') and value.endswith('>'):
                # 如果值已经是XML格式，直接使用
                xml.append(f"<{key}>{value}</{key}>")
            else:
                # 转义XML特殊字符
                escaped_value = str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
                xml.append(f"<{key}>{escaped_value}</{key}>")
        return "\n".join(xml)

    def get_integer_item(self, k: str) -> Optional[int]:
        """
        获取整数值。
        
        Args:
            k: 键名
            
        Returns:
            如果值存在且可以转换为整数，返回该值；否则返回None
        """
        item = self.get(k)
        if isinstance(item, (int, str)):
            try:
                return int(item)
            except ValueError:
                return None
        return None

    def get_integer2_item(self, k: str) -> int:
        """
        获取整数值，如果转换失败返回0。
        
        Args:
            k: 键名
            
        Returns:
            如果值存在且可以转换为整数，返回该值；否则返回0
        """
        item = self.get_integer_item(k)
        return item if item is not None else 0

    def get_long_item(self, k: str) -> Optional[int]:
        """
        获取长整数值。
        
        Args:
            k: 键名
            
        Returns:
            如果值存在且可以转换为长整数，返回该值；否则返回None
        """
        item = self.get(k)
        if isinstance(item, (int, str)):
            try:
                # 检查是否超出Python int的范围
                value = int(item)
                if value > 9223372036854775807:  # 最大长整型值
                    return None
                return value
            except ValueError:
                return None
        return None

    def get_long2_item(self, k: str) -> int:
        """
        获取长整数值，如果转换失败返回0。
        
        Args:
            k: 键名
            
        Returns:
            如果值存在且可以转换为长整数，返回该值；否则返回0
        """
        item = self.get_long_item(k)
        return item if item is not None else 0

    def get_big_decimal(self, k: str) -> Optional[float]:
        """
        获取浮点数值。
        
        Args:
            k: 键名
            
        Returns:
            如果值存在且可以转换为浮点数，返回该值；否则返回None
        """
        item = self.get(k)
        if isinstance(item, (int, float, str)):
            try:
                return float(item)
            except ValueError:
                return None
        return None

    def get_datas(self) -> List[str]:
        """
        获取所有字符串值。
        
        Returns:
            包含所有字符串值的列表
        """
        return [v for v in self.values() if isinstance(v, str)]

    def get_datasets(self) -> Dict[str, 'DataSet']:
        """
        获取所有数据集。
        
        Returns:
            包含所有DataSet的字典
        """
        return {k: v for k, v in self.items() if isinstance(v, DataSet)}

    def set_integer_item(self, k: str, v: int):
        """
        设置整数值。
        
        Args:
            k: 键名
            v: 整数值
        """
        self[k] = str(v)

    def set_integer2_item(self, k: str, v: int):
        """
        设置整数值。
        
        Args:
            k: 键名
            v: 整数值
        """
        self[k] = str(v)

    def set_long_item(self, k: str, v: int):
        """
        设置长整数值。
        
        Args:
            k: 键名
            v: 长整数值
        """
        self[k] = str(v)

    def set_long2_item(self, k: str, v: int):
        """
        设置长整数值。
        
        Args:
            k: 键名
            v: 长整数值
        """
        self[k] = str(v)

    def set_big_decimal_item(self, k: str, v: float):
        """
        设置浮点数值。
        
        Args:
            k: 键名
            v: 浮点数值
        """
        self[k] = str(v)

    def get_int(self, k: str) -> Optional[int]:
        """
        获取整数值。
        
        Args:
            k: 键
            
        Returns:
            整数值，如果不存在或无法转换则返回None
        """
        v = self.get(k)
        if v is None:
            return None
        try:
            return int(v)
        except (ValueError, TypeError):
            return None

    def get_long(self, k: str) -> Optional[int]:
        """
        获取长整数值。
        
        Args:
            k: 键
            
        Returns:
            长整数值，如果不存在或无法转换则返回None
        """
        v = self.get(k)
        if v is None:
            return None
        try:
            return int(v)
        except (ValueError, TypeError):
            return None

    def get_float(self, k: str) -> Optional[float]:
        """
        获取浮点数值。
        
        Args:
            k: 键
            
        Returns:
            浮点数值，如果不存在或无法转换则返回None
        """
        v = self.get(k)
        if v is None:
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    def get_bool(self, k: str) -> Optional[bool]:
        """
        获取布尔值。
        
        Args:
            k: 键
            
        Returns:
            布尔值，如果不存在或无法转换则返回None
        """
        v = self.get(k)
        if v is None:
            return None
        try:
            return bool(v)
        except (ValueError, TypeError):
            return None

    def clone(self) -> 'Data':
        """
        克隆数据对象。
        
        Returns:
            新的数据对象
        """
        new_data = Data()
        for k, v in self.items():
            if isinstance(v, DataSet):
                new_data.set_dataset(k, v.clone())
            else:
                new_data.set_string(k, v)
        return new_data

    def set_item(self, key: str, value: Any) -> None:
        """设置键值对
        
        Args:
            key: 键名
            value: 值，可以是字符串、数字、布尔值、字典、列表等
        """
        if not isinstance(key, str):
            raise TypeError('key must be string')
        self[key] = value
    
    def get_item(self, key: str) -> Any:
        """获取键对应的值
        
        Args:
            key: 键名
            
        Returns:
            键对应的值，如果键不存在则返回None
        """
        if not isinstance(key, str):
            raise TypeError('key must be string')
        return self.get(key)

    def __str__(self) -> str:
        """
        获取字符串表示。
        
        Returns:
            XML格式的字符串
        """
        return self.to_xml()

    def to_dict(self) -> Dict:
        """转换为字典
        
        Returns:
            字典对象
        """
        result = {}
        for key, value in self.items():
            if isinstance(value, Data):
                result[key] = value.to_dict()
            elif isinstance(value, DataSet):
                result[key] = value.to_dict()
            else:
                result[key] = str(value)
        return result

    def to_json(self) -> str:
        """
        将数据转换为JSON格式字符串。
        
        Returns:
            JSON格式的字符串
        """
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

class DataSet:
    """
    数据集类，用于存储和管理多行数据。
    """
    def __init__(self, rows: Optional[List[Union[Dict, Data]]] = None) -> None:
        """
        初始化数据集对象。
        
        Args:
            rows: 初始数据行列表，每个元素可以是字典或Data对象
        """
        self._rows: List[Data] = []
        if rows:
            for row in rows:
                if isinstance(row, dict):
                    self._rows.append(Data(**row))
                elif isinstance(row, Data):
                    self._rows.append(row.clone())
                else:
                    raise TypeError('row must be dict or Data')

    def __getitem__(self, index: int) -> Data:
        """
        支持下标访问操作
        
        Args:
            index: 行索引
            
        Returns:
            Data对象
            
        Raises:
            IndexError: 索引超出范围
        """
        if not isinstance(index, int):
            raise TypeError('index must be integer')
        if index < 0 or index >= len(self._rows):
            raise IndexError('index out of range')
        return self._rows[index]

    def __len__(self) -> int:
        """
        获取数据集中的行数。
        
        Returns:
            行数
        """
        return len(self._rows)

    def set_row(self, row: Union[Dict, Data], index: Optional[int] = None) -> None:
        """设置数据行
        
        Args:
            row: 数据行，可以是字典或Data对象
            index: 行索引，如果为None则追加到末尾或更新已存在的行
            
        Raises:
            TypeError: 如果row类型不正确
            IndexError: 如果index超出范围
        """
        if not isinstance(row, (dict, Data)):
            raise TypeError("row must be dict or Data")
            
        if index is not None:
            if index < 0 or index >= len(self._rows):
                raise IndexError("index out of range")
            self._rows[index] = row
        else:
            # 检查是否存在相同id的行
            row_id = row.get("id")
            if row_id is not None:
                for i, existing_row in enumerate(self._rows):
                    if existing_row.get("id") == row_id:
                        self._rows[i] = row
                        return
            self._rows.append(row)

    def get_row(self, index: int) -> Optional[Data]:
        """获取指定索引位置的数据行
        
        Args:
            index: 行索引
            
        Returns:
            Data对象，如果索引无效则返回None
        """
        if not isinstance(index, int):
            raise TypeError('index must be integer')
        if index < 0 or index >= len(self._rows):
            return None
        return self._rows[index]

    def get_rows(self, start_index: int = 0, count: int = None) -> List[Data]:
        """
        获取指定范围的行数据。
        
        Args:
            start_index: 起始索引，默认为0
            count: 获取的行数，默认为None（获取到末尾）
            
        Returns:
            行数据列表
        """
        if start_index < 0:
            return []
        if count is None:
            count = len(self._rows) - start_index
        end_index = min(start_index + count, len(self._rows))
        if start_index >= end_index:
            return []
        return self._rows[start_index:end_index]

    def add_row(self, row: Union[Dict, Data]) -> None:
        """添加数据行
        
        Args:
            row: 数据行，可以是字典或Data对象
            
        Raises:
            TypeError: row参数类型错误
        """
        self.set_row(row)

    def set_rows(self, rows: List[Union[Dict[str, str], Data]], start_index: Optional[int] = None) -> None:
        """
        设置多行数据。
        如果指定了起始索引，则从该位置开始插入或更新数据；
        如果没有指定起始索引，则追加到末尾。
        
        Args:
            rows: 数据行列表
            start_index: 可选的起始行索引
        """
        if start_index is not None:
            for i, row in enumerate(rows):
                if start_index + i < len(self._rows):
                    self.set_row(row)
                else:
                    self.add_row(row)
        else:
            for row in rows:
                self.add_row(row)

    def merge(self, other: 'DataSet') -> None:
        """
        合并另一个数据集到当前数据集。
        
        Args:
            other: 要合并的数据集
        """
        for row in other._rows:
            self.add_row(row)

    def clone(self) -> 'DataSet':
        """
        克隆数据集对象。
        
        Returns:
            新的数据集对象
        """
        new_dataset = DataSet()
        for row in self._rows:
            if isinstance(row, Data):
                new_dataset._rows.append(row.clone())
            else:
                new_dataset._rows.append(Data(row))
        return new_dataset

    def to_json(self) -> str:
        """
        将数据集转换为JSON格式字符串。
        
        Returns:
            JSON格式的字符串
        """
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    def to_xml(self) -> str:
        """转换为XML格式
        
        Returns:
            XML格式的字符串
        """
        if not self._rows:
            return ""
            
        xml = []
        for row in self._rows:
            xml.append("<row>")
            for key, value in row.items():
                if isinstance(value, (Data, DataSet, Entity)):
                    xml.append(f"<{key}>{value.to_xml()}</{key}>")
                else:
                    # 转义XML特殊字符
                    escaped_value = str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
                    xml.append(f"<{key}>{escaped_value}</{key}>")
            xml.append("</row>")
        return "\n".join(xml)

    def __str__(self) -> str:
        """
        获取实体的字符串表示。
        
        Returns:
            XML格式的字符串
        """
        return self.to_xml()

    def to_dict(self) -> List[Dict]:
        """转换为字典列表
        
        Returns:
            字典列表，每个字典代表一行数据
        """
        return [row.to_dict() if isinstance(row, Data) else dict(row) for row in self._rows]

class Entity:
    """
    实体类，用于存储业务数据。
    """
    def __init__(self, **kwargs) -> None:
        """
        初始化实体对象。
        
        Args:
            **kwargs: 键值对，用于初始化节点
        """
        self._data = {}
        for k, v in kwargs.items():
            self.set_node(v, node=k)

    def __len__(self) -> int:
        """
        获取实体中节点的数量。
        
        Returns:
            节点数量
        """
        return len(self._data)

    def set_node(self, value: Union[str, Dict, List[Dict], Data, DataSet, 'Entity', None] = None, *, node: str = "default") -> None:
        """设置节点值
        
        Args:
            value: 节点值，可以是字符串、字典、列表、Data、DataSet或Entity对象，默认为None
            node: 节点名称，默认为"default"
            
        Raises:
            TypeError: 参数类型错误
        """
        if not isinstance(node, str):
            raise TypeError("node must be string")
            
        if value is None:
            if node in self._data:
                del self._data[node]
        elif isinstance(value, str):
            self._data[node] = value
        elif isinstance(value, dict):
            self._data[node] = Data(value)
        elif isinstance(value, list):
            self._data[node] = DataSet(value)
        elif isinstance(value, (Data, DataSet, Entity)):
            self._data[node] = value.clone()
        else:
            raise TypeError("unsupported value type")

    def get_node(self, node: str = "default") -> Optional[Union[str, Data, DataSet, 'Entity']]:
        """获取节点值
        
        Args:
            node: 节点名称，默认为"default"
            
        Returns:
            节点值，如果节点不存在则返回None
        """
        if not isinstance(node, str):
            raise TypeError("node must be string")
        return self._data.get(node)

    def set_node_item(self, key: str, value: Any, *, node: str = "default") -> None:
        """设置节点的键值对
        
        Args:
            key: 键名
            value: 值，可以是字符串或None
            node: 节点名，默认为"default"
            
        Raises:
            TypeError: 参数类型错误
        """
        if not isinstance(key, str):
            raise TypeError('key must be string')
        if value is not None and not isinstance(value, str):
            raise TypeError('value must be string')
        if not isinstance(node, str):
            raise TypeError('node must be string')
        if node not in self._data:
            self._data[node] = Data()
        if value is None:
            if key in self._data[node]:
                del self._data[node][key]
        else:
            self._data[node].set_item(key, value)

    def get_node_item(self, key: str, *, node: str = "default") -> Optional[str]:
        """获取节点的键值对
        
        Args:
            key: 键名
            node: 节点名，默认为"default"
            
        Returns:
            键对应的值，如果节点或键不存在则返回None
        """
        if not isinstance(key, str):
            raise TypeError("key must be string")
        if not isinstance(node, str):
            raise TypeError("node must be string")
        if node not in self._data:
            return None
        value = self._data[node]
        if isinstance(value, Data):
            return value.get_item(key)
        return None

    def set_node_dataset(self, name: str, dataset: Optional[Union[List[Dict], DataSet]] = None, *, node: str = "default") -> None:
        """设置节点的数据集
        
        Args:
            name: 数据集名称
            dataset: 数据集，可以是字典列表或DataSet对象，如果为None则删除节点
            node: 节点名称，默认为"default"
            
        Raises:
            TypeError: 参数类型错误
        """
        if not isinstance(name, str):
            raise TypeError("name must be string")
        if not isinstance(node, str):
            raise TypeError("node must be string")
            
        if dataset is None:
            if node in self._data and isinstance(self._data[node], Data):
                if name in self._data[node]:
                    del self._data[node][name]
        else:
            if node not in self._data:
                self._data[node] = Data()
            if isinstance(dataset, list):
                self._data[node][name] = DataSet(dataset)
            elif isinstance(dataset, DataSet):
                self._data[node][name] = dataset.clone()
            else:
                raise TypeError("dataset must be list or DataSet")

    def get_node_dataset(self, name: str, *, node: str = "default") -> Optional[DataSet]:
        """获取节点的数据集
        
        Args:
            name: 数据集名称
            node: 节点名称，默认为"default"
            
        Returns:
            数据集对象，如果节点不存在或不是数据集则返回None
        """
        if not isinstance(name, str):
            raise TypeError("name must be string")
        if not isinstance(node, str):
            raise TypeError("node must be string")
        if node not in self._data:
            return None
        if not isinstance(self._data[node], Data):
            return None
        value = self._data[node].get(name)
        if not isinstance(value, DataSet):
            return None
        return value

    def delete_node(self, node: str) -> None:
        """
        删除节点。
        
        Args:
            node: 节点名称
        """
        if node in self._data:
            del self._data[node]

    def clone(self) -> 'Entity':
        """
        克隆实体对象。
        
        Returns:
            新的实体对象
        """
        new_entity = Entity()
        for node, value in self._data.items():
            if value is None:
                new_entity._data[node] = None
            elif isinstance(value, str):
                new_entity._data[node] = value
            elif isinstance(value, Data):
                new_entity._data[node] = value.clone()
            elif isinstance(value, DataSet):
                new_entity._data[node] = value.clone()
            elif isinstance(value, Entity):
                new_entity._data[node] = value.clone()
        return new_entity

    def get_nested_node(self, path: str) -> Optional[Union[Data, DataSet, 'Entity']]:
        """
        获取嵌套节点。
        
        Args:
            path: 节点路径，使用点号分隔，例如"level1.level2.level3"
            
        Returns:
            节点值，如果不存在则返回None
        """
        current = self
        for node in path.split('.'):
            if not isinstance(current, Entity):
                return None
            current = current.get_node(node)
            if current is None:
                return None
        return current

    def get_nested_node_item(self, name: str, path: str) -> Optional[str]:
        """
        获取嵌套节点项。
        
        Args:
            name: 项名称
            path: 节点路径，使用点号分隔，例如"level1.level2.level3"
            
        Returns:
            项值，如果不存在则返回None
        """
        node = self.get_nested_node(path)
        if isinstance(node, (Data, Entity)):
            return node.get_node_item(name) if isinstance(node, Entity) else node.get_string(name)
        return None

    def get_nested_node_dataset(self, name: str, path: str) -> Optional[DataSet]:
        """
        获取嵌套节点数据集。
        
        Args:
            name: 数据集名称
            path: 节点路径，使用点号分隔，例如"level1.level2.level3"
            
        Returns:
            数据集，如果不存在则返回None
        """
        node = self.get_nested_node(path)
        if isinstance(node, (Data, Entity)):
            return node.get_node_dataset(name) if isinstance(node, Entity) else node.get_dataset(name)
        return None

    def to_dict(self) -> Dict:
        """转换为字典
        
        Returns:
            字典对象
        """
        result = {}
        for node, value in self._data.items():
            if isinstance(value, Data):
                result[node] = value.to_dict()
            elif isinstance(value, DataSet):
                result[node] = value.to_dict()
            elif isinstance(value, Entity):
                result[node] = value.to_dict()
            else:
                result[node] = str(value)
        return result

    def to_json(self) -> str:
        """
        转换为JSON格式。
    
        Returns:
            JSON格式的字符串
        """
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    def to_xml(self) -> str:
        """
        转换为XML格式。
    
        Returns:
            XML格式的字符串
        """
        if len(self._data) == 0:
            return ""
    
        xml = []
        for key, value in self._data.items():
            if isinstance(value, (Data, DataSet, Entity)):
                xml_value = value.to_xml()
                if xml_value:  # 只有当子节点有内容时才添加
                    xml.append(f"<{key}>{xml_value}</{key}>")
            else:
                # 转义XML特殊字符
                escaped_value = str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
                xml.append(f"<{key}>{escaped_value}</{key}>")
        return "\n".join(xml)

    def __str__(self) -> str:
        """
        获取实体的字符串表示。
        
        Returns:
            XML格式的字符串
        """
        return self.to_xml()

class EnvelopHead(Entity):
    """
    信封头部类，继承自Entity。
    """
    def __init__(self, **kwargs):
        """
        初始化信封头部
        
        Args:
            **kwargs: 关键字参数，用于初始化头部属性
        """
        super().__init__()
        # 设置默认值
        self.set_node_item("success", "true")
        self.set_node_item("message", "执行成功")

    def clone(self) -> 'EnvelopHead':
        """
        克隆信封头部对象。
        
        Returns:
            新的信封头部对象
        """
        new_header = EnvelopHead()
        for k, v in self._data.items():
            if isinstance(v, (Data, DataSet, Entity)):
                new_header._data[k] = v.clone()
            else:
                new_header._data[k] = v
        return new_header

    def to_json(self) -> str:
        """
        转换为JSON格式。
        
        Returns:
            JSON字符串
        """
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    def to_xml(self) -> str:
        """转换为XML格式
        
        Returns:
            XML字符串
        """
        xml = ['<head>']
        for k, v in self._data.items():
            if isinstance(v, (Data, DataSet, Entity)):
                xml.append(f'<{k}>{v.to_xml()}</{k}>')
            else:
                # 转义XML特殊字符
                escaped_value = str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
                xml.append(f'<{k}>{escaped_value}</{k}>')
        xml.append('</head>')
        return '\n'.join(xml)

    def to_dict(self) -> Dict:
        """转换为字典
        
        Returns:
            字典对象
        """
        result = {}
        # 添加所有节点数据
        for node_name, node_data in self._data.items():
            if isinstance(node_data, (Data, DataSet, Entity)):
                result[node_name] = node_data.to_dict()
            else:
                result[node_name] = node_data
                
        return result

class EnvelopBody(Entity):
    """
    信封体类，继承自Entity。
    用于存储业务数据。
    """
    def __init__(self, data: Optional[Dict] = None):
        """
        初始化信封体对象。
        支持从字典或关键字参数创建信封体对象。
        
        Args:
            data: 初始数据字典
        """
        super().__init__()
        if data:
            for node, value in data.items():
                if isinstance(value, dict):
                    self.set_node(node, Data(**value))
                elif isinstance(value, list):
                    self.set_node_dataset(node, value)
                else:
                    self.set_node(node, str(value))

    def clone(self) -> 'EnvelopBody':
        """
        克隆信封体对象。
        
        Returns:
            新的信封体对象
        """
        new_body = EnvelopBody()
        for k, v in self._data.items():
            if isinstance(v, (Data, DataSet, Entity)):
                new_body._data[k] = v.clone()
            else:
                new_body._data[k] = v
        return new_body

    def to_xml(self) -> str:
        """转换为XML格式
        
        Returns:
            XML格式的字符串
        """
        xml = ['<body>']
        for k, v in self._data.items():
            if isinstance(v, (Data, DataSet, Entity)):
                xml.append(f'<{k}>{v.to_xml()}</{k}>')
            else:
                # 转义XML特殊字符
                escaped_value = str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
                xml.append(f'<{k}>{escaped_value}</{k}>')
        xml.append('</body>')
        return '\n'.join(xml)

    def __str__(self) -> str:
        return self.to_xml()

    def to_dict(self) -> Dict:
        """转换为字典
        
        Returns:
            字典对象
        """
        result = {}
        for node, value in self._data.items():
            if isinstance(value, Data):
                result[node] = value.to_dict()
            elif isinstance(value, DataSet):
                result[node] = value.to_dict()
            elif isinstance(value, Entity):
                result[node] = value.to_dict()
            else:
                result[node] = str(value)
        return result

    def to_json(self) -> str:
        """转换为JSON格式
        
        Returns:
            JSON格式的字符串
        """
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

class Envelop:
    """
    信封类，用于封装消息的头部和主体。
    支持通过属性或方法访问头部和主体。
    """
    def __init__(self, header: Optional[Dict] = None, body: Optional[Dict] = None):
        """
        初始化信封对象。
        
        Args:
            header: 头部数据字典
            body: 主体数据字典
            
        Raises:
            TypeError: 如果header或body的类型不正确
        """
        self._header = EnvelopHead()
        self._body = EnvelopBody()
        
        if header is not None:
            if not isinstance(header, dict):
                raise TypeError("header must be dict or None")
            for key, value in header.items():
                if isinstance(value, dict):
                    if 'dataset' in value:  # 如果是数据集
                        if isinstance(value['dataset'], list):
                            dataset = DataSet(value['dataset'])
                            self._header.set_node_dataset('dataset', dataset=dataset, node=key)
                        else:
                            data = Data(value)
                            self._header.set_node(data, node=key)
                    else:
                        data = Data(value)
                        self._header.set_node(data, node=key)
                else:
                    self._header.set_node_item(key, str(value))
                
        if body is not None:
            if not isinstance(body, dict):
                raise TypeError("body must be dict or None")
            for key, value in body.items():
                if isinstance(value, dict):
                    if 'dataset' in value:  # 如果是数据集
                        if isinstance(value['dataset'], list):
                            dataset = DataSet(value['dataset'])
                            self._body.set_node_dataset('dataset', dataset=dataset, node=key)
                        else:
                            data = Data(value)
                            self._body.set_node(data, node=key)
                    else:
                        data = Data(value)
                        self._body.set_node(data, node=key)
                else:
                    self._body.set_node_item(key, str(value))

    @property
    def header(self) -> EnvelopHead:
        """获取头部对象"""
        return self._header

    @header.setter
    def header(self, value: EnvelopHead) -> None:
        """设置头部对象"""
        if not isinstance(value, EnvelopHead):
            raise TypeError("header must be EnvelopHead")
        self._header = value

    @property
    def body(self) -> EnvelopBody:
        """获取主体对象"""
        return self._body

    @body.setter
    def body(self, value: EnvelopBody) -> None:
        """设置主体对象"""
        if not isinstance(value, EnvelopBody):
            raise TypeError("body must be EnvelopBody")
        self._body = value

    def set_header(self, header: EnvelopHead) -> None:
        """设置头部对象"""
        self.header = header

    def get_header(self) -> EnvelopHead:
        """获取头部对象"""
        return self.header

    def set_body(self, body: EnvelopBody) -> None:
        """设置主体对象"""
        self.body = body

    def get_body(self) -> EnvelopBody:
        """获取主体对象"""
        return self.body

    def validate(self, rules: Optional[Dict] = None) -> bool:
        """
        验证信封是否有效。
        
        Args:
            rules: 验证规则字典
            
        Returns:
            验证是否通过
        """
        if rules is None:
            return True
            
        # 验证头部
        if "header" in rules:
            header_rules = rules["header"]
            for field, validator in header_rules.items():
                value = self._header.get_node_item(field)
                if value is None or not validator(value):
                    return False
                    
        return True
    
    def to_json(self) -> str:
        """
        转换为JSON格式。
        
        Returns:
            JSON格式的字符串
        """
        data = self.to_dict()
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    
    def to_xml(self) -> str:
        """
        转换为XML格式。
        
        Returns:
            XML格式的字符串
        """
        xml = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml.append('<envelop>')
        xml.append(self._header.to_xml())
        xml.append(self._body.to_xml())
        xml.append('</envelop>')
        return '\n'.join(xml)

    def to_dict(self) -> Dict:
        """
        转换为字典格式。
        
        Returns:
            字典对象
        """
        return {
            "header": self._header.to_dict(),
            "body": self._body.to_dict()
        }

    def __str__(self) -> str:
        """
        获取字符串表示。
        
        Returns:
            XML格式的字符串
        """
        return self.to_xml()

    def clone(self) -> 'Envelop':
        """
        克隆信封对象。
        
        Returns:
            新的信封对象
        """
        new_envelop = Envelop()
        new_envelop._header = self._header.clone()
        new_envelop._body = self._body.clone()
        return new_envelop 