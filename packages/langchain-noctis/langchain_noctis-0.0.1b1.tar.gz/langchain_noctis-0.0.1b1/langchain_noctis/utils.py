"""Utility functions for the Noctis retriever."""

from typing import Any, Dict, List


class RelationshipExtractor:
    """Utility class to extract and clean relationship data from Noctis API responses.
    
    This class provides methods to parse relationship data from the API.
    """
    
    @staticmethod
    def extract_relationships(
        data: Dict[str, Any], relationship_type: str
    ) -> List[Dict[str, Any]]:
        """Extract relationships of a specific type from API response.
        
        Args:
            data: The API response data containing relationships
            relationship_type: The type of relationship to extract
            
        Returns:
            List of extracted relationships
        """
        results = []
        
        if not isinstance(data, dict) or not data or "relationships" not in data:
            return results
            
        if not data["relationships"]:
            return results
        
        for relation in data.get("relationships", []):
            if relation.get("middle") == relationship_type:
                left = relation.get("left", {})
                right = relation.get("right", {})
                
                for left_key, left_value in left.items():
                    for right_key, right_value in right.items():
                        # Clean up names if they have unwanted characters
                        right_clean = RelationshipExtractor.clean_name(right_key)
                        
                        results.append({
                            "primary_domain": left_key,
                            "related_entity": right_clean,
                            "primary_info": left_value,
                            "related_info": right_value,
                            "relationship_type": relation.get("middle")
                        })
        
        return results
    
    @staticmethod
    def clean_name(name: str) -> str:
        """Clean up entity names by removing trailing braces and brackets.
        
        Args:
            name: The name to clean
            
        Returns:
            Cleaned name
        """
        # Remove trailing braces and brackets
        if "}" in name:
            name = name.split("}")[0]
        if "}}}]" in name:
            name = name.split("}}}]")[0]
        return name 