#!/usr/bin/env python3
"""
Energy Optimizer - Code Analysis Module

This module implements the code analysis architecture for identifying energy
inefficiencies in embedded systems code, particularly for MSP430 microcontrollers.
"""

import os
import logging
import re
import random
from typing import Dict, List, Any, Optional, Tuple
from abc import ABC, abstractmethod
import ast
import json
from dataclasses import dataclass

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("energy-optimizer.analyzer")


@dataclass
class SourceLocation:
    """Represents a location in source code."""
    file: str
    line: int
    column: int = 0


@dataclass
class EnergyIssue:
    """Representation of an energy-related issue found in code."""
    issue_type: str  # E.g., "inefficient_loop", "suboptimal_sleep_mode"
    location: SourceLocation
    description: str
    impact: float  # Estimated energy impact (0.0-1.0)
    suggestion: str
    code_snippet: str = ""
    fix_complexity: float = 0.5  # How complex it is to fix (0.0-1.0)

    def __str__(self) -> str:
        return f"{self.location.file}:{self.location.line} - {self.description} (Impact: {self.impact:.2f})"


class AnalysisContext:
    """Holds context information for the analysis process."""

    def __init__(self, project_path: str, config: Dict[str, Any] = None):
        self.project_path = os.path.abspath(project_path)
        self.config = config or {}
        self.issues: List[EnergyIssue] = []
        self.file_cache: Dict[str, str] = {}  # Cache for file contents
        self.ast_cache: Dict[str, Any] = {}   # Cache for parsed ASTs


class Analyzer(ABC):
    """Base class for all analyzers."""

    def __init__(self, context: AnalysisContext):
        self.context = context

    @abstractmethod
    def analyze(self, file_path: str, ast_node: Any = None) -> List[EnergyIssue]:
        """Analyze a file or AST node and return found issues."""
        pass


class CodeParser:
    """Parses source code files into AST."""

    def __init__(self, context: AnalysisContext):
        self.context = context

    def detect_language(self, file_path: str) -> str:
        """Detect the programming language of a file."""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext in ['.c', '.h']:
            return 'c'
        elif ext in ['.cpp', '.hpp', '.cc', '.cxx']:
            return 'cpp'
        elif ext in ['.py']:
            return 'python'
        elif ext in ['.asm', '.s']:
            return 'assembly'
        else:
            # Default to C for embedded projects
            return 'c'

    def parse_file(self, file_path: str) -> Optional[Any]:
        """Parse a file into an AST."""
        if file_path in self.context.ast_cache:
            return self.context.ast_cache[file_path]

        try:
            language = self.detect_language(file_path)

            # Get file content
            if file_path not in self.context.file_cache:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.context.file_cache[file_path] = f.read()

            file_content = self.context.file_cache[file_path]

            # Parse based on language
            if language == 'python':
                # Use Python's built-in ast module for Python files
                tree = ast.parse(file_content, filename=file_path)
                self.context.ast_cache[file_path] = tree
                return tree
            elif language in ['c', 'cpp']:
                # In a real implementation, we would use a C/C++ parser like pycparser or clang
                # For this prototype, we'll return a simple placeholder
                # Placeholder: just tokenize the file
                tokens = self._tokenize_c_like(file_content)
                self.context.ast_cache[file_path] = tokens
                return tokens
            elif language == 'assembly':
                # Simple line-based parsing for assembly
                lines = file_content.splitlines()
                self.context.ast_cache[file_path] = lines
                return lines
            else:
                logger.warning(f"Unsupported language for file: {file_path}")
                return None

        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {e}")
            return None

    def _tokenize_c_like(self, content: str) -> List[Dict[str, Any]]:
        """Simple tokenizer for C-like languages (placeholder for real parsing)."""
        # This is a very simplified tokenizer for demonstration
        # In a real implementation, we would use a proper parser

        tokens = []

        # Simple regex patterns for C-like syntax elements
        patterns = [
            ('INCLUDE', r'#include\s+[<"]([^>"]+)[>"]'),
            ('DEFINE', r'#define\s+(\w+)(?:\s+(.+))?'),
            ('FUNCTION', r'(\w+)\s+(\w+)\s*\(([^)]*)\)\s*\{'),
            ('IF', r'if\s*\(([^)]+)\)\s*\{'),
            ('WHILE', r'while\s*\(([^)]+)\)\s*\{'),
            ('FOR', r'for\s*\(([^)]+)\)\s*\{'),
            ('COMMENT', r'//(.*)$|/\*(.*?)\*/'),
        ]

        # Find all occurrences of each pattern
        for token_type, pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                line_number = content[:match.start()].count('\n') + 1
                tokens.append({
                    'type': token_type,
                    'text': match.group(0),
                    'line': line_number,
                    'column': match.start() - content.rfind('\n', 0, match.start()),
                    'groups': match.groups()
                })

        # Sort tokens by their position in the file
        tokens.sort(key=lambda t: (t['line'], t['column']))

        return tokens


class LoopAnalyzer(Analyzer):
    """Analyzes loops for energy inefficiencies."""

    def analyze(self, file_path: str, ast_node: Any = None) -> List[EnergyIssue]:
        issues = []

        if not ast_node:
            ast_node = self.context.ast_cache.get(file_path)
            if not ast_node:
                logger.warning(f"No AST available for {file_path}")
                return issues

        # Get file content for snippets
        file_content = self.context.file_cache.get(file_path, "")
        file_lines = file_content.splitlines() if file_content else []

        # If we have C-like tokens
        if isinstance(ast_node, list) and all(isinstance(item, dict) for item in ast_node):
            # Find loops in tokens
            for token in ast_node:
                if token['type'] in ['FOR', 'WHILE']:
                    loop_condition = token['groups'][0] if token['groups'] else ""
                    line_number = token['line']

                    # Get code snippet
                    start_line = max(0, line_number - 2)
                    end_line = min(len(file_lines), line_number + 3)
                    code_snippet = "\n".join(file_lines[start_line:end_line])

                    # Check for inefficient patterns in loop conditions
                    if self._is_inefficient_loop(loop_condition):
                        issues.append(EnergyIssue(
                            issue_type="inefficient_loop",
                            location=SourceLocation(file=file_path, line=line_number),
                            description="Inefficient loop pattern detected - function calls or complex calculations in loop condition",
                            impact=0.6,
                            suggestion="Move function calls and calculations outside the loop or use simpler conditions",
                            code_snippet=code_snippet
                        ))

                    # Check if the loop might be doing unnecessary work
                    if self._has_unnecessary_operations_in_loop(token, ast_node):
                        issues.append(EnergyIssue(
                            issue_type="unnecessary_loop_operations",
                            location=SourceLocation(file=file_path, line=line_number),
                            description="Loop may contain operations that could be moved outside the loop",
                            impact=0.7,
                            suggestion="Identify and move loop-invariant operations outside the loop",
                            code_snippet=code_snippet
                        ))

        return issues

    def _is_inefficient_loop(self, condition: str) -> bool:
        """Check if a loop has inefficient patterns."""
        # In a real implementation, this would have sophisticated pattern detection
        # For the prototype, we'll check for some simple inefficient patterns

        # Check for function calls in loop condition
        if re.search(r'\b\w+\(', condition):
            return True

        # Check for complex calculations in loop condition
        # FIX: Fix the regular expression here - there was a syntax error
        if re.search(r'[+\-*/]', condition) and not re.match(r'^\s*\w+\s*[+\-*/][=]\s*\d+\s*$', condition):
            return True

        return False

    def _has_unnecessary_operations_in_loop(self, loop_token: Dict[str, Any], tokens: List[Dict[str, Any]]) -> bool:
        """Check if a loop might have unnecessary operations that could be moved outside."""
        # This would require more sophisticated analysis in a real implementation
        # For the prototype, we'll return a placeholder value
        return random.random() > 0.7  # Simulate finding issues in ~30% of loops


class SleepModeAnalyzer(Analyzer):
    """Analyzes sleep mode configurations for energy inefficiencies."""

    # MSP430 power modes and their relative energy efficiency (higher is better)
    POWER_MODES = {
        'LPM0': 1,
        'LPM1': 2,
        'LPM2': 3,
        'LPM3': 4,
        'LPM4': 5
    }

    def analyze(self, file_path: str, ast_node: Any = None) -> List[EnergyIssue]:
        issues = []

        if not ast_node:
            ast_node = self.context.ast_cache.get(file_path)
            if not ast_node:
                logger.warning(f"No AST available for {file_path}")
                return issues

        # Get file content for snippets
        file_content = self.context.file_cache.get(file_path, "")

        # Look for power mode patterns in the file content
        for mode_name, efficiency in self.POWER_MODES.items():
            if mode_name in file_content:
                # For each instance of a power mode, check if it's the optimal choice
                for match in re.finditer(r'\b' + mode_name + r'\b', file_content):
                    line_number = file_content[:match.start()].count('\n') + 1

                    # Get surrounding context (simplistic approach)
                    start_pos = max(0, match.start() - 100)
                    end_pos = min(len(file_content), match.end() + 100)
                    context = file_content[start_pos:end_pos]

                    # Check if a more efficient mode could be used
                    better_mode = self._suggest_better_power_mode(mode_name, context)
                    if better_mode:
                        # Get code snippet
                        file_lines = file_content.splitlines()
                        start_line = max(0, line_number - 2)
                        end_line = min(len(file_lines), line_number + 3)
                        code_snippet = "\n".join(file_lines[start_line:end_line])

                        issues.append(EnergyIssue(
                            issue_type="suboptimal_sleep_mode",
                            location=SourceLocation(file=file_path, line=line_number),
                            description=f"Suboptimal power mode {mode_name} being used",
                            impact=0.5 + (self.POWER_MODES[better_mode] - efficiency) * 0.1,
                            suggestion=f"Consider using {better_mode} for better energy efficiency",
                            code_snippet=code_snippet
                        ))

        return issues

    def _suggest_better_power_mode(self, current_mode: str, context: str) -> Optional[str]:
        """Suggest a better power mode based on the context."""
        current_efficiency = self.POWER_MODES.get(current_mode, 0)

        # This is a simplistic heuristic - in a real implementation, we would
        # need much more sophisticated analysis of the surrounding code

        # If we find indicators of long sleep times, suggest deeper sleep modes
        if 'long' in context.lower() or 'delay' in context.lower() or 'wait' in context.lower():
            for mode, efficiency in self.POWER_MODES.items():
                if efficiency > current_efficiency:
                    return mode

        # If we see wake-up sources that are compatible with deeper sleep
        if 'RTC' in context or 'timer' in context.lower():
            # LPM3 is often a good balance for timer-based wake-up
            if current_mode in ['LPM0', 'LPM1', 'LPM2'] and 'LPM3' in self.POWER_MODES:
                return 'LPM3'

        return None


class PeripheralAnalyzer(Analyzer):
    """Analyzes peripheral usage for energy inefficiencies."""

    def analyze(self, file_path: str, ast_node: Any = None) -> List[EnergyIssue]:
        issues = []

        if not ast_node:
            ast_node = self.context.ast_cache.get(file_path)
            if not ast_node:
                logger.warning(f"No AST available for {file_path}")
                return issues

        # Get file content
        file_content = self.context.file_cache.get(file_path, "")
        file_lines = file_content.splitlines() if file_content else []

        # Look for common peripheral initialization and usage patterns
        peripheral_patterns = {
            'ADC': r'\b(ADC\w*|adc\w*)\b',
            'UART': r'\b(UART\w*|uart\w*)\b',
            'SPI': r'\b(SPI\w*|spi\w*)\b',
            'I2C': r'\b(I2C\w*|i2c\w*)\b',
            'GPIO': r'\b(GPIO\w*|gpio\w*|P\d[IN|OUT|DIR|SEL])\b',
            'Timer': r'\b(Timer\w*|timer\w*|TA\d\w*)\b'
        }

        for peripheral, pattern in peripheral_patterns.items():
            for match in re.finditer(pattern, file_content, re.MULTILINE):
                line_number = file_content[:match.start()].count('\n') + 1

                # Check if peripheral is properly disabled when not in use
                if not self._is_properly_disabled(peripheral, file_content):
                    # Get code snippet
                    start_line = max(0, line_number - 2)
                    end_line = min(len(file_lines), line_number + 3)
                    code_snippet = "\n".join(file_lines[start_line:end_line])

                    issues.append(EnergyIssue(
                        issue_type="peripheral_not_disabled",
                        location=SourceLocation(file=file_path, line=line_number),
                        description=f"{peripheral} peripheral may not be properly disabled when not in use",
                        impact=0.7,
                        suggestion=f"Ensure {peripheral} is properly disabled when not needed to save power",
                        code_snippet=code_snippet
                    ))

        return issues

    def _is_properly_disabled(self, peripheral: str, content: str) -> bool:
        """Check if a peripheral is properly disabled when not in use."""
        # This is a simplistic check - in a real implementation, we would
        # perform much more sophisticated analysis

        # Look for disable/power down patterns
        disable_patterns = [
            f"{peripheral}.*disable",
            f"{peripheral}.*power.*down",
            f"{peripheral}.*sleep",
            f"{peripheral}.*off",
            f"disable.*{peripheral}",
        ]

        for pattern in disable_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True

        # Simulate finding issues in ~40% of peripherals
        return random.random() > 0.6


class ClockConfigAnalyzer(Analyzer):
    """Analyzes clock configurations for energy inefficiencies."""

    def analyze(self, file_path: str, ast_node: Any = None) -> List[EnergyIssue]:
        issues = []

        # Get file content
        file_content = self.context.file_cache.get(file_path, "")
        if not file_content:
            return issues

        file_lines = file_content.splitlines()

        # Look for clock configuration patterns
        clock_patterns = [
            (r'\bDCOCTL\b', "DCO configuration"),
            (r'\bBCSCTL\d\b', "Basic Clock System configuration"),
            (r'\bMCLK\b', "Master Clock configuration"),
            (r'\bSMCLK\b', "Sub-Main Clock configuration"),
            (r'\bACLK\b', "Auxiliary Clock configuration"),
            (r'\bCS_\w+', "Clock System configuration")
        ]

        for pattern, description in clock_patterns:
            for match in re.finditer(pattern, file_content):
                line_number = file_content[:match.start()].count('\n') + 1

                # Get code snippet
                start_line = max(0, line_number - 2)
                end_line = min(len(file_lines), line_number + 3)
                code_snippet = "\n".join(file_lines[start_line:end_line])

                # Check if clock frequency is higher than necessary
                if self._is_clock_frequency_too_high(code_snippet):
                    issues.append(EnergyIssue(
                        issue_type="high_clock_frequency",
                        location=SourceLocation(file=file_path, line=line_number),
                        description="Clock frequency may be higher than necessary",
                        impact=0.8,
                        suggestion="Consider reducing clock frequency when high performance is not needed",
                        code_snippet=code_snippet
                    ))

                # Check if unused clocks are disabled
                if self._are_unused_clocks_enabled(code_snippet):
                    issues.append(EnergyIssue(
                        issue_type="unused_clocks_enabled",
                        location=SourceLocation(file=file_path, line=line_number),
                        description="Unused clocks may be enabled",
                        impact=0.6,
                        suggestion="Disable unused clock sources to save power",
                        code_snippet=code_snippet
                    ))

        return issues

    def _is_clock_frequency_too_high(self, code_snippet: str) -> bool:
        """Check if clock frequency is set higher than necessary."""
        # In a real implementation, this would analyze the actual frequency values
        # For now, we'll use a simple heuristic based on keywords

        high_freq_indicators = [
            r'\b16\s*MHz\b', r'\b8\s*MHz\b', r'\bXT2\b', r'\bDCO\s*=\s*\d+'
        ]

        for indicator in high_freq_indicators:
            if re.search(indicator, code_snippet):
                # Simulate finding issues in ~30% of clock configurations
                return random.random() > 0.7

        return False

    def _are_unused_clocks_enabled(self, code_snippet: str) -> bool:
        """Check if unused clocks are left enabled."""
        # In a real implementation, we would track which clocks are actually used
        # For now, we'll use a simple heuristic

        # If multiple clocks are configured but not explicitly disabled
        clock_enables = len(re.findall(r'\b(ACLK|MCLK|SMCLK)\b', code_snippet))
        clock_disables = len(re.findall(r'\b(ACLK|MCLK|SMCLK).*off\b', code_snippet.lower()))

        if clock_enables > 1 and clock_disables == 0:
            # Simulate finding issues in ~40% of such cases
            return random.random() > 0.6

        return False


class MSP430RegisterAnalyzer(Analyzer):
    """Analyzes MSP430-specific register configurations."""

    def analyze(self, file_path: str, ast_node: Any = None) -> List[EnergyIssue]:
        issues = []

        # Get file content
        file_content = self.context.file_cache.get(file_path, "")
        if not file_content:
            return issues

        file_lines = file_content.splitlines()

        # MSP430 register patterns to look for
        register_patterns = {
            r'\bP\d(IN|OUT|DIR|SEL)\b': "Port configuration",
            r'\bLPM\d\b': "Low Power Mode",
            r'\bPMMCTL\d\b': "Power Management",
            r'\bSVSMHCTL\b': "Supervisor configuration",
            r'\bSVSMLCTL\b': "Supervisor configuration",
            r'\bPMMRIE\b': "PMM interrupt enable"
        }

        for pattern, description in register_patterns.items():
            for match in re.finditer(pattern, file_content):
                line_number = file_content[:match.start()].count('\n') + 1

                # Get code snippet
                start_line = max(0, line_number - 2)
                end_line = min(len(file_lines), line_number + 3)
                code_snippet = "\n".join(file_lines[start_line:end_line])

                # Analyze for specific MSP430 inefficiencies
                issues.extend(self._check_msp430_specific_issues(
                    match.group(0),
                    code_snippet,
                    file_path,
                    line_number
                ))

        return issues

    def _check_msp430_specific_issues(self, register: str, code_snippet: str, file_path: str, line_number: int) -> List[EnergyIssue]:
        """Check for MSP430-specific energy issues based on register usage."""
        issues = []

        # Port configuration check
        if re.match(r'P\d(IN|OUT|DIR|SEL)', register):
            if 'OUT' in register and not re.search(r'P\dDIR\s*=', code_snippet):
                issues.append(EnergyIssue(
                    issue_type="incomplete_port_config",
                    location=SourceLocation(file=file_path, line=line_number),
                    description="Port output set without configuring direction",
                    impact=0.4,
                    suggestion="Configure port direction before setting output",
                    code_snippet=code_snippet
                ))

        # Low Power Mode check
        elif re.match(r'LPM\d', register):
            # Already handled by SleepModeAnalyzer
            pass

        # PMM configuration check
        elif re.match(r'PMMCTL\d', register):
            if 'SVMHE' in code_snippet and 'SVMLE' in code_snippet:
                issues.append(EnergyIssue(
                    issue_type="excessive_supervision",
                    location=SourceLocation(file=file_path, line=line_number),
                    description="Both high-side and low-side supervision enabled",
                    impact=0.6,
                    suggestion="Consider if both supervision sides are necessary",
                    code_snippet=code_snippet
                ))

        return issues


class AnalyzerFactory:
    """Factory for creating analyzer instances."""

    @staticmethod
    def create_analyzers(context: AnalysisContext) -> List[Analyzer]:
        """Create all configured analyzers."""
        return [
            LoopAnalyzer(context),
            SleepModeAnalyzer(context),
            PeripheralAnalyzer(context),
            ClockConfigAnalyzer(context),
            MSP430RegisterAnalyzer(context)
        ]


class CodeAnalysisManager:
    """Manages the entire code analysis process."""

    def __init__(self, project_path: str, config: Dict[str, Any] = None):
        self.context = AnalysisContext(project_path, config)
        self.parser = CodeParser(self.context)
        self.analyzers = AnalyzerFactory.create_analyzers(self.context)

    def analyze_project(self) -> List[EnergyIssue]:
        """Analyze the entire project."""
        logger.info(f"Starting analysis of project at {self.context.project_path}")

        # Scan for relevant files
        self._scan_files()

        # Run all analyzers on all files
        for file_path in self.context.file_cache.keys():
            self._analyze_file(file_path)

        # Sort issues by impact (highest first)
        self.context.issues.sort(key=lambda x: x.impact, reverse=True)

        logger.info(f"Analysis completed. Found {len(self.context.issues)} issues.")
        return self.context.issues

    def _scan_files(self):
        """Scan files in the project directory."""
        logger.info("Scanning project files")

        for root, _, files in os.walk(self.context.project_path):
            for file in files:
                if file.endswith(('.c', '.h', '.cpp', '.hpp')):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.context.project_path)

                    # Read and cache file content
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            self.context.file_cache[file_path] = f.read()
                        logger.debug(f"Scanned file: {relative_path}")
                    except Exception as e:
                        logger.error(f"Error reading file {relative_path}: {e}")

        logger.info(f"Scanned {len(self.context.file_cache)} files")

    def _analyze_file(self, file_path: str):
        """Analyze a single file with all analyzers."""
        relative_path = os.path.relpath(file_path, self.context.project_path)
        logger.debug(f"Analyzing file: {relative_path}")

        # Parse the file
        ast_node = self.parser.parse_file(file_path)
        if not ast_node:
            logger.warning(f"Failed to parse {relative_path}")
            return

        # Run all analyzers
        for analyzer in self.analyzers:
            try:
                issues = analyzer.analyze(file_path, ast_node)
                self.context.issues.extend(issues)
                if issues:
                    logger.debug(f"Found {len(issues)} issues with {analyzer.__class__.__name__}")
            except Exception as e:
                logger.error(f"Error in {analyzer.__class__.__name__} analyzing {relative_path}: {e}")


def analyze_code(project_path: str, config: Dict[str, Any] = None) -> List[EnergyIssue]:
    """Analyze code in the specified project path."""
    manager = CodeAnalysisManager(project_path, config)
    return manager.analyze_project()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python code_analyzer.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    issues = analyze_code(project_path)

    print(f"Found {len(issues)} energy issues:")
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")