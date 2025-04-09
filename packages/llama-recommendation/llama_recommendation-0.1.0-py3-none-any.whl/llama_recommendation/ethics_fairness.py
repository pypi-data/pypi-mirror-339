"""
Fairness metrics and utilities for recommendation systems.

This module provides fairness metrics and algorithms for ensuring
fair treatment across different user groups in recommendations.
"""

import logging

from typing import List, Dict, Any, Optional, Tuple, Set, Union

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
