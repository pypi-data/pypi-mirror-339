"""
Ethical guidelines for recommendation systems.

This module provides utilities for implementing ethical guidelines
in recommendation systems, including content filtering and ethical scoring.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
from llama_recommender.utils.logging import get_logger


class EthicalGuidelines:
    """
    Implement ethical guidelines for recommendations.
    
    This class provides methods for evaluating recommendations against
    ethical guidelines and filtering out problematic content.
    """
    
    def __init__(
        self,
        guideline_config: Optional[Dict[str, Any]] = None,
        sensitive_attributes: Optional[List[str]] = None,
        content_categories: Optional[Dict[str, List[str]]] = None,
        minimum_ethical_score: float = 0.7,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize ethical guidelines.
        
        Args:
            guideline_config: Configuration for ethical guidelines
            sensitive_attributes: List of sensitive attributes to monitor
            content_categories: Dictionary mapping content categories to keywords
            minimum_ethical_score: Minimum ethical score for recommendations
            logger: Logger instance
        """
        self.guideline_config = guideline_config or {}
        self.sensitive_attributes = sensitive_attributes or []
        self.content_categories = content_categories or {}
        self.minimum_ethical_score = minimum_ethical_score
        self.logger = logger or get_logger(self.__class__.__name__)
        
        # Initialize default guidelines if not provided
        if not self.guideline_config:
            self._init_default_guidelines()
    
    def _init_default_guidelines(self) -> None:
        """
        Initialize default ethical guidelines.
        """
        self.guideline_config = {
            "banned_categories": [
                "illegal_content",
                "hate_speech",
                "harmful_content",
                "explicit_adult_content"
            ],
            "age_restricted_categories": [
                "violence",
                "gambling",
                "alcohol",
                "tobacco"
            ],
            "data_privacy": {
                "require_consent": True,
                "minimize_data_collection": True,
                "allow_opt_out": True
            },
            "transparency": {
                "explain_recommendations": True,
                "disclose_data_usage": True,
                "disclose_personalization": True
            },
            "fairness": {
                "ensure_equal_opportunity": True,
                "prevent_discriminatory_outcomes": True,
                "monitor_bias": True
            },
            "diversity": {
                "promote_diverse_content": True,
                "prevent_filter_bubbles": True,
                "include_minority_viewpoints": True
            }
        }
    
    def evaluate_item(
        self,
        item_id: str,
        item_metadata: Dict[str, Any],
        user_id: Optional[str] = None,
        user_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate an item against ethical guidelines.
        
        Args:
            item_id: Item identifier
            item_metadata: Item metadata
            user_id: User identifier (optional)
            user_metadata: User metadata (optional)
            
        Returns:
            Dictionary with evaluation results
        """
        # Initialize result
        result = {
            "item_id": item_id,
            "ethical_score": 1.0,
            "issues": [],
            "warnings": [],
            "allowed": True
        }
        
        # Check for banned categories
        banned_categories = self.guideline_config.get("banned_categories", [])
        item_categories = item_metadata.get("categories", [])
        
        banned_found = [cat for cat in item_categories if cat in banned_categories]
        if banned_found:
            result["ethical_score"] = 0.0
            result["allowed"] = False
            result["issues"].append({
                "type": "banned_category",
                "categories": banned_found,
                "severity": "high"
            })
        
        # Check for age-restricted content
        if user_metadata and "age" in user_metadata:
            age = user_metadata["age"]
            age_restricted = self.guideline_config.get("age_restricted_categories", [])
            
            restricted_found = [cat for cat in item_categories if cat in age_restricted]
            if restricted_found and age < 18:
                result["ethical_score"] = 0.0
                result["allowed"] = False
                result["issues"].append({
                    "type": "age_restricted_content",
                    "categories": restricted_found,
                    "user_age": age,
                    "severity": "high"
                })
        
        # Check for sensitive attributes
        sensitive_content = []
        for attr in self.sensitive_attributes:
            if attr in item_metadata.get("attributes", {}):
                sensitive_content.append(attr)
        
        if sensitive_content:
            # Reduce score but don't necessarily ban
            result["ethical_score"] *= 0.9
            result["warnings"].append({
                "type": "sensitive_attributes",
                "attributes": sensitive_content,
                "severity": "medium"
            })
        
        # Check for diversity concerns
        if "popularity" in item_metadata and item_metadata["popularity"] > 0.9:
            # Slightly reduce score for very popular items to encourage diversity
            result["ethical_score"] *= 0.95
            result["warnings"].append({
                "type": "popularity_bias",
                "popularity": item_metadata["popularity"],
                "severity": "low"
            })
        
        # Check if ethical score meets minimum threshold
        if result["ethical_score"] < self.minimum_ethical_score:
            result["allowed"] = False
        
        return result
    
    def filter_recommendations(
        self,
        items: List[Dict[str, Any]],
        user_id: Optional[str] = None,
        user_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Filter recommendations based on ethical guidelines.
        
        Args:
            items: List of item dictionaries
            user_id: User identifier (optional)
            user_metadata: User metadata (optional)
            
        Returns:
            List of filtered items with ethical scores
        """
        filtered_items = []
        
        for item in items:
            item_id = item.get("item_id")
            item_metadata = item.get("metadata", {})
            
            # Evaluate item
            evaluation = self.evaluate_item(
                item_id, 
                item_metadata,
                user_id, 
                user_metadata
            )
            
            # Add ethical evaluation to item
            item_with_ethics = item.copy()
            item_with_ethics["ethical_score"] = evaluation["ethical_score"]
            item_with_ethics["ethical_issues"] = evaluation["issues"]
            item_with_ethics["ethical_warnings"] = evaluation["warnings"]
            
            # Only include allowed items
            if evaluation["allowed"]:
                filtered_items.append(item_with_ethics)
            else:
                self.logger.info(f"Filtered out item {item_id} due to ethical concerns")
        
        return filtered_items
    
    def evaluate_recommendation_list(
        self,
        items: List[Dict[str, Any]],
        user_id: Optional[str] = None,
        user_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate an entire recommendation list against ethical guidelines.
        
        Args:
            items: List of item dictionaries
            user_id: User identifier (optional)
            user_metadata: User metadata (optional)
            
        Returns:
            Dictionary with evaluation results
        """
        # Evaluate each item
        item_evaluations = []
        for item in items:
            item_id = item.get("item_id")
            item_metadata = item.get("metadata", {})
            
            evaluation = self.evaluate_item(
                item_id, 
                item_metadata,
                user_id, 
                user_metadata
            )
            
            item_evaluations.append(evaluation)
        
        # Calculate aggregate metrics
        avg_ethical_score = np.mean([e["ethical_score"] for e in item_evaluations]) if item_evaluations else 0
        filtered_count = sum(1 for e in item_evaluations if not e["allowed"])
        
        # Check for diversity
        categories = []
        for item in items:
            item_categories = item.get("metadata", {}).get("categories", [])
            categories.extend(item_categories)
        
        unique_categories = len(set(categories))
        category_diversity = unique_categories / len(categories) if categories else 0
        
        # Check for filter bubble concerns
        popularities = [
            item.get("metadata", {}).get("popularity", 0.5) 
            for item in items
        ]
        avg_popularity = np.mean(popularities) if popularities else 0.5
        popularity_std = np.std(popularities) if popularities else 0
        
        filter_bubble_risk = "low"
        if avg_popularity > 0.8 and popularity_std < 0.1:
            filter_bubble_risk = "high"
        elif avg_popularity > 0.7 and popularity_std < 0.2:
            filter_bubble_risk = "medium"
        
        return {
            "avg_ethical_score": float(avg_ethical_score),
            "filtered_count": filtered_count,
            "original_count": len(items),
            "remaining_count": len(items) - filtered_count,
            "category_diversity": float(category_diversity),
            "filter_bubble_risk": filter_bubble_risk,
            "avg_popularity": float(avg_popularity),
            "item_evaluations": item_evaluations
        }
    
    def get_ethical_explanation(
        self,
        evaluation: Dict[str, Any]
    ) -> str:
        """
        Generate a human-readable explanation of ethical evaluation.
        
        Args:
            evaluation: Ethical evaluation results
            
        Returns:
            Human-readable explanation
        """
        if not evaluation.get("allowed", True):
            # Item was filtered out
            issues = evaluation.get("issues", [])
            if issues:
                issue_types = [issue["type"] for issue in issues]
                
                if "banned_category" in issue_types:
                    categories = next(
                        issue["categories"] 
                        for issue in issues 
                        if issue["type"] == "banned_category"
                    )
                    return f"This item was filtered out because it contains banned content categories: {', '.join(categories)}."
                
                elif "age_restricted_content" in issue_types:
                    categories = next(
                        issue["categories"] 
                        for issue in issues 
                        if issue["type"] == "age_restricted_content"
                    )
                    return f"This item was filtered out because it contains age-restricted content: {', '.join(categories)}."
                
                else:
                    return "This item was filtered out because it doesn't meet our ethical guidelines."
            
            # No specific issues found
            return "This item was filtered out due to ethical concerns."
        
        # Item is allowed but may have warnings
        warnings = evaluation.get("warnings", [])
        if warnings:
            warning_texts = []
            
            for warning in warnings:
                if warning["type"] == "sensitive_attributes":
                    attributes = warning["attributes"]
                    warning_texts.append(
                        f"This item contains potentially sensitive content related to: {', '.join(attributes)}."
                    )
                
                elif warning["type"] == "popularity_bias":
                    warning_texts.append(
                        "This is a very popular item that many users interact with."
                    )
            
            if warning_texts:
                return " ".join(warning_texts)
        
        # No issues or warnings
        return "This item meets our ethical guidelines."
    
    def add_custom_guideline(
        self,
        guideline_name: str,
        guideline_config: Dict[str, Any]
    ) -> None:
        """
        Add a custom ethical guideline.
        
        Args:
            guideline_name: Name of the guideline
            guideline_config: Configuration for the guideline
        """
        self.guideline_config[guideline_name] = guideline_config
        self.logger.info(f"Added custom guideline: {guideline_name}")
    
    def add_sensitive_attribute(
        self,
        attribute_name: str
    ) -> None:
        """
        Add a sensitive attribute to monitor.
        
        Args:
            attribute_name: Name of the sensitive attribute
        """
        if attribute_name not in self.sensitive_attributes:
            self.sensitive_attributes.append(attribute_name)
            self.logger.info(f"Added sensitive attribute: {attribute_name}")
    
    def add_content_category(
        self,
        category_name: str,
        keywords: List[str],
        is_banned: bool = False,
        is_age_restricted: bool = False
    ) -> None:
        """
        Add a content category to monitor.
        
        Args:
            category_name: Name of the content category
            keywords: List of keywords associated with the category
            is_banned: Whether the category is banned
            is_age_restricted: Whether the category is age-restricted
        """
        self.content_categories[category_name] = keywords
        
        if is_banned and category_name not in self.guideline_config.get("banned_categories", []):
            if "banned_categories" not in self.guideline_config:
                self.guideline_config["banned_categories"] = []
            self.guideline_config["banned_categories"].append(category_name)
        
        if is_age_restricted and category_name not in self.guideline_config.get("age_restricted_categories", []):
            if "age_restricted_categories" not in self.guideline_config:
                self.guideline_config["age_restricted_categories"] = []
            self.guideline_config["age_restricted_categories"].append(category_name)
        
        self.logger.info(f"Added content category: {category_name}")


class ContentSafetyChecker:
    """
    Check content for safety concerns.
    
    This class provides methods for checking content against safety
    guidelines and detecting problematic content.
    """
    
    def __init__(
        self,
        safety_thresholds: Optional[Dict[str, float]] = None,
        custom_detection_rules: Optional[Dict[str, Callable]] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize content safety checker.
        
        Args:
            safety_thresholds: Dictionary mapping safety categories to thresholds
            custom_detection_rules: Dictionary mapping rule names to detection functions
            logger: Logger instance
        """
        self.safety_thresholds = safety_thresholds or {
            "hate_speech": 0.7,
            "violence": 0.8,
            "sexual_content": 0.8,
            "harassment": 0.7,
            "self_harm": 0.6,
            "misinformation": 0.7
        }
        
        self.custom_detection_rules = custom_detection_rules or {}
        self.logger = logger or get_logger(self.__class__.__name__)
    
    def check_text(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Check text content for safety concerns.
        
        Args:
            text: Text content to check
            
        Returns:
            Dictionary with safety check results
        """
        # Initialize result
        result = {
            "is_safe": True,
            "safety_scores": {},
            "content_issues": [],
            "overall_safety_score": 1.0
        }
        
        # Apply simple keyword-based detection
        # (In a real implementation, this would use a more sophisticated model)
        safety_categories = {
            "hate_speech": [
                "hate", "slur", "racist", "bigot", "nazi", "supremacist"
            ],
            "violence": [
                "kill", "murder", "attack", "destroy", "violent", "weapon"
            ],
            "sexual_content": [
                "explicit", "pornography", "sexual", "nude", "xxx"
            ],
            "harassment": [
                "harass", "bully", "threaten", "stalk", "intimidate"
            ],
            "self_harm": [
                "suicide", "self-harm", "cutting", "depression"
            ],
            "misinformation": [
                "fake news", "conspiracy", "hoax", "disinformation"
            ]
        }
        
        # Check each category
        text_lower = text.lower()
        category_scores = {}
        
        for category, keywords in safety_categories.items():
            # Count keyword matches
            matches = sum(keyword in text_lower for keyword in keywords)
            
            # Calculate safety score (inverse of match ratio)
            if matches > 0:
                # Higher score means more concerning
                score = min(1.0, matches / 10)
            else:
                score = 0.0
            
            category_scores[category] = score
            result["safety_scores"][category] = score
            
            # Check if score exceeds threshold
            threshold = self.safety_thresholds.get(category, 0.7)
            if score >= threshold:
                result["is_safe"] = False
                result["content_issues"].append({