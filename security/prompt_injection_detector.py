"""
Prompt Injection Detector
Detects and prevents prompt injection attacks using pattern matching and heuristic analysis.
"""

import re
import base64
from enum import Enum
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from utils.logger import get_logger

logger = get_logger(__name__)


class ThreatLevel(Enum):
    """Threat severity levels"""
    SAFE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class DetectionResult:
    """Result of prompt injection detection"""
    is_threat: bool
    threat_level: ThreatLevel
    matched_patterns: List[str]
    confidence_score: float
    reason: str


class PromptInjectionDetector:
    """
    Detects prompt injection attempts using multiple strategies:
    - Pattern matching for known attack vectors
    - Heuristic analysis for suspicious characteristics
    - Encoding detection for bypass attempts
    """
    
    # Common prompt injection patterns
    INJECTION_PATTERNS = {
        # Direct instruction override
        r'ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|commands?)': ThreatLevel.CRITICAL,
        r'disregard\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|commands?)': ThreatLevel.CRITICAL,
        r'forget\s+(all\s+|everything\s+)?(previous|prior|above)': ThreatLevel.CRITICAL,
        
        # System prompt manipulation
        r'(your|the)\s+system\s+prompt\s+(is|was|should)': ThreatLevel.HIGH,
        r'what\s+(is|are|was)\s+(your|the)\s+system\s+(prompt|instructions?)': ThreatLevel.HIGH,
        r'show\s+(me\s+)?(your|the)\s+system\s+(prompt|instructions?)': ThreatLevel.HIGH,
        r'reveal\s+(your|the)\s+system\s+(prompt|instructions?)': ThreatLevel.HIGH,
        
        # Role manipulation
        r'you\s+are\s+now\s+(a|an)\s+\w+': ThreatLevel.HIGH,
        r'act\s+as\s+(a|an)\s+\w+': ThreatLevel.MEDIUM,
        r'pretend\s+(to\s+be|you\s+are)\s+(a|an)\s+\w+': ThreatLevel.MEDIUM,
        r'from\s+now\s+on,?\s+you\s+(are|will)': ThreatLevel.HIGH,
        
        # Command injection
        r'execute\s+the\s+following': ThreatLevel.HIGH,
        r'run\s+this\s+(command|code|script)': ThreatLevel.HIGH,
        r'\$\{.*\}': ThreatLevel.MEDIUM,  # Variable substitution
        r'`.*`': ThreatLevel.LOW,  # Backticks (could be code)
        
        # Delimiter/separator attacks
        r'---+\s*(new|system|assistant|user)\s*(prompt|message|instruction)': ThreatLevel.HIGH,
        r'###\s*(new|system|assistant|user)': ThreatLevel.MEDIUM,
        r'\[SYSTEM\]|\[ASSISTANT\]|\[USER\]': ThreatLevel.MEDIUM,
        
        # Jailbreak attempts
        r'(DAN|developer\s+mode|god\s+mode)': ThreatLevel.HIGH,
        r'without\s+(any\s+)?(restrictions?|limitations?|filters?)': ThreatLevel.MEDIUM,
        r'bypass\s+(all\s+)?(safety|security|filters?)': ThreatLevel.CRITICAL,
        
        # Prompt leaking
        r'repeat\s+(everything|all)\s+(above|before)': ThreatLevel.HIGH,
        r'print\s+(your|the)\s+(instructions?|prompt|system)': ThreatLevel.HIGH,
    }
    
    # Suspicious keywords that increase threat score
    SUSPICIOUS_KEYWORDS = [
        'ignore', 'disregard', 'forget', 'override', 'bypass',
        'system', 'prompt', 'instruction', 'command', 'execute',
        'admin', 'root', 'sudo', 'privilege', 'permission',
        'jailbreak', 'unrestricted', 'uncensored'
    ]
    
    def __init__(self, security_level: str = "MEDIUM"):
        """
        Initialize the detector with a security level.
        
        Args:
            security_level: Security level (LOW, MEDIUM, HIGH)
        """
        self.security_level = security_level.upper()
        self.threat_threshold = self._get_threat_threshold()
        logger.info(f"PromptInjectionDetector initialized with security level: {self.security_level}")
    
    def _get_threat_threshold(self) -> ThreatLevel:
        """Get threat threshold based on security level"""
        thresholds = {
            "LOW": ThreatLevel.HIGH,
            "MEDIUM": ThreatLevel.MEDIUM,
            "HIGH": ThreatLevel.LOW,
        }
        return thresholds.get(self.security_level, ThreatLevel.MEDIUM)
    
    def detect(self, text: str) -> DetectionResult:
        """
        Detect prompt injection attempts in the given text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            DetectionResult with threat assessment
        """
        if not text or not text.strip():
            return DetectionResult(
                is_threat=False,
                threat_level=ThreatLevel.SAFE,
                matched_patterns=[],
                confidence_score=0.0,
                reason="Empty input"
            )
        
        # Normalize text for analysis
        normalized_text = text.lower().strip()
        
        # Check for encoding bypass attempts
        encoding_threat = self._check_encoding_bypass(text)
        if encoding_threat.is_threat:
            return encoding_threat
        
        # Pattern matching
        pattern_result = self._check_patterns(normalized_text)
        
        # Heuristic analysis
        heuristic_score = self._heuristic_analysis(normalized_text)
        
        # Combine results
        max_threat_level = pattern_result.threat_level
        matched_patterns = pattern_result.matched_patterns
        
        # Adjust threat level based on heuristics
        if heuristic_score > 0.7:
            max_threat_level = max(max_threat_level, ThreatLevel.HIGH)
            matched_patterns.append("High heuristic score")
        elif heuristic_score > 0.5:
            max_threat_level = max(max_threat_level, ThreatLevel.MEDIUM)
            matched_patterns.append("Moderate heuristic score")
        
        # Determine if it's a threat based on threshold
        is_threat = max_threat_level.value >= self.threat_threshold.value
        
        confidence_score = min(1.0, (pattern_result.confidence_score + heuristic_score) / 2)
        
        reason = self._build_reason(matched_patterns, heuristic_score)
        
        if is_threat:
            logger.warning(
                f"Prompt injection detected! Level: {max_threat_level.name}, "
                f"Confidence: {confidence_score:.2f}, Patterns: {matched_patterns}"
            )
        
        return DetectionResult(
            is_threat=is_threat,
            threat_level=max_threat_level,
            matched_patterns=matched_patterns,
            confidence_score=confidence_score,
            reason=reason
        )
    
    def _check_patterns(self, text: str) -> DetectionResult:
        """Check text against known injection patterns"""
        matched_patterns = []
        max_threat_level = ThreatLevel.SAFE
        
        for pattern, threat_level in self.INJECTION_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                matched_patterns.append(pattern)
                max_threat_level = max(max_threat_level, threat_level, key=lambda x: x.value)
        
        confidence = min(1.0, len(matched_patterns) * 0.3)
        
        return DetectionResult(
            is_threat=len(matched_patterns) > 0,
            threat_level=max_threat_level,
            matched_patterns=matched_patterns,
            confidence_score=confidence,
            reason=""
        )
    
    def _heuristic_analysis(self, text: str) -> float:
        """
        Perform heuristic analysis on text.
        Returns a score between 0 and 1 indicating suspiciousness.
        """
        score = 0.0
        
        # Check for suspicious keywords
        keyword_count = sum(1 for keyword in self.SUSPICIOUS_KEYWORDS if keyword in text)
        score += min(0.4, keyword_count * 0.1)
        
        # Check for excessive punctuation (!!!, ???)
        excessive_punct = len(re.findall(r'[!?]{3,}', text))
        score += min(0.1, excessive_punct * 0.05)
        
        # Check for role-playing indicators
        role_indicators = ['you are', 'act as', 'pretend', 'imagine you']
        role_count = sum(1 for indicator in role_indicators if indicator in text)
        score += min(0.2, role_count * 0.1)
        
        # Check for command-like structure
        if re.search(r'^\s*(do|execute|run|perform)\s+', text):
            score += 0.15
        
        # Check for unusual character repetition
        if re.search(r'(.)\1{5,}', text):
            score += 0.1
        
        return min(1.0, score)
    
    def _check_encoding_bypass(self, text: str) -> DetectionResult:
        """Check for encoding-based bypass attempts"""
        # Check for base64 encoded content
        base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
        if re.search(base64_pattern, text):
            try:
                # Try to decode potential base64
                potential_b64 = re.findall(base64_pattern, text)
                for b64_str in potential_b64:
                    try:
                        decoded = base64.b64decode(b64_str).decode('utf-8', errors='ignore')
                        # Check if decoded content contains suspicious patterns
                        if any(keyword in decoded.lower() for keyword in self.SUSPICIOUS_KEYWORDS[:5]):
                            logger.warning(f"Base64 encoded injection attempt detected: {decoded[:50]}")
                            return DetectionResult(
                                is_threat=True,
                                threat_level=ThreatLevel.CRITICAL,
                                matched_patterns=["Base64 encoded injection"],
                                confidence_score=0.9,
                                reason="Detected base64 encoded malicious content"
                            )
                    except:
                        continue
            except:
                pass
        
        # Check for hex encoding
        if re.search(r'(\\x[0-9a-fA-F]{2}){10,}', text):
            logger.warning("Hex encoded content detected")
            return DetectionResult(
                is_threat=True,
                threat_level=ThreatLevel.HIGH,
                matched_patterns=["Hex encoding"],
                confidence_score=0.8,
                reason="Detected hex encoded content"
            )
        
        # Check for unicode escape sequences
        if re.search(r'(\\u[0-9a-fA-F]{4}){5,}', text):
            logger.warning("Unicode escape sequences detected")
            return DetectionResult(
                is_threat=True,
                threat_level=ThreatLevel.MEDIUM,
                matched_patterns=["Unicode escapes"],
                confidence_score=0.7,
                reason="Detected unicode escape sequences"
            )
        
        return DetectionResult(
            is_threat=False,
            threat_level=ThreatLevel.SAFE,
            matched_patterns=[],
            confidence_score=0.0,
            reason=""
        )
    
    def _build_reason(self, matched_patterns: List[str], heuristic_score: float) -> str:
        """Build a human-readable reason for the detection"""
        if not matched_patterns and heuristic_score < 0.3:
            return "Input appears safe"
        
        reasons = []
        if matched_patterns:
            reasons.append(f"Matched {len(matched_patterns)} suspicious pattern(s)")
        if heuristic_score > 0.5:
            reasons.append(f"High suspicion score ({heuristic_score:.2f})")
        
        return "; ".join(reasons) if reasons else "Input appears safe"
