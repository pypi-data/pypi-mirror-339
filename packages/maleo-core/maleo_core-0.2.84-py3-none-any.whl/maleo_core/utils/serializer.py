from collections import defaultdict
from typing import Any

class BaseSerializer:
    @staticmethod
    def build_nested_expand_structure(expand: set[str]) -> dict[str, set[str]]:
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
                nested[item] = set()  # Empty set means expand field without children
        return dict(nested)

    @staticmethod
    def recursive_prune(obj: Any, expand_map: dict[str, set[str]]) -> Any:
        """
        Prune object based on expand map rules:
        - If a field is not in expand_map, don't include it
        - If a field is in expand_map with empty set, include it without children
        - If a field is in expand_map with non-empty set, include it with only specified children
        """
        if not isinstance(obj, dict):
            return obj

        result = {}
        for key, value in obj.items():
            # Skip if not in expand_map (not requested)
            if key not in expand_map:
                continue

            # Get nested expansion for this key
            nested_expansion = expand_map[key]
            
            if isinstance(value, dict) and nested_expansion:
                # Parent with specified children - only include those children
                nested_expand_map = BaseSerializer.build_nested_expand_structure(nested_expansion)
                result[key] = BaseSerializer.recursive_prune(value, nested_expand_map)
            else:
                # Either a scalar field or parent expanded without children
                result[key] = {} if isinstance(value, dict) and not nested_expansion else value

        return result