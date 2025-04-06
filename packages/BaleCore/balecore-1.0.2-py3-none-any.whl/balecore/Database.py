import json
import os
from typing import Dict, List, Optional, Union, Any
from uuid import uuid4
import time
from copy import deepcopy

class Database:
    def __init__(self, name: str = "database", autocommit: bool = True):
        self.name = name
        self.file_path = f"{name}.json"
        self.backup_path = f"{name}_backup.json"
        self.autocommit = autocommit
        self.transaction_stack = []
        self.data = self._load_database()
        if "_metadata" not in self.data:
            self.data["_metadata"] = {
                "version": "1.0",
                "created_at": time.time(),
                "last_modified": time.time()
            }
            self._commit()

    def _load_database(self) -> Dict:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if "tables" not in data:
                    data["tables"] = {}
                if "indexes" not in data:
                    data["indexes"] = {}
                if "_metadata" not in data:
                    data["_metadata"] = {
                        "version": "1.0",
                        "created_at": time.time(),
                        "last_modified": time.time()
                    }
                return data
        return {
            "tables": {},
            "indexes": {},
            "_metadata": {
                "version": "1.0",
                "created_at": time.time(),
                "last_modified": time.time()
            }
        }

    def _commit(self):
        if self.autocommit and not self.transaction_stack:
            if "_metadata" not in self.data:
                self.data["_metadata"] = {
                    "version": "1.0",
                    "created_at": time.time(),
                    "last_modified": time.time()
                }
            else:
                self.data["_metadata"]["last_modified"] = time.time()
            
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)

    def _create_backup(self):
        with open(self.backup_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def restore_backup(self):
        if os.path.exists(self.backup_path):
            with open(self.backup_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            self._commit()
            return True
        return False

    def begin_transaction(self):
        self.transaction_stack.append(deepcopy(self.data))

    def commit_transaction(self):
        if self.transaction_stack:
            self.transaction_stack.pop()
            self._commit()

    def rollback_transaction(self):
        if self.transaction_stack:
            self.data = self.transaction_stack.pop()

    def create_table(self, table_name: str, table_type: str = "list", initial_data: Any = None) -> bool:
        if table_name in self.data["tables"]:
            return False
            
        if table_type == "list":
            self.data["tables"][table_name] = initial_data if initial_data is not None else []
        elif table_type == "dict":
            self.data["tables"][table_name] = initial_data if initial_data is not None else {}
        else:
            raise ValueError("Table type must be either 'list' or 'dict'")
            
        self._commit()
        return True

    def delete_table(self, table_name: str) -> bool:
        if table_name not in self.data["tables"]:
            return False
        del self.data["tables"][table_name]
        for index_name in list(self.data["indexes"].keys()):
            if index_name.startswith(f"{table_name}."):
                del self.data["indexes"][index_name]
                
        self._commit()
        return True

    def rename_table(self, old_name: str, new_name: str) -> bool:
        if old_name not in self.data["tables"] or new_name in self.data["tables"]:
            return False
            
        self.data["tables"][new_name] = self.data["tables"][old_name]
        del self.data["tables"][old_name]
        for index_name in list(self.data["indexes"].keys()):
            if index_name.startswith(f"{old_name}."):
                new_index_name = index_name.replace(f"{old_name}.", f"{new_name}.")
                self.data["indexes"][new_index_name] = self.data["indexes"][index_name]
                del self.data["indexes"][index_name]
                
        self._commit()
        return True

    def table_type(self, table_name: str) -> Optional[str]:
        if table_name not in self.data["tables"]:
            return None
            
        table_data = self.data["tables"][table_name]
        return "dict" if isinstance(table_data, dict) else "list"

    def convert_table_type(self, table_name: str, new_type: str) -> bool:
        if table_name not in self.data["tables"]:
            return False
            
        current_type = self.table_type(table_name)
        if current_type == new_type:
            return True
            
        try:
            if new_type == "list":
                if isinstance(self.data["tables"][table_name], dict):
                    self.data["tables"][table_name] = list(self.data["tables"][table_name].values())
            elif new_type == "dict":
                if isinstance(self.data["tables"][table_name], list):
                    new_dict = {}
                    for i, item in enumerate(self.data["tables"][table_name]):
                        if isinstance(item, dict) and "id" in item:
                            new_dict[item["id"]] = item
                        else:
                            new_dict[str(i)] = item
                    self.data["tables"][table_name] = new_dict
            else:
                return False
                
            self._commit()
            return True
        except Exception:
            return False

    def create_nested_table(self, parent_table: str, path: str, table_type: str = "list") -> bool:
        if parent_table not in self.data["tables"]:
            return False
            
        path_parts = path.split('.')
        current = self.data["tables"][parent_table]
        
        for part in path_parts[:-1]:
            if isinstance(current, dict):
                if part not in current:
                    current[part] = {}
                current = current[part]
            elif isinstance(current, list):
                try:
                    index = int(part)
                    if index < len(current):
                        current = current[index]
                    else:
                        return False
                except ValueError:
                    return False
            else:
                return False
                
        final_part = path_parts[-1]
        if isinstance(current, dict):
            if table_type == "list":
                current[final_part] = []
            else:
                current[final_part] = {}
            self._commit()
            return True
            
        return False

    def insert(self, table_name: str, data: Any, path: Optional[str] = None) -> bool:
        if table_name not in self.data["tables"]:
            return False
            
        if not path:
            if isinstance(self.data["tables"][table_name], list):
                self.data["tables"][table_name].append(data)
                self._commit()
                return True
            elif isinstance(self.data["tables"][table_name], dict):
                if isinstance(data, dict) and "id" in data:
                    self.data["tables"][table_name][data["id"]] = data
                else:
                    self.data["tables"][table_name][str(uuid4())] = data
                self._commit()
                return True
            return False
            
        path_parts = path.split('.')
        current = self.data["tables"][table_name]
        
        for part in path_parts[:-1]:
            if isinstance(current, dict):
                if part not in current:
                    return False
                current = current[part]
            elif isinstance(current, list):
                try:
                    index = int(part)
                    if index < len(current):
                        current = current[index]
                    else:
                        return False
                except ValueError:
                    return False
            else:
                return False
                
        final_part = path_parts[-1]
        if isinstance(current, dict):
            current[final_part] = data
            self._commit()
            return True
        elif isinstance(current, list):
            try:
                index = int(final_part)
                if index < len(current):
                    current[index] = data
                    self._commit()
                    return True
            except ValueError:
                pass
                
        return False

    def get(self, table_name: str, path: Optional[str] = None, default: Any = None) -> Any:
        if table_name not in self.data["tables"]:
            return default

        if not path:
            return deepcopy(self.data["tables"][table_name])

        try:
            path_parts = path.split('.')
            current = self.data["tables"][table_name]

            for part in path_parts:
                if isinstance(current, dict):
                    current = current.get(part, default)
                    if current is default:
                        return default
                elif isinstance(current, list):
                    try:
                        index = int(part)
                        current = current[index] if index < len(current) else default
                    except (ValueError, IndexError):
                        return default
                else:
                    return default

            return deepcopy(current)
        except Exception:
            return default

    def update(self, table_name: str, new_data: Any, path: Optional[str] = None) -> bool:
        if table_name not in self.data["tables"]:
            return False
            
        if not path:
            self.data["tables"][table_name] = new_data
            self._commit()
            return True
            
        path_parts = path.split('.')
        current = self.data["tables"][table_name]
        
        for part in path_parts[:-1]:
            if isinstance(current, dict):
                if part not in current:
                    return False
                current = current[part]
            elif isinstance(current, list):
                try:
                    index = int(part)
                    if index < len(current):
                        current = current[index]
                    else:
                        return False
                except ValueError:
                    return False
            else:
                return False
                
        final_part = path_parts[-1]
        if isinstance(current, dict):
            current[final_part] = new_data
            self._commit()
            return True
        elif isinstance(current, list):
            try:
                index = int(final_part)
                if index < len(current):
                    current[index] = new_data
                    self._commit()
                    return True
            except ValueError:
                pass
                
        return False

    def delete(self, table_name: str, path: Optional[str] = None) -> bool:
        if table_name not in self.data["tables"]:
            return False
            
        if not path:
            self.data["tables"][table_name] = [] if isinstance(self.data["tables"][table_name], list) else {}
            self._commit()
            return True
            
        path_parts = path.split('.')
        current = self.data["tables"][table_name]
        
        for part in path_parts[:-1]:
            if isinstance(current, dict):
                if part not in current:
                    return False
                current = current[part]
            elif isinstance(current, list):
                try:
                    index = int(part)
                    if index < len(current):
                        current = current[index]
                    else:
                        return False
                except ValueError:
                    return False
            else:
                return False
                
        final_part = path_parts[-1]
        if isinstance(current, dict):
            if final_part in current:
                del current[final_part]
                self._commit()
                return True
        elif isinstance(current, list):
            try:
                index = int(final_part)
                if index < len(current):
                    del current[index]
                    self._commit()
                    return True
            except ValueError:
                pass
                
        return False

    def create_index(self, table_name: str, field: str) -> bool:
        if table_name not in self.data["tables"]:
            return False
            
        index_name = f"{table_name}.{field}"
        if index_name in self.data["indexes"]:
            return True
            
        table_data = self.data["tables"][table_name]
        index = {}
        
        if isinstance(table_data, list):
            for i, item in enumerate(table_data):
                if isinstance(item, dict) and field in item:
                    value = item[field]
                    if value not in index:
                        index[value] = []
                    index[value].append(i)
        elif isinstance(table_data, dict):
            for key, item in table_data.items():
                if isinstance(item, dict) and field in item:
                    value = item[field]
                    if value not in index:
                        index[value] = []
                    index[value].append(key)
                    
        self.data["indexes"][index_name] = index
        self._commit()
        return True

    def query(self, table_name: str, conditions: Dict, use_index: bool = True, limit: Optional[int] = None, sort: Optional[str] = None, reverse: bool = False) -> List[Any]:
        if table_name not in self.data["tables"]:
            return []

        table_data = self.data["tables"][table_name]
        results = []

        if use_index and conditions:
            first_field = next(iter(conditions))
            if isinstance(conditions[first_field], dict):
                operator, value = next(iter(conditions[first_field].items()))
                if operator == "$gte":
                    index_name = f"{table_name}.{first_field}"
                    if index_name in self.data["indexes"]:
                        index = self.data["indexes"][index_name]
                        filtered_keys = [k for k in index.keys() if int(k) >= value]
                        keys_or_indices = []
                        for k in filtered_keys:
                            keys_or_indices.extend(index[k])

                        if isinstance(table_data, list):
                            for i in keys_or_indices:
                                if i < len(table_data):
                                    results.append(deepcopy(table_data[i]))
                        elif isinstance(table_data, dict):
                            for key in keys_or_indices:
                                if key in table_data:
                                    results.append(deepcopy(table_data[key]))
                        return results[:limit] if limit is not None else results
            else:
                index_name = f"{table_name}.{first_field}"
                if index_name in self.data["indexes"]:
                    index = self.data["indexes"][index_name]
                    first_value = conditions[first_field]

                    if first_value in index:
                        keys_or_indices = index[first_value]
                        remaining_conditions = {k: v for k, v in conditions.items() if k != first_field}

                        if isinstance(table_data, list):
                            for i in keys_or_indices:
                                if i < len(table_data):
                                    item = table_data[i]
                                    if all(item.get(k) == v for k, v in remaining_conditions.items()):
                                        results.append(deepcopy(item))
                        elif isinstance(table_data, dict):
                            for key in keys_or_indices:
                                if key in table_data:
                                    item = table_data[key]
                                    if all(item.get(k) == v for k, v in remaining_conditions.items()):
                                        results.append(deepcopy(item))
                        return results[:limit] if limit is not None else results

        if isinstance(table_data, list):
            for item in table_data:
                if isinstance(item, dict):
                    match = True
                    for field, condition in conditions.items():
                        if isinstance(condition, dict):
                            for op, value in condition.items():
                                if op == "$gte":
                                    if not (item.get(field, 0) >= value):
                                        match = False
                                        break
                        else:
                            if item.get(field) != condition:
                                match = False
                                break
                    if match:
                        results.append(deepcopy(item))
        elif isinstance(table_data, dict):
            for item in table_data.values():
                if isinstance(item, dict):
                    match = True
                    for field, condition in conditions.items():
                        if isinstance(condition, dict):
                            for op, value in condition.items():
                                if op == "$gte":
                                    if not (item.get(field, 0) >= value):
                                        match = False
                                        break
                        else:
                            if item.get(field) != condition:
                                match = False
                                break
                    if match:
                        results.append(deepcopy(item))

        # اعمال مرتب‌سازی اگر مشخص شده باشد
        if sort:
            reverse_sort = reverse if isinstance(reverse, bool) else False
            results.sort(key=lambda x: x.get(sort, 0), reverse=reverse_sort)

        # اعمال محدودیت تعداد نتایج
        if limit is not None:
            results = results[:limit]

        return results

    def backup(self, backup_name: str) -> bool:
        try:
            backup_path = f"{self.name}_{backup_name}.json"
            with open(backup_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def vacuum(self) -> bool:
        try:
            for index_name in list(self.data["indexes"].keys()):
                table_name, field = index_name.split('.')
                if table_name in self.data["tables"]:
                    self.create_index(table_name, field)
            for table_name, table_data in self.data["tables"].items():
                if isinstance(table_data, list):
                    self.data["tables"][table_name] = [x for x in table_data if x is not None]
                    
            self._commit()
            return True
        except Exception:
            return False

    def list_tables(self) -> List[str]:
        return list(self.data["tables"].keys())

    def table_info(self, table_name: str) -> Optional[Dict]:
        if table_name not in self.data["tables"]:
            return None
            
        table_data = self.data["tables"][table_name]
        info = {
            "type": "dict" if isinstance(table_data, dict) else "list",
            "size": len(table_data),
            "indexes": [idx.split('.')[1] for idx in self.data["indexes"] if idx.startswith(f"{table_name}.")]
        }
        
        if isinstance(table_data, list) and table_data and isinstance(table_data[0], dict):
            info["fields"] = list(table_data[0].keys())
        elif isinstance(table_data, dict) and table_data and isinstance(next(iter(table_data.values())), dict):
            info["fields"] = list(next(iter(table_data.values())).keys())
            
        return info

    def export_table(self, table_name: str, format: str = "json") -> Optional[str]:
        if table_name not in self.data["tables"]:
            return None
            
        table_data = self.data["tables"][table_name]
        
        if format == "json":
            return json.dumps(table_data, indent=4, ensure_ascii=False)
        elif format == "csv":
            if isinstance(table_data, list) and table_data and isinstance(table_data[0], dict):
                import csv
                from io import StringIO
                
                output = StringIO()
                writer = csv.DictWriter(output, fieldnames=table_data[0].keys())
                writer.writeheader()
                writer.writerows(table_data)
                return output.getvalue()
            elif isinstance(table_data, dict) and table_data and isinstance(next(iter(table_data.values())), dict):
                import csv
                from io import StringIO
                
                first_item = next(iter(table_data.values()))
                output = StringIO()
                writer = csv.DictWriter(output, fieldnames=first_item.keys())
                writer.writeheader()
                writer.writerows(table_data.values())
                return output.getvalue()
            else:
                return None
        else:
            return None