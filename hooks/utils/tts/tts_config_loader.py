#!/usr/bin/env python3
"""
TTS Configuration Loader
Loads and provides TTS configuration from tts_config.json
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class TTSConfig:
    def __init__(self):
        self.config_path = Path(__file__).parent.parent.parent / "tts_config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file, with defaults if file doesn't exist."""
        default_config = {
            "enabled": True,
            "volume": 0.7,
            "provider_priority": ["elevenlabs", "pyttsx3"],
            "providers": {
                "elevenlabs": {
                    "enabled": True,
                    "voice_id": "default",
                    "model": "eleven_monolingual_v1"
                },
                "openai": {
                    "enabled": False,
                    "voice": "alloy",
                    "model": "tts-1"
                },
                "pyttsx3": {
                    "enabled": True,
                    "rate": 150,
                    "voice_index": 0
                }
            },
            "notifications": {
                "on_task_complete": True,
                "on_user_input_needed": True,
                "on_subagent_complete": True,
                "on_error": False
            },
            "quiet_hours": {
                "enabled": False,
                "start": "22:00",
                "end": "08:00"
            }
        }
        
        if not self.config_path.exists():
            # Create default config file if it doesn't exist
            self.config_path.write_text(json.dumps(default_config, indent=2))
            return default_config
        
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Return defaults if config file is corrupted
            return default_config
    
    def is_enabled(self) -> bool:
        """Check if TTS is globally enabled."""
        return self.config.get("enabled", True)
    
    def get_volume(self) -> float:
        """Get the configured volume level (0.0 to 1.0)."""
        return min(max(self.config.get("volume", 0.7), 0.0), 1.0)
    
    def is_provider_enabled(self, provider: str) -> bool:
        """Check if a specific TTS provider is enabled."""
        if not self.is_enabled():
            return False
        providers = self.config.get("providers", {})
        provider_config = providers.get(provider, {})
        return provider_config.get("enabled", False)
    
    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get configuration for a specific provider."""
        providers = self.config.get("providers", {})
        return providers.get(provider, {})
    
    def should_notify(self, event_type: str) -> bool:
        """Check if notification should be sent for a specific event type."""
        if not self.is_enabled():
            return False
            
        # Check quiet hours
        if self._is_quiet_hours():
            return False
            
        notifications = self.config.get("notifications", {})
        event_map = {
            "task_complete": "on_task_complete",
            "user_input": "on_user_input_needed",
            "subagent_complete": "on_subagent_complete",
            "error": "on_error"
        }
        
        notification_key = event_map.get(event_type)
        if notification_key:
            return notifications.get(notification_key, True)
        return True
    
    def _is_quiet_hours(self) -> bool:
        """Check if current time is within quiet hours."""
        quiet_hours = self.config.get("quiet_hours", {})
        if not quiet_hours.get("enabled", False):
            return False
        
        try:
            now = datetime.now().time()
            start_str = quiet_hours.get("start", "22:00")
            end_str = quiet_hours.get("end", "08:00")
            
            start_time = datetime.strptime(start_str, "%H:%M").time()
            end_time = datetime.strptime(end_str, "%H:%M").time()
            
            # Handle overnight quiet hours
            if start_time > end_time:
                return now >= start_time or now <= end_time
            else:
                return start_time <= now <= end_time
        except (ValueError, TypeError):
            return False
    
    def get_preferred_provider(self) -> Optional[str]:
        """Get the first enabled provider from priority list."""
        if not self.is_enabled():
            return None
            
        priority = self.config.get("provider_priority", ["elevenlabs", "pyttsx3"])
        for provider in priority:
            if self.is_provider_enabled(provider):
                # Also check if required API key exists for the provider
                if provider == "elevenlabs" and not os.getenv('ELEVENLABS_API_KEY'):
                    continue
                if provider == "openai" and not os.getenv('OPENAI_API_KEY'):
                    continue
                return provider
        return None


# Global instance for easy access
tts_config = TTSConfig()