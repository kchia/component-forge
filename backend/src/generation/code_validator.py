"""
Code Validator with LLM Fix Loop

Validates generated TypeScript/React code and uses LLM to fix errors.
Supports parallel validation (TypeScript + ESLint) and iterative fixes.
"""

import asyncio
import json
import subprocess
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import os

# Try to import LangSmith for tracing (optional dependency)
try:
    from langsmith import traceable
    LANGSMITH_AVAILABLE = True
except ImportError:
    # Create a no-op decorator if LangSmith is not available
    def traceable(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    LANGSMITH_AVAILABLE = False


@dataclass
class ValidationError:
    """Individual validation error."""
    line: int
    column: int
    message: str
    rule_id: str
    severity: str  # 'error' or 'warning'


@dataclass
class ValidationResult:
    """Result of code validation."""
    valid: bool
    code: str  # Final (possibly fixed) code
    attempts: int  # Number of validation/fix attempts
    typescript_errors: List[ValidationError]
    eslint_errors: List[ValidationError]
    typescript_warnings: List[ValidationError]
    eslint_warnings: List[ValidationError]
    typescript_quality_score: float  # TypeScript-specific quality score (0.0 - 1.0)
    eslint_quality_score: float  # ESLint-specific quality score (0.0 - 1.0)
    overall_quality_score: float  # Overall quality score (0.0 - 1.0)
    compilation_success: bool
    lint_success: bool


class CodeValidator:
    """
    Validate generated code and fix errors using LLM.
    
    Features:
    - Parallel TypeScript and ESLint validation
    - LLM-based error fixing with context
    - Iterative fix loop with max retries
    - Quality scoring based on validation results
    - Performance tracking
    """
    
    def __init__(
        self,
        scripts_dir: Optional[Path] = None,
        llm_generator=None,  # LLMComponentGenerator instance
        max_retries: int = 2,
    ):
        """
        Initialize code validator.
        
        Args:
            scripts_dir: Directory containing validation scripts
            llm_generator: LLM generator for fixing errors
            max_retries: Maximum number of fix attempts
        """
        self.scripts_dir = scripts_dir or Path(__file__).parent.parent.parent / "scripts"
        self.llm_generator = llm_generator
        self.max_retries = max_retries
        
        # Paths to validation scripts
        self.ts_script = self.scripts_dir / "validate_typescript.js"
        self.eslint_script = self.scripts_dir / "validate_eslint.js"
        
        # Verify scripts exist
        if not self.ts_script.exists():
            raise FileNotFoundError(f"TypeScript validation script not found: {self.ts_script}")
        if not self.eslint_script.exists():
            raise FileNotFoundError(f"ESLint validation script not found: {self.eslint_script}")
    
    @traceable(run_type="tool", name="validate_and_fix_code")
    async def validate_and_fix(
        self,
        code: str,
        original_prompt: Optional[str] = None,
    ) -> ValidationResult:
        """
        Validate code and fix errors if needed.
        
        Args:
            code: Generated code to validate
            original_prompt: Original generation prompt (for context in fixes)
        
        Returns:
            ValidationResult with final code and validation status
        """
        current_code = code
        
        for attempt in range(self.max_retries + 1):
            # Run validations in parallel
            ts_result, eslint_result = await asyncio.gather(
                self._validate_typescript(current_code),
                self._validate_eslint(current_code),
            )
            
            # Parse results
            ts_errors = self._parse_validation_result(ts_result, "typescript")
            eslint_errors = self._parse_validation_result(eslint_result, "eslint")
            
            # Separate errors and warnings
            ts_error_list = [e for e in ts_errors if e.severity == "error"]
            ts_warning_list = [e for e in ts_errors if e.severity == "warning"]
            eslint_error_list = [e for e in eslint_errors if e.severity == "error"]
            eslint_warning_list = [e for e in eslint_errors if e.severity == "warning"]
            
            # Check if valid (no errors)
            compilation_success = len(ts_error_list) == 0
            lint_success = len(eslint_error_list) == 0
            valid = compilation_success and lint_success
            
            if valid:
                # Success! Calculate quality scores
                ts_quality_score = self._calculate_typescript_quality_score(
                    ts_error_list,
                    ts_warning_list,
                )
                eslint_quality_score = self._calculate_eslint_quality_score(
                    eslint_error_list,
                    eslint_warning_list,
                )
                overall_quality_score = self._calculate_quality_score(
                    ts_error_list,
                    eslint_error_list,
                    ts_warning_list,
                    eslint_warning_list,
                )
                
                return ValidationResult(
                    valid=True,
                    code=current_code,
                    attempts=attempt + 1,
                    typescript_errors=ts_error_list,
                    eslint_errors=eslint_error_list,
                    typescript_warnings=ts_warning_list,
                    eslint_warnings=eslint_warning_list,
                    typescript_quality_score=ts_quality_score,
                    eslint_quality_score=eslint_quality_score,
                    overall_quality_score=overall_quality_score,
                    compilation_success=True,
                    lint_success=True,
                )
            
            # If not valid and not last attempt, try to fix
            if attempt < self.max_retries:
                if self.llm_generator:
                    try:
                        current_code = await self._llm_fix_errors(
                            current_code,
                            ts_error_list,
                            eslint_error_list,
                            original_prompt,
                        )
                    except Exception as e:
                        # If fix fails, continue with current code
                        pass
        
        # Max retries reached without success
        ts_quality_score = self._calculate_typescript_quality_score(
            ts_error_list,
            ts_warning_list,
        )
        eslint_quality_score = self._calculate_eslint_quality_score(
            eslint_error_list,
            eslint_warning_list,
        )
        overall_quality_score = self._calculate_quality_score(
            ts_error_list,
            eslint_error_list,
            ts_warning_list,
            eslint_warning_list,
        )
        
        return ValidationResult(
            valid=False,
            code=current_code,
            attempts=self.max_retries + 1,
            typescript_errors=ts_error_list,
            eslint_errors=eslint_error_list,
            typescript_warnings=ts_warning_list,
            eslint_warnings=eslint_warning_list,
            typescript_quality_score=ts_quality_score,
            eslint_quality_score=eslint_quality_score,
            overall_quality_score=overall_quality_score,
            compilation_success=compilation_success,
            lint_success=lint_success,
        )
    
    async def _validate_typescript(self, code: str) -> Dict[str, Any]:
        """
        Validate TypeScript code using Node.js script.
        
        Args:
            code: TypeScript code to validate
        
        Returns:
            Validation result as JSON
        """
        try:
            process = await asyncio.create_subprocess_exec(
                "node",
                str(self.ts_script),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate(code.encode("utf-8"))
            
            # Parse JSON output
            result = json.loads(stdout.decode("utf-8"))
            return result
            
        except Exception as e:
            # Return error result
            return {
                "valid": False,
                "errors": [{
                    "line": 0,
                    "column": 0,
                    "message": f"TypeScript validation failed: {str(e)}",
                    "code": 0,
                    "category": "Error",
                }],
                "warnings": [],
                "errorCount": 1,
                "warningCount": 0,
            }
    
    async def _validate_eslint(self, code: str) -> Dict[str, Any]:
        """
        Validate code using ESLint script.
        
        Args:
            code: Code to validate
        
        Returns:
            Validation result as JSON
        """
        try:
            process = await asyncio.create_subprocess_exec(
                "node",
                str(self.eslint_script),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            
            stdout, stderr = await process.communicate(code.encode("utf-8"))
            
            # Parse JSON output
            result = json.loads(stdout.decode("utf-8"))
            return result
            
        except Exception as e:
            # Return error result
            return {
                "valid": False,
                "errors": [{
                    "line": 0,
                    "column": 0,
                    "message": f"ESLint validation failed: {str(e)}",
                    "ruleId": "fatal",
                    "severity": 2,
                }],
                "warnings": [],
                "errorCount": 1,
                "warningCount": 0,
            }
    
    def _parse_validation_result(
        self,
        result: Dict[str, Any],
        validator: str,
    ) -> List[ValidationError]:
        """
        Parse validation result into list of errors.
        
        Args:
            result: JSON result from validator
            validator: 'typescript' or 'eslint'
        
        Returns:
            List of ValidationError objects
        """
        errors = []
        
        # Parse errors
        for error in result.get("errors", []):
            errors.append(ValidationError(
                line=error.get("line", 0),
                column=error.get("column", 0),
                message=error.get("message", ""),
                rule_id=error.get("ruleId", error.get("code", "unknown")),
                severity="error",
            ))
        
        # Parse warnings
        for warning in result.get("warnings", []):
            errors.append(ValidationError(
                line=warning.get("line", 0),
                column=warning.get("column", 0),
                message=warning.get("message", ""),
                rule_id=warning.get("ruleId", warning.get("code", "unknown")),
                severity="warning",
            ))
        
        return errors
    
    async def _llm_fix_errors(
        self,
        code: str,
        ts_errors: List[ValidationError],
        eslint_errors: List[ValidationError],
        original_prompt: Optional[str] = None,
    ) -> str:
        """
        Use LLM to fix validation errors.
        
        Args:
            code: Code with errors
            ts_errors: TypeScript errors
            eslint_errors: ESLint errors
            original_prompt: Original generation prompt for context
        
        Returns:
            Fixed code
        """
        if not self.llm_generator:
            return code
        
        # Build fix prompt
        system_prompt = """You are an expert at debugging and fixing TypeScript and React code.
Your task is to fix ONLY the specific errors listed below while preserving all working code.
Return the complete fixed code in JSON format: {"component_code": "...", "stories_code": "...", "imports": [], "exports": [], "explanation": "..."}"""
        
        # Format errors
        error_lines = []
        
        if ts_errors:
            error_lines.append("## TypeScript Errors:")
            for error in ts_errors[:5]:  # Limit to first 5
                error_lines.append(
                    f"- Line {error.line}, Column {error.column}: {error.message}"
                )
        
        if eslint_errors:
            error_lines.append("\n## ESLint Errors:")
            for error in eslint_errors[:5]:  # Limit to first 5
                error_lines.append(
                    f"- Line {error.line}, Column {error.column}: {error.message} ({error.rule_id})"
                )
        
        errors_text = "\n".join(error_lines)
        
        user_prompt = f"""## Original Code (WITH ERRORS)
```tsx
{code}
```

{errors_text}

## Task
Fix ONLY the specific errors listed above. Preserve all working code and functionality.
Return the complete fixed code."""
        
        # Call LLM to fix
        result = await self.llm_generator.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,  # Lower temperature for more deterministic fixes
        )
        
        return result.component_code
    
    def _calculate_quality_score(
        self,
        ts_errors: List[ValidationError],
        eslint_errors: List[ValidationError],
        ts_warnings: List[ValidationError],
        eslint_warnings: List[ValidationError],
    ) -> float:
        """
        Calculate overall quality score based on validation results.
        
        Score factors:
        - No errors: base 1.0
        - Each error: -0.2
        - Each warning: -0.05
        
        Returns:
            Quality score from 0.0 to 1.0
        """
        score = 1.0
        
        # Deduct for errors (major impact)
        error_count = len(ts_errors) + len(eslint_errors)
        score -= error_count * 0.2
        
        # Deduct for warnings (minor impact)
        warning_count = len(ts_warnings) + len(eslint_warnings)
        score -= warning_count * 0.05
        
        # Clamp to [0.0, 1.0]
        return max(0.0, min(1.0, score))
    
    def _calculate_typescript_quality_score(
        self,
        ts_errors: List[ValidationError],
        ts_warnings: List[ValidationError],
    ) -> float:
        """
        Calculate TypeScript-specific quality score.
        
        Returns:
            Quality score from 0.0 to 1.0
        """
        score = 1.0
        score -= len(ts_errors) * 0.2
        score -= len(ts_warnings) * 0.05
        return max(0.0, min(1.0, score))
    
    def _calculate_eslint_quality_score(
        self,
        eslint_errors: List[ValidationError],
        eslint_warnings: List[ValidationError],
    ) -> float:
        """
        Calculate ESLint-specific quality score.
        
        Returns:
            Quality score from 0.0 to 1.0
        """
        score = 1.0
        score -= len(eslint_errors) * 0.2
        score -= len(eslint_warnings) * 0.05
        return max(0.0, min(1.0, score))
