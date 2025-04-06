from collections import defaultdict
from typing import Any

class BaseSerializer:
    @staticmethod
    def build_nested_expand_structure(expand:set[str]) -> dict[str, set[str]]:
        """
        Turn set like {'profile.gender', 'user_type'} into:
        {
            'profile': {'gender'},
            'user_type': set()
        }
        """
        nested = defaultdict(set)
        for item in expand:
            if "." in item:
                parent, child = item.split(".", 1)
                nested[parent].add(child)
            else:
                nested[item]  #* empty set means expand whole field
        return nested

    def recursive_prune(obj:Any, expandable_fields:set[str], expand_map:dict[str, set[str]], current_field:str = "") -> Any:
        if not isinstance(obj, dict):
            return obj

        result = {}
        for key, value in obj.items():
            full_key = f"{current_field}.{key}" if current_field else key

            #* If field is not expandable, include it
            if full_key not in expandable_fields:
                result[key] = value
                continue

            #* Fully expanded field
            if full_key in expand_map and not expand_map[full_key]:
                result[key] = value
                continue

            #* Parent field needed for nested expansion
            if key in expand_map or full_key in expand_map:
                nested_expansion = expand_map.get(full_key, set())
                if isinstance(value, dict):
                    result[key] = BaseSerializer.recursive_prune(value, expandable_fields, BaseSerializer.build_nested_expand_structure(nested_expansion), full_key)
                else:
                    result[key] = value  #* Non-dict field — include as-is
                continue

            #* Not in expand — skip
        return result