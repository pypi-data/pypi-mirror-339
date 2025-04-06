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
    def recursive_prune(obj: Any, expandable_fields: set[str], expand_map: dict[str, set[str]]) -> Any:
        if not isinstance(obj, dict):
            return obj

        result = {}
        for key, value in obj.items():
            #* Include non-expandable fields
            if key not in expandable_fields:
                result[key] = value
                continue

            #* Skip if not in expand_map (i.e. was not requested at all)
            if key not in expand_map:
                continue

            #* If there are children to expand, recursively prune them
            nested_expansion = expand_map[key]
            if isinstance(value, dict):
                if nested_expansion:
                    nested_expand_map = BaseSerializer.build_nested_expand_structure(nested_expansion)
                    result[key] = BaseSerializer.recursive_prune(value, expandable_fields, nested_expand_map)
                else:
                    #* Field is expanded with no children — show empty object
                    result[key] = {}
            else:
                #* Scalar fields — include directly
                result[key] = value

        return result