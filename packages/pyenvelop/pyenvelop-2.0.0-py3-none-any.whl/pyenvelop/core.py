from typing import Dict, Union, Optional, List, Any
import json
import re
from pydantic import BaseModel, Field
import xml.etree.ElementTree as ET
from pydantic import validator
from pydantic import ConfigDict, field_validator
from pydantic.functional_validators import model_validator

"""
pyenvelop 2.0.0
一个用于处理信封式数据结构的 Python 包
"""

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

class DataSet(List[Dict[str, str]]):
    """
    DataSet类是一个列表类型的容器，用于存储多行数据。
    继承自List[Dict[str, str]]，每个元素都是字典。
    """
    def __init__(self, data: Optional[List[Dict]] = None) -> None:
        """
        初始化DataSet对象。
        
        Args:
            data: 数据列表，每个元素都是字典
        """
        super().__init__()
        if data:
            for item in data:
                if isinstance(item, dict):
                    self.append(item)
                else:
                    raise TypeError("data must be list of dict")

    def set_row(self, data: Dict[str, str], index: Optional[int] = None) -> None:
        """
        设置一行数据。
        
        Args:
            data: 数据字典
            index: 可选的行索引，如果提供则在指定位置插入/更新
        """
        if not isinstance(data, dict):
            raise TypeError("data must be dict")
        
        if index is not None:
            if index < 0 or index >= len(self):
                raise IndexError("index out of range")
            self[index] = data
        else:
            # 检查是否存在相同id的行
            row_id = data.get("id")
            if row_id is not None:
                for i, existing_row in enumerate(self):
                    if existing_row.get("id") == row_id:
                        self[i] = data
                        return
            self.append(data)

    def set_rows(self, rows: List[Dict[str, str]], start_index: Optional[int] = None) -> None:
        """
        设置多行数据。
        
        Args:
            rows: 数据行列表
            start_index: 可选的起始行索引
        """
        if start_index is not None:
            if start_index < 0:
                raise IndexError("start_index must be non-negative")
            for i, row in enumerate(rows):
                if start_index + i < len(self):
                    self.set_row(row, start_index + i)
                else:
                    self.set_row(row)
        else:
            for row in rows:
                self.set_row(row)

    def get_row(self, index: int = 0) -> Optional[Dict[str, str]]:
        """
        获取指定索引的行。
        
        Args:
            index: 行索引，默认为0
            
        Returns:
            字典对象，如果索引越界则返回None
        """
        if index < 0 or index >= len(self):
            return None
        return self[index]

    def get_rows(self, start_index: int = 0, count: Optional[int] = None) -> List[Dict[str, str]]:
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
            count = len(self) - start_index
        end_index = min(start_index + count, len(self))
        if start_index >= end_index:
            return []
        return self[start_index:end_index]

    def merge(self, other: 'DataSet') -> None:
        """
        合并另一个数据集。
        
        Args:
            other: 要合并的数据集
        """
        if not isinstance(other, DataSet):
            raise TypeError("other must be DataSet")
        for row in other:
            self.set_row(row)

    def clone(self) -> 'DataSet':
        """
        克隆数据集。
        
        Returns:
            新的DataSet对象
        """
        new_dataset = DataSet()
        for row in self:
            new_dataset.append(row.copy())
        return new_dataset

    def to_dict(self) -> List[Dict[str, str]]:
        """
        转换为字典列表。
        
        Returns:
            字典列表
        """
        return [row.copy() for row in self]

    def to_json(self) -> str:
        """
        转换为JSON格式字符串。
        
        Returns:
            JSON格式的字符串
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(',', ':'))

    def to_xml(self) -> str:
        """
        转换为XML格式字符串。
        
        Returns:
            XML格式的字符串
        """
        if not self:
            return ""
        xml = []
        for row in self:
            xml.append("<row>")
            for k, v in row.items():
                # 转义XML特殊字符
                escaped_value = str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
                xml.append(f"<{k}>{escaped_value}</{k}>")
            xml.append("</row>")
        return "\n".join(xml)

    def __str__(self) -> str:
        """
        获取字符串表示。
        
        Returns:
            XML格式的字符串
        """
        return self.to_xml()

class Entity(Dict[str, Union[str, Data, 'Entity']]):
    """
    实体类，用于存储业务数据。
    """
    def __init__(self, **kwargs) -> None:
        """
        初始化实体对象。
        
        Args:
            **kwargs: 键值对，用于初始化节点
        """
        super().__init__()
        for k, v in kwargs.items():
            self.set_node(v, node=k)

    def __len__(self) -> int:
        """
        获取实体中节点的数量。
        
        Returns:
            节点数量
        """
        return super().__len__()

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
            if node in self:
                del self[node]
        elif isinstance(value, str):
            self[node] = value
        elif isinstance(value, dict):
            if isinstance(value, Entity):
                self[node] = value.clone()
            else:
                self[node] = Data(value)
        elif isinstance(value, list):
            self[node] = DataSet(value)
        elif isinstance(value, (Data, DataSet)):
            self[node] = value.clone()
        elif isinstance(value, Entity):
            self[node] = value.clone()
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
        value = self.get(node)
        if isinstance(value, dict):
            if isinstance(value, Entity):
                return value
            if isinstance(value, Data):
                # 将 Data 对象转换为 Entity 对象
                new_entity = Entity()
                for k, v in value.items():
                    new_entity.set_node(v, node=k)
                return new_entity
            return Data(value)
        return value

    def get_string(self, key: str) -> Optional[str]:
        """获取字符串值
        
        Args:
            key: 键名
            
        Returns:
            字符串值，如果不存在则返回None
        """
        value = self.get(key)
        if isinstance(value, str):
            return value
        if isinstance(value, Data):
            return value.get_string(key)
        return None

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
        if node not in self:
            self[node] = Data()
        if value is None:
            if key in self[node]:
                del self[node][key]
        else:
            self[node].set_item(key, value)

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
        if node not in self:
            return None
        value = self[node]
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
            if node in self and isinstance(self[node], Data):
                if name in self[node]:
                    del self[node][name]
        else:
            if node not in self:
                self[node] = Data()
            if isinstance(dataset, list):
                self[node][name] = DataSet(dataset)
            elif isinstance(dataset, DataSet):
                self[node][name] = dataset.clone()
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
        if node not in self:
            return None
        if not isinstance(self[node], Data):
            return None
        value = self[node].get(name)
        if not isinstance(value, DataSet):
            return None
        return value

    def delete_node(self, node: str) -> None:
        """
        删除节点。
        
        Args:
            node: 节点名称
        """
        if node in self:
            del self[node]

    def clone(self) -> 'Entity':
        """
        克隆实体对象。
        
        Returns:
            新的实体对象
        """
        new_entity = Entity()
        for node, value in self.items():
            if value is None:
                new_entity[node] = None
            elif isinstance(value, str):
                new_entity[node] = value
            elif isinstance(value, Data):
                new_entity[node] = value.clone()
            elif isinstance(value, DataSet):
                new_entity[node] = value.clone()
            elif isinstance(value, Entity):
                new_entity[node] = value.clone()
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
        for node, value in self.items():
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
        if not self:
            return ""
    
        xml = []
        for key, value in self.items():
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
    EnvelopHead类继承自Entity，用于存储信封头部信息。
    """
    def __init__(self, **kwargs):
        super().__init__()
        # 只在没有提供值时设置默认值
        if 'success' not in kwargs:
            self.set_node_item("success", "true")
        if 'message' not in kwargs:
            self.set_node_item("message", "执行成功")
        # 设置用户提供的值
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.set_node(Data(value), node=key)
            elif isinstance(value, list):
                self.set_node(DataSet(value), node=key)
            else:
                self.set_node_item(key, str(value))

    def to_xml_element(self) -> ET.Element:
        """转换为XML元素"""
        root = ET.Element('header')
        for node_name, node in self.items():
            if isinstance(node, Data):
                node_elem = ET.SubElement(root, node_name)
                for key, value in node.to_dict().items():
                    item_elem = ET.SubElement(node_elem, key)
                    item_elem.text = str(value)
            elif isinstance(node, DataSet):
                node_elem = ET.SubElement(root, node_name)
                for item in node.to_dict():
                    item_elem = ET.SubElement(node_elem, 'item')
                    for key, value in item.items():
                        sub_elem = ET.SubElement(item_elem, key)
                        sub_elem.text = str(value)
            else:
                node_elem = ET.SubElement(root, node_name)
                node_elem.text = str(node)
        return root

class EnvelopBody(Entity):
    """
    EnvelopBody类继承自Entity，用于存储信封主体信息。
    """
    def __init__(self, data: Optional[Dict] = None):
        super().__init__()
        if data:
            for k, v in data.items():
                if isinstance(v, dict):
                    self.set_node(Data(v), node=k)
                elif isinstance(v, list):
                    if all(isinstance(item, dict) for item in v):
                        self.set_node_dataset(k, DataSet(v))
                    else:
                        self.set_node_item(k, str(v))
                else:
                    self.set_node_item(k, str(v))

    def to_xml_element(self) -> ET.Element:
        """转换为XML元素"""
        root = ET.Element('body')
        for node_name, node in self.items():
            if isinstance(node, Data):
                node_elem = ET.SubElement(root, node_name)
                for key, value in node.to_dict().items():
                    item_elem = ET.SubElement(node_elem, key)
                    item_elem.text = str(value)
            elif isinstance(node, DataSet):
                node_elem = ET.SubElement(root, node_name)
                for item in node.to_dict():
                    item_elem = ET.SubElement(node_elem, 'item')
                    for key, value in item.items():
                        sub_elem = ET.SubElement(item_elem, key)
                        sub_elem.text = str(value)
            else:
                node_elem = ET.SubElement(root, node_name)
                node_elem.text = str(node)
        return root

class Envelop(BaseModel):
    """
    信封类，用于封装请求和响应数据。
    """
    header: EnvelopHead = Field(default_factory=EnvelopHead)
    body: EnvelopBody = Field(default_factory=EnvelopBody)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **kwargs):
        # 如果提供了header或body的字典数据，转换为对应的对象
        if "header" in kwargs and isinstance(kwargs["header"], dict):
            kwargs["header"] = EnvelopHead(**kwargs["header"])
        if "body" in kwargs and isinstance(kwargs["body"], dict):
            kwargs["body"] = EnvelopBody(**kwargs["body"])
        super().__init__(**kwargs)

    @field_validator('header', mode='before')
    @classmethod
    def validate_header(cls, v):
        if isinstance(v, dict):
            return EnvelopHead(**v)
        if not isinstance(v, EnvelopHead):
            raise TypeError("header must be EnvelopHead")
        return v

    @field_validator('body', mode='before')
    @classmethod
    def validate_body(cls, v):
        if isinstance(v, dict):
            return EnvelopBody(**v)
        if not isinstance(v, EnvelopBody):
            raise TypeError("body must be EnvelopBody")
        return v

    @model_validator(mode='after')
    def validate_types(self):
        if not isinstance(self.header, EnvelopHead):
            raise TypeError("header must be EnvelopHead")
        if not isinstance(self.body, EnvelopBody):
            raise TypeError("body must be EnvelopBody")
        return self

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'header':
            if not isinstance(value, (EnvelopHead, dict)):
                raise TypeError("header must be EnvelopHead")
        elif name == 'body':
            if not isinstance(value, (EnvelopBody, dict)):
                raise TypeError("body must be EnvelopBody")
        super().__setattr__(name, value)

    def set_header(self, header: EnvelopHead) -> None:
        """设置信封头部"""
        if not isinstance(header, EnvelopHead):
            raise TypeError("header must be EnvelopHead")
        self.header = header

    def get_header(self) -> EnvelopHead:
        """获取信封头部"""
        return self.header

    def set_body(self, body: EnvelopBody) -> None:
        """设置信封主体"""
        if not isinstance(body, EnvelopBody):
            raise TypeError("body must be EnvelopBody")
        self.body = body

    def get_body(self) -> EnvelopBody:
        """获取信封主体"""
        return self.body

    def validate_envelop(self, rules: Optional[Dict] = None) -> bool:
        """验证信封数据是否符合规则"""
        if rules is None:
            return True

        # 验证头部
        if "header" in rules:
            header_rules = rules["header"]
            for field, validator in header_rules.items():
                value = self.header.get_node_item(field)
                if value is None or not validator(value):
                    return False

        return True

    def validate(self, rules: Optional[Dict] = None) -> bool:
        """验证信封数据是否符合规则（兼容旧版本）"""
        return self.validate_envelop(rules)

    def to_dict(self) -> dict:
        """转换为字典"""
        header_dict = {}
        for node_name, node in self.header.items():
            if isinstance(node, (Data, DataSet)):
                header_dict[node_name] = node.to_dict()
            else:
                header_dict[node_name] = str(node)

        body_dict = {}
        for node_name, node in self.body.items():
            if isinstance(node, (Data, DataSet)):
                body_dict[node_name] = node.to_dict()
            else:
                body_dict[node_name] = str(node)

        return {
            'header': header_dict,
            'body': body_dict
        }

    def to_json(self) -> str:
        """转换为JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(',', ':'))

    def to_xml(self) -> str:
        """转换为XML"""
        root = ET.Element('envelop')
        if self.header:
            header_elem = ET.SubElement(root, 'header')
            header_elem.append(self.header.to_xml_element())
        if self.body:
            body_elem = ET.SubElement(root, 'body')
            body_elem.append(self.body.to_xml_element())
        return ET.tostring(root, encoding='unicode')

    def __str__(self) -> str:
        return self.to_xml()

    def clone(self) -> 'Envelop':
        """克隆对象"""
        return Envelop(
            header=self.header.clone().to_dict(),
            body=self.body.clone().to_dict()
        )