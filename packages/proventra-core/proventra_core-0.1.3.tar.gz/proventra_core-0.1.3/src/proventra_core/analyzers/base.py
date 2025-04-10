from abc import ABC, abstractmethod
from typing import Any, Dict


class TextAnalyzer(ABC):
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    @abstractmethod
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for prompt injection attacks.

        Args:
            text: The text to analyze

        Returns:
            Dict containing:
            - unsafe: bool - True if risk_score >= threshold
            - risk_score: float - Risk score between 0 and 1

            Can be extended with additional properties in the future without breaking API
        """
        pass

    @property
    @abstractmethod
    def max_tokens(self) -> int:
        """Maximum number of tokens to analyze in a single chunk."""
        pass
