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
                nested[item] = set()  # Empty set means expand field without children
        return dict(nested)

    @staticmethod
    def recursive_prune(obj: Any, expand_map: dict[str, set[str]], expandable_fields: set[str] = None) -> Any:
        """
        Prune object based on expand map rules:
        - Regular fields (not in expandable_fields) are always included
        - Expandable fields not in expand_map are excluded
        - Expandable fields in expand_map:
        - If no children specified, include the field but exclude ALL expandable children
        - If children specified, include only those specific children
        """
        if not isinstance(obj, dict):
            return obj
        
        # If expandable_fields is not provided, treat all fields in expand_map as expandable
        if expandable_fields is None:
            expandable_fields = set(expand_map.keys())
        
        result = {}
        for key, value in obj.items():
            # If it's not an expandable field, include it directly
            if key not in expandable_fields:
                result[key] = value
                continue
                
            # Skip expandable fields not requested
            if key not in expand_map:
                continue
            
            # Get nested expansion for this key
            nested_expansion = expand_map[key]
            
            if isinstance(value, dict):
                if nested_expansion:
                    # Has children specified - include only those children
                    nested_expand_map = BaseSerializer.build_nested_expand_structure(nested_expansion)
                    result[key] = BaseSerializer.recursive_prune(
                        value, 
                        nested_expand_map,
                        expandable_fields={f.split(".", 1)[0] for f in expandable_fields if "." in f and f.startswith(f"{key}.")}
                    )
                else:
                    # No children specified - include only non-expandable fields
                    filtered_value = {}
                    child_expandable_fields = {f.split(".", 1)[0] for f in expandable_fields if "." in f and f.startswith(f"{key}.")}
                    
                    for child_key, child_value in value.items():
                        if child_key not in child_expandable_fields:
                            filtered_value[child_key] = child_value
                    
                    result[key] = filtered_value
            else:
                # Scalar field - include directly
                result[key] = value
                
        return result