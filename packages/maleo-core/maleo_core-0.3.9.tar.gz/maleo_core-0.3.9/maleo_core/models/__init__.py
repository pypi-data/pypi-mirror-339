# This file serves as collection of all general and reusable models in MaleoCore

from __future__ import annotations
from .base import BaseModels
from .maleo_suite import MaleoSuiteModels

class MaleoCoreModels:
    Base = BaseModels
    Maleosuite = MaleoSuiteModels

__all__ = ["MaleoCoreModels", "BaseModels", "MaleoSuiteModels"]