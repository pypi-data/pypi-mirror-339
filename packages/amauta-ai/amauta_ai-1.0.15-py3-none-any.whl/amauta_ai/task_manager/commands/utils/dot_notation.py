"""
Dot Notation Parser for Task References

This module provides functionality to parse and resolve dot notation references to tasks.
For example, 'EPIC1.TASK2.STORY3' can be resolved to the actual task ID in the system.
"""

from typing import Dict, List, Optional, Tuple, Set, Union
import re
from functools import lru_cache

from amauta_ai.task_manager.models import TaskItem, ItemType
from amauta_ai.task_manager.service import TaskManagerService


class DotNotationError(Exception):
    """Base exception for dot notation parsing errors."""
    pass


class AmbiguousReferenceError(DotNotationError):
    """Exception raised when a reference is ambiguous (multiple matches)."""
    
    def __init__(self, reference: str, matches: List[str], suggestions: Optional[List[str]] = None):
        self.reference = reference
        self.matches = matches
        self.suggestions = suggestions or []
        message = f"Ambiguous reference '{reference}'. Multiple matches found: {', '.join(matches)}"
        if suggestions:
            message += f"\nTry using a more specific reference like: {', '.join(suggestions)}"
        super().__init__(message)


class ReferenceNotFoundError(DotNotationError):
    """Exception raised when a reference cannot be found."""
    
    def __init__(self, reference: str, context: Optional[str] = None, similar_matches: Optional[List[str]] = None):
        self.reference = reference
        self.context = context
        self.similar_matches = similar_matches or []
        message = f"Reference '{reference}' not found"
        if context:
            message += f" in context of '{context}'"
        if similar_matches:
            message += f"\nDid you mean one of: {', '.join(similar_matches)}?"
        super().__init__(message)


class InvalidReferenceFormatError(DotNotationError):
    """Exception raised when a reference format is invalid."""
    
    def __init__(self, reference: str, detail: str):
        self.reference = reference
        self.detail = detail
        message = f"Invalid reference format '{reference}': {detail}"
        super().__init__(message)


class DotNotationParser:
    """
    Parser for dot notation references to tasks.
    
    Allows addressing tasks using a hierarchical dot notation like:
    - "EPIC1" - References an epic by its ID prefix/name
    - "EPIC1.TASK2" - References a task that is a child of EPIC1
    - "EPIC1.TASK2.STORY3" - References a story that is a child of TASK2
    
    The parser handles both exact ID matches and partial/abbreviated references.
    """
    
    def __init__(self, task_manager: TaskManagerService):
        """
        Initialize the dot notation parser.
        
        Args:
            task_manager: The task manager service to use for resolving references
        """
        self.task_manager = task_manager
        # Regular expression for validating and splitting dot notation
        self.dot_pattern = re.compile(r'^([^.]+)(?:\.([^.]+))*$')
        # Regex to extract the prefix part (E-, T-, S-, I-) and numeric part
        self.id_pattern = re.compile(r'^([A-Z]-\d+)-([A-Z0-9]+)$')
    
    def parse(self, reference: str) -> str:
        """
        Parse a dot notation reference and return the corresponding task ID.
        
        Args:
            reference: The dot notation reference (e.g., "EPIC1.TASK2.STORY3")
            
        Returns:
            The resolved task ID
            
        Raises:
            InvalidReferenceFormatError: If the reference format is invalid
            ReferenceNotFoundError: If the reference cannot be found
            AmbiguousReferenceError: If the reference is ambiguous (multiple matches)
        """
        # Validate the overall dot notation format
        if not self.dot_pattern.match(reference):
            raise InvalidReferenceFormatError(
                reference, 
                "Reference must be in the format 'ITEM1' or 'ITEM1.ITEM2.ITEM3'"
            )
        
        # Split the reference into segments
        segments = reference.split('.')
        
        # Start with no parent context
        parent_id = None
        current_id = None
        
        # Process each segment in the chain
        for i, segment in enumerate(segments):
            # Find matching items for this segment, filtered by parent if applicable
            matches = self._find_matches(segment, parent_id)
            
            if not matches:
                context = f"{segments[i-1]}" if i > 0 else None
                # Try to find similar matches for better error messages
                similar_matches = self._find_similar_matches(segment, parent_id)
                raise ReferenceNotFoundError(segment, context, similar_matches)
            
            if len(matches) > 1:
                # Handle ambiguity - return details to help user and suggest alternatives
                match_ids = [item.id for item in matches]
                # Provide more specific suggestions to disambiguate
                suggestions = self._generate_disambiguation_suggestions(matches, segment)
                raise AmbiguousReferenceError(segment, match_ids, suggestions)
            
            # We have exactly one match
            current_id = matches[0].id
            parent_id = current_id  # For the next iteration
        
        return current_id
    
    def _find_matches(self, segment: str, parent_id: Optional[str] = None) -> List[TaskItem]:
        """
        Find items matching a segment, optionally filtered by parent.
        
        Args:
            segment: The segment to match (e.g., "EPIC1", "TASK2")
            parent_id: Optional parent ID to filter children
            
        Returns:
            List of matching TaskItems
        """
        all_items = self.task_manager.get_all_items()
        matches = []
        
        # Check if segment is a full ID
        exact_match = next((item for item in all_items if item.id == segment), None)
        if exact_match:
            if parent_id is None or exact_match.parent == parent_id:
                return [exact_match]
        
        # Case 1: Check for item type prefix (E-, T-, S-, I-)
        for item in all_items:
            # If parent_id is specified, filter by parent
            if parent_id is not None and item.parent != parent_id:
                continue
                
            # Match by ID prefix and abbreviated ID
            if self._matches_abbreviated_id(item.id, segment):
                matches.append(item)
                continue
                
            # Match by item type and simple name or number
            type_prefix = self._get_type_prefix(item.type)
            if segment.upper().startswith(type_prefix):
                # Extract numeric part to compare
                matches.append(item)
        
        return matches
    
    def _matches_abbreviated_id(self, full_id: str, abbreviated: str) -> bool:
        """
        Check if an abbreviated ID matches a full ID.
        
        Args:
            full_id: The full task ID (e.g., "E-1743775035-YINR")
            abbreviated: The abbreviated reference (e.g., "E-YINR" or "YINR")
            
        Returns:
            True if the abbreviated reference matches the full ID
        """
        # Direct match
        if full_id == abbreviated:
            return True
            
        # Match by suffix part
        match = self.id_pattern.match(full_id)
        if match and match.group(2) == abbreviated:
            return True
            
        # Match by prefix + suffix
        prefix_match = match and f"{match.group(1)[:1]}-{match.group(2)}" == abbreviated
        return prefix_match
    
    @staticmethod
    def _get_type_prefix(item_type: ItemType) -> str:
        """
        Get the prefix for a given item type.
        
        Args:
            item_type: The item type
            
        Returns:
            The prefix (E- for Epic, T- for Task, etc.)
        """
        prefix_map = {
            ItemType.EPIC: "E-",
            ItemType.TASK: "T-",
            ItemType.STORY: "S-",
            ItemType.ISSUE: "I-",
        }
        return prefix_map.get(item_type, "")
    
    def resolve_many(self, references: List[str]) -> Dict[str, str]:
        """
        Resolve multiple dot notation references at once.
        
        Args:
            references: List of dot notation references
            
        Returns:
            Dictionary mapping references to resolved IDs
            
        Raises:
            Various DotNotationError subtypes for parsing errors
        """
        result = {}
        for ref in references:
            try:
                result[ref] = self.parse(ref)
            except DotNotationError as e:
                # Re-raise the exception
                raise
        return result
    
    @lru_cache(maxsize=128)
    def suggest_completions(self, partial_reference: str) -> List[str]:
        """
        Suggest possible completions for a partial dot notation reference.
        
        Args:
            partial_reference: The partial reference (e.g., "EPIC1." or "EPIC1.T")
            
        Returns:
            List of possible completions
        """
        # Handle empty input
        if not partial_reference:
            return self._get_top_level_suggestions()
            
        # Check if we're looking for completions of a parent reference
        if partial_reference.endswith('.'):
            # Extract the parent reference and find its children
            parent_ref = partial_reference[:-1]
            try:
                parent_id = self.parse(parent_ref)
                return self._get_child_suggestions(parent_id)
            except DotNotationError:
                return []
                
        # We're in the middle of typing a segment
        segments = partial_reference.split('.')
        current_segment = segments[-1]
        
        # If we only have one segment, suggest from all items
        if len(segments) == 1:
            return self._get_suggestions_matching_prefix(current_segment)
            
        # We're completing a child segment
        parent_ref = '.'.join(segments[:-1])
        try:
            parent_id = self.parse(parent_ref)
            return self._get_child_suggestions_matching_prefix(parent_id, current_segment)
        except DotNotationError:
            return []
    
    def _get_top_level_suggestions(self) -> List[str]:
        """Get suggestions for top-level items (mainly Epics)."""
        all_items = self.task_manager.get_all_items()
        # Primarily suggest Epics, but allow any item without a parent
        return [item.id for item in all_items if item.parent is None]
    
    def _get_child_suggestions(self, parent_id: str) -> List[str]:
        """Get suggestions for children of a specific parent."""
        parent_item = self.task_manager.get_item_by_id(parent_id)
        if not parent_item:
            return []
            
        children = []
        for child_id in parent_item.children:
            child = self.task_manager.get_item_by_id(child_id)
            if child:
                children.append(child.id)
                
        return children
    
    def _get_suggestions_matching_prefix(self, prefix: str) -> List[str]:
        """Get all items whose ID or abbreviated form starts with the given prefix."""
        all_items = self.task_manager.get_all_items()
        matches = []
        
        for item in all_items:
            # Match by ID start
            if item.id.startswith(prefix):
                matches.append(item.id)
                continue
                
            # Match by abbreviated forms
            match = self.id_pattern.match(item.id)
            if match:
                # Match by suffix
                suffix = match.group(2)
                if suffix.startswith(prefix):
                    matches.append(item.id)
                    continue
                
                # Match by type + suffix
                type_prefix = item.id[0]
                if f"{type_prefix}-{suffix}".startswith(prefix):
                    matches.append(item.id)
                    
        return matches
    
    def _get_child_suggestions_matching_prefix(self, parent_id: str, prefix: str) -> List[str]:
        """Get children of a specific parent whose ID starts with the given prefix."""
        parent_item = self.task_manager.get_item_by_id(parent_id)
        if not parent_item:
            return []
            
        matches = []
        for child_id in parent_item.children:
            child = self.task_manager.get_item_by_id(child_id)
            if not child:
                continue
                
            # Apply the same matching logic as in _get_suggestions_matching_prefix
            if child.id.startswith(prefix):
                matches.append(child.id)
                continue
                
            match = self.id_pattern.match(child.id)
            if match:
                suffix = match.group(2)
                if suffix.startswith(prefix):
                    matches.append(child.id)
                    continue
                
                type_prefix = child.id[0]
                if f"{type_prefix}-{suffix}".startswith(prefix):
                    matches.append(child.id)
                    
        return matches
    
    def _find_similar_matches(self, segment: str, parent_id: Optional[str] = None, max_suggestions: int = 3) -> List[str]:
        """
        Find items with names similar to the given segment for better error messages.
        
        Args:
            segment: The segment that didn't match
            parent_id: Optional parent ID to filter children
            max_suggestions: Maximum number of suggestions to return
            
        Returns:
            List of similar item IDs
        """
        all_items = self.task_manager.get_all_items()
        candidates = []
        
        # Filter by parent if specified
        if parent_id is not None:
            all_items = [item for item in all_items if item.parent == parent_id]
            
        # Get segment parts (prefix, ID part)
        seg_parts = segment.split('-')
        seg_prefix = seg_parts[0] if len(seg_parts) > 1 else None
        
        # Score items by similarity
        for item in all_items:
            # Skip exact matches (which would've been found already)
            if item.id == segment:
                continue
                
            score = 0
            
            # Check ID part similarity
            item_parts = item.id.split('-')
            
            # If prefixes match exactly
            if seg_prefix and len(item_parts) > 0 and item_parts[0] == seg_prefix:
                score += 3
                
            # Check if type matches
            type_prefix = self._get_type_prefix(item.type)
            if segment.upper().startswith(type_prefix):
                score += 2
                
            # Check if suffix part matches partially
            if len(item_parts) > 2 and len(seg_parts) > 1:
                if item_parts[2].startswith(seg_parts[1]):
                    score += 2
                    
            # If it has a reasonable similarity score, include it
            if score >= 2:
                candidates.append((score, item.id))
                
        # Sort by score descending and return top matches
        candidates.sort(reverse=True)
        return [id for _, id in candidates[:max_suggestions]]
    
    def _generate_disambiguation_suggestions(self, matches: List[TaskItem], original_segment: str) -> List[str]:
        """
        Generate suggestions to help disambiguate multiple matches.
        
        Args:
            matches: The list of matching items
            original_segment: The original segment that caused ambiguity
            
        Returns:
            List of suggested more specific references
        """
        suggestions = []
        
        # Group by item type
        by_type = {}
        for item in matches:
            if item.type not in by_type:
                by_type[item.type] = []
            by_type[item.type].append(item)
            
        # If we have items of different types, suggest using type prefix
        if len(by_type) > 1:
            for item_type, items in by_type.items():
                type_prefix = self._get_type_prefix(item_type)
                suffix = original_segment.split('-')[-1] if '-' in original_segment else original_segment
                suggestions.append(f"{type_prefix}{suffix}")
                
        # For items of the same type, suggest using full ID or ID suffix
        for item in matches[:3]:  # Limit to first 3 to avoid too many suggestions
            # Extract the suffix portion (last part after hyphen)
            match = self.id_pattern.match(item.id)
            if match:
                suffix = match.group(2)
                if not any(s.endswith(suffix) for s in suggestions):
                    suggestions.append(suffix)
                    
        return suggestions[:5]  # Limit to 5 suggestions maximum 