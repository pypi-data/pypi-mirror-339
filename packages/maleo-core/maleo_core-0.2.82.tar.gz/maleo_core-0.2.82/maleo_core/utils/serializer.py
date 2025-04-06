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
        return dict(nested)

    @staticmethod
    def recursive_prune(obj:Any, expandable_fields:set[str], expand_map:dict[str, set[str]]) -> Any:
        if not isinstance(obj, dict):
            return obj

        result = {}
        for key, value in obj.items():
            #* If field is not expandable, always include it
            if key not in expandable_fields:
                result[key] = value
                continue

            #* Fully expanded (e.g. "profile" in expand means include everything in profile)
            if key in expand_map and not expand_map[key]:
                result[key] = value
                continue

            #* Partially expanded (e.g. "profile.gender" in expand but not "profile.blood_type")
            if key in expand_map:
                nested_expansion = expand_map[key]
                nested_expand_map = BaseSerializer.build_nested_expand_structure(nested_expansion)
                if isinstance(value, dict):
                    result[key] = BaseSerializer.recursive_prune(value, expandable_fields, nested_expand_map)
                else:
                    result[key] = value
                continue

            #* Not in expand — skip
            #* (i.e. field is expandable but was not requested nor has children explicitly requested)
        return result