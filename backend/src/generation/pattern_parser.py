"""
Pattern Parser - Extract component structure from pattern JSON.

This module parses shadcn/ui pattern JSON files to extract component metadata,
props, variants, and modification points for code generation.
"""

import json
import os
import re
from typing import Dict, List, Any, Optional
from pathlib import Path

from .types import PatternStructure


class PatternParser:
    """
    Parser for extracting component structure from pattern JSON.
    
    Uses regex-based parsing for MVP (full AST parsing deferred to post-MVP).
    """
    
    def __init__(self, patterns_dir: Optional[Path] = None):
        """
        Initialize pattern parser.
        
        Args:
            patterns_dir: Directory containing pattern JSON files.
                         Defaults to PATTERNS_DIR env var or backend/data/patterns/
        """
        if patterns_dir is None:
            # Check environment variable first
            env_patterns_dir = os.getenv("PATTERNS_DIR")
            if env_patterns_dir:
                patterns_dir = Path(env_patterns_dir)
            else:
                # Default to backend/data/patterns
                backend_dir = Path(__file__).parent.parent.parent
                patterns_dir = backend_dir / "data" / "patterns"
        
        self.patterns_dir = Path(patterns_dir)
    
    def load_pattern(self, pattern_id: str) -> Dict[str, Any]:
        """
        Load pattern JSON from file.
        
        Args:
            pattern_id: ID of the pattern (e.g., "shadcn-button")
        
        Returns:
            Pattern data as dictionary
        
        Raises:
            FileNotFoundError: If pattern file doesn't exist
            ValueError: If pattern JSON is invalid
        """
        # Map pattern ID to filename
        # E.g., "shadcn-button" -> "button.json"
        pattern_name = pattern_id.replace("shadcn-", "").lower()
        pattern_file = self.patterns_dir / f"{pattern_name}.json"
        
        if not pattern_file.exists():
            raise FileNotFoundError(f"Pattern file not found: {pattern_file}")
        
        try:
            with open(pattern_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid pattern JSON in {pattern_file}: {e}")
    
    def parse(self, pattern_id: str) -> PatternStructure:
        """
        Parse pattern and extract component structure.
        
        Args:
            pattern_id: ID of the pattern to parse
        
        Returns:
            PatternStructure with extracted metadata
        """
        pattern_data = self.load_pattern(pattern_id)
        
        # Extract basic metadata
        component_name = pattern_data.get("name", "Component")
        code = pattern_data.get("code", "")
        metadata = pattern_data.get("metadata", {})
        
        # Extract component structure
        props_interface = self._extract_props_interface(code)
        imports = self._extract_imports(code)
        variants = self._extract_variants(metadata)
        modification_points = self._find_modification_points(code, metadata)
        
        return PatternStructure(
            component_name=component_name,
            props_interface=props_interface,
            imports=imports,
            variants=variants,
            modification_points=modification_points,
            code=code,
            metadata=metadata
        )
    
    def _extract_props_interface(self, code: str) -> str:
        """
        Extract TypeScript props interface from code.
        
        Args:
            code: Component source code
        
        Returns:
            Props interface definition
        """
        # Match interface definitions like: interface ButtonProps extends...
        interface_pattern = r'(export\s+)?interface\s+\w+Props[^{]*\{[^}]*\}'
        match = re.search(interface_pattern, code, re.DOTALL)
        
        if match:
            return match.group(0)
        
        return ""
    
    def _extract_imports(self, code: str) -> List[str]:
        """
        Extract all import statements from code.
        
        Args:
            code: Component source code
        
        Returns:
            List of import statements
        """
        # Match import statements
        import_pattern = r'^import\s+.*?from\s+["\'].*?["\'];?$'
        imports = re.findall(import_pattern, code, re.MULTILINE)
        
        return imports
    
    def _extract_variants(self, metadata: Dict[str, Any]) -> List[str]:
        """
        Extract variant names from pattern metadata.
        
        Args:
            metadata: Pattern metadata dictionary
        
        Returns:
            List of variant names
        """
        variants = []
        
        # Extract from metadata.variants
        if "variants" in metadata:
            for variant in metadata["variants"]:
                if isinstance(variant, dict):
                    variants.append(variant.get("name", ""))
                elif isinstance(variant, str):
                    variants.append(variant)
        
        return [v for v in variants if v]  # Filter empty strings
    
    def _find_modification_points(
        self, code: str, metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Identify points in code where modifications can be made.
        
        Args:
            code: Component source code
            metadata: Pattern metadata
        
        Returns:
            Dictionary of modification points and their locations
        """
        modification_points = {
            "className_locations": [],
            "variant_definitions": [],
            "prop_locations": [],
            "style_locations": []
        }
        
        # Find className attributes
        className_pattern = r'className=\{[^}]+\}'
        modification_points["className_locations"] = [
            match.start() for match in re.finditer(className_pattern, code)
        ]
        
        # Find variant definitions (e.g., in cva() calls)
        variant_pattern = r'variants:\s*\{[^}]+\}'
        match = re.search(variant_pattern, code, re.DOTALL)
        if match:
            modification_points["variant_definitions"].append({
                "start": match.start(),
                "end": match.end(),
                "content": match.group(0)
            })
        
        # Find prop destructuring locations
        prop_pattern = r'\(\s*\{[^}]+\}\s*,?\s*ref\)'
        match = re.search(prop_pattern, code)
        if match:
            modification_points["prop_locations"].append({
                "start": match.start(),
                "end": match.end(),
                "content": match.group(0)
            })
        
        return modification_points
    
    def list_available_patterns(self) -> List[str]:
        """
        List all available pattern IDs.
        
        Returns:
            List of pattern IDs (e.g., ["shadcn-button", "shadcn-card"])
        """
        if not self.patterns_dir.exists():
            return []
        
        patterns = []
        for pattern_file in self.patterns_dir.glob("*.json"):
            # Convert filename to pattern ID
            # E.g., "button.json" -> "shadcn-button"
            pattern_name = pattern_file.stem
            pattern_id = f"shadcn-{pattern_name}"
            patterns.append(pattern_id)
        
        return sorted(patterns)
