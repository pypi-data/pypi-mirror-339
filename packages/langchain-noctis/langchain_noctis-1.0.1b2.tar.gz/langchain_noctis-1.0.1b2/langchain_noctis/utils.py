"""Utility functions for the Noctis retriever."""

from typing import Any, Dict, List

from noctis_sdk.models.response import Response


class RelationshipExtractor:
    """Utility class to extract and clean relationship data from Noctis API responses.
    
    This class provides static methods to extract related entities and their attributes
    from Noctis relationship objects, handling different data formats and cleaning up
    entity names.
    """
    
    @staticmethod
    def extract_relationships(
        response: Response, 
        relationship_type: str
    ) -> List[Dict[str, Any]]:
        """Extract relationships of a specific type from API response.
        
        Args:
            response: The API response containing relationships
            relationship_type: The type of relationship to extract
            
        Returns:
            List of extracted relationships
        """
        results = []
        
        if not response or not response.relationships:
            return results
        
        for relation in response.relationships:
            if hasattr(relation, 'middle') and relation.middle == relationship_type:
                left = relation.left if hasattr(relation, 'left') else {}
                right = relation.right if hasattr(relation, 'right') else {}
                
                for left_key, left_value in left.items():
                    for right_key, right_value in right.items():
                        # Clean up names if they have unwanted characters
                        right_clean = RelationshipExtractor.clean_name(right_key)
                        
                        results.append({
                            "primary_domain": left_key,
                            "related_entity": right_clean,
                            "primary_info": left_value,
                            "related_info": right_value,
                            "relationship_type": relation.middle
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