"""
Energy Optimizer - A tool for analyzing and optimizing energy consumption in embedded systems.

This package provides tools for analyzing embedded code for energy inefficiencies,
suggesting optimizations, and generating reports.
"""

from ._version import __version__

from .analyzer import (
    EnergyIssue,
    SourceLocation,
    analyze_code,
    CodeAnalysisManager,
    CodeParser,
    LoopAnalyzer,
    SleepModeAnalyzer,
    PeripheralAnalyzer,
    ClockConfigAnalyzer,
    MSP430RegisterAnalyzer
)

# Define what's available for import
__all__ = [
    '__version__',
    'EnergyIssue',
    'SourceLocation',
    'analyze_code',
    'CodeAnalysisManager',
    'CodeParser',
]