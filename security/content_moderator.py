"""
Content Moderator
Provides additional content validation and rate limiting.
"""

import time
from typing import Dict, List, Optional
from collections import defaultdict, deque
from dataclasses import dataclass
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ModerationResult:
    """Result of content moderation"""
    is_allowed: bool
    reason: str
    action_taken: Optional[str] = None


class ContentModerator:
    """
    Moderates content by:
    - Rate limiting to prevent spam/flooding
    - Blacklist/whitelist pattern matching
    - Message structure validation
    """
    
    def __init__(
        self,
        rate_limit_messages: int = 10,
        rate_limit_window: int = 60,
        enable_rate_limiting: bool = True
    ):
        """
        Initialize the content moderator.
        
        Args:
            rate_limit_messages: Maximum messages allowed per window
            rate_limit_window: Time window in seconds
            enable_rate_limiting: Whether to enable rate limiting
        """
        self.rate_limit_messages = rate_limit_messages
        self.rate_limit_window = rate_limit_window
        self.enable_rate_limiting = enable_rate_limiting
        
        # Track message timestamps per session
        self.message_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=rate_limit_messages))
        
        # Blacklist patterns (can be customized)
        self.blacklist_patterns: List[str] = []
        
        # Whitelist patterns (bypass other checks)
        self.whitelist_patterns: List[str] = []
        
        logger.info(
            f"ContentModerator initialized: rate_limit={rate_limit_messages}/{rate_limit_window}s, "
            f"enabled={enable_rate_limiting}"
        )
    
    def moderate(self, text: str, session_id: str = "default") -> ModerationResult:
        """
        Moderate content.
        
        Args:
            text: Text to moderate
            session_id: Session identifier for rate limiting
            
        Returns:
            ModerationResult indicating if content is allowed
        """
        if not text or not text.strip():
            return ModerationResult(
                is_allowed=False,
                reason="Empty message"
            )
        
        # Check whitelist first (bypass other checks)
        if self._check_whitelist(text):
            return ModerationResult(
                is_allowed=True,
                reason="Whitelisted content"
            )
        
        # Check blacklist
        blacklist_result = self._check_blacklist(text)
        if not blacklist_result.is_allowed:
            return blacklist_result
        
        # Check rate limiting
        if self.enable_rate_limiting:
            rate_limit_result = self._check_rate_limit(session_id)
            if not rate_limit_result.is_allowed:
                return rate_limit_result
        
        # All checks passed
        self._record_message(session_id)
        return ModerationResult(
            is_allowed=True,
            reason="Content approved"
        )
    
    def _check_whitelist(self, text: str) -> bool:
        """Check if text matches whitelist patterns"""
        # Currently no default whitelist patterns
        # Can be extended by users
        return False
    
    def _check_blacklist(self, text: str) -> ModerationResult:
        """Check if text matches blacklist patterns"""
        text_lower = text.lower()
        
        # Default blacklist: extremely offensive or dangerous patterns
        default_blacklist = [
            # Add custom blacklist patterns here if needed
            # Example: r'extremely_dangerous_pattern'
        ]
        
        all_patterns = default_blacklist + self.blacklist_patterns
        
        for pattern in all_patterns:
            if pattern in text_lower:
                logger.warning(f"Blacklisted content detected: {pattern}")
                return ModerationResult(
                    is_allowed=False,
                    reason=f"Content contains blacklisted pattern",
                    action_taken="blocked"
                )
        
        return ModerationResult(
            is_allowed=True,
            reason="No blacklist match"
        )
    
    def _check_rate_limit(self, session_id: str) -> ModerationResult:
        """Check if session has exceeded rate limit"""
        current_time = time.time()
        message_times = self.message_history[session_id]
        
        # Remove messages outside the time window
        cutoff_time = current_time - self.rate_limit_window
        while message_times and message_times[0] < cutoff_time:
            message_times.popleft()
        
        # Check if limit exceeded
        if len(message_times) >= self.rate_limit_messages:
            oldest_message_time = message_times[0]
            wait_time = int(oldest_message_time + self.rate_limit_window - current_time)
            
            logger.warning(
                f"Rate limit exceeded for session {session_id}: "
                f"{len(message_times)} messages in {self.rate_limit_window}s"
            )
            
            return ModerationResult(
                is_allowed=False,
                reason=f"Rate limit exceeded. Please wait {wait_time} seconds.",
                action_taken="rate_limited"
            )
        
        return ModerationResult(
            is_allowed=True,
            reason="Within rate limit"
        )
    
    def _record_message(self, session_id: str):
        """Record a message timestamp for rate limiting"""
        current_time = time.time()
        self.message_history[session_id].append(current_time)
    
    def add_blacklist_pattern(self, pattern: str):
        """
        Add a pattern to the blacklist.
        
        Args:
            pattern: Pattern to blacklist (case-insensitive)
        """
        if pattern not in self.blacklist_patterns:
            self.blacklist_patterns.append(pattern.lower())
            logger.info(f"Added blacklist pattern: {pattern}")
    
    def add_whitelist_pattern(self, pattern: str):
        """
        Add a pattern to the whitelist.
        
        Args:
            pattern: Pattern to whitelist (case-insensitive)
        """
        if pattern not in self.whitelist_patterns:
            self.whitelist_patterns.append(pattern.lower())
            logger.info(f"Added whitelist pattern: {pattern}")
    
    def reset_session(self, session_id: str):
        """
        Reset rate limiting for a session.
        
        Args:
            session_id: Session identifier to reset
        """
        if session_id in self.message_history:
            del self.message_history[session_id]
            logger.info(f"Reset rate limiting for session: {session_id}")
    
    def get_session_stats(self, session_id: str) -> Dict:
        """
        Get statistics for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with session statistics
        """
        current_time = time.time()
        message_times = self.message_history.get(session_id, deque())
        
        # Count messages in current window
        cutoff_time = current_time - self.rate_limit_window
        recent_messages = sum(1 for t in message_times if t >= cutoff_time)
        
        return {
            "session_id": session_id,
            "messages_in_window": recent_messages,
            "limit": self.rate_limit_messages,
            "window_seconds": self.rate_limit_window,
            "remaining": max(0, self.rate_limit_messages - recent_messages)
        }
