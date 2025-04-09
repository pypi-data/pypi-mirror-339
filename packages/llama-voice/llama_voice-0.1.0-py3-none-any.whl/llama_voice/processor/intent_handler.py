"""
Intent Handler module for detecting user intents from voice input.

This module analyzes transcribed text and prosodic features to detect user intents,
and can integrate with SiriKit for system-level actions.
"""

import json
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Conditional imports for MLX
try:
    import mlx.core as mx
    import mlx.nn as nn

    HAS_MLX = True
except ImportError:
    HAS_MLX = False

# Conditional imports for SiriKit integration
try:
    import Foundation
    import Intents
    import pyobjc

    HAS_SIRIKIT = True
except ImportError:
    HAS_SIRIKIT = False

from llama_voice.utils.logging import setup_logger


class IntentDomain(Enum):
    """Domains of intents supported by the handler."""

    GENERAL = "general"
    MEDIA = "media"
    COMMUNICATION = "communication"
    NAVIGATION = "navigation"
    PRODUCTIVITY = "productivity"
    HOME = "home"
    CUSTOM = "custom"


@dataclass
class IntentConfig:
    """Configuration for intent detection."""

    enabled_domains: List[IntentDomain] = None
    confidence_threshold: float = 0.6
    use_prosody: bool = True
    enable_sirikit: bool = False
    custom_intents_path: Optional[str] = None

    def __post_init__(self):
        if self.enabled_domains is None:
            self.enabled_domains = [domain for domain in IntentDomain]


class IntentHandler:
    """
    Intent Handler for detecting user intents from voice input.

    This class analyzes transcribed text and prosodic features to detect user intents,
    and can integrate with SiriKit for system-level actions.
    """

    # Base intents by domain
    BASE_INTENTS = {
        IntentDomain.GENERAL: ["help", "confirm", "cancel", "stop", "repeat"],
        IntentDomain.MEDIA: [
            "play_media",
            "pause_media",
            "next_track",
            "previous_track",
            "volume_up",
            "volume_down",
            "mute",
        ],
        IntentDomain.COMMUNICATION: ["call", "message", "email", "video_call"],
        IntentDomain.NAVIGATION: ["navigate_to", "find_nearby", "get_directions", "show_map"],
        IntentDomain.PRODUCTIVITY: [
            "create_reminder",
            "set_alarm",
            "create_note",
            "check_calendar",
        ],
        IntentDomain.HOME: ["lights_on", "lights_off", "adjust_temperature", "lock_doors"],
    }

    # Intent patterns (simplified regex patterns for basic intent matching)
    INTENT_PATTERNS = {
        # General
        "help": r"help|assist|support|how (do|can|to)|what can you do",
        "confirm": r"yes|yeah|confirm|correct|right|ok|okay|sure|yep|yup",
        "cancel": r"cancel|nevermind|never mind|forget it",
        "stop": r"stop|end|quit|exit|terminate",
        "repeat": r"repeat|say (that|it) again|what did you say",
        # Media
        "play_media": r"play|start|resume|listen to",
        "pause_media": r"pause|stop playing|halt",
        "next_track": r"next|skip|forward",
        "previous_track": r"previous|back|rewind",
        "volume_up": r"louder|volume up|increase volume|turn (it|the volume) up",
        "volume_down": r"quieter|volume down|decrease volume|lower|turn (it|the volume) down",
        "mute": r"mute|silence|quiet|no sound",
        # Communication
        "call": r"call|phone|dial|ring",
        "message": r"message|text|send (a )?(message|text)|sms",
        "email": r"email|send (an )?email|mail",
        "video_call": r"video call|facetime|zoom|video chat|video conference",
        # Navigation
        "navigate_to": r"navigate to|directions to|take me to|go to|route to",
        "find_nearby": r"find nearby|what.?s near|close to me|around (me|here)|in the area",
        "get_directions": r"how (do|can) (i|we) get to|directions",
        "show_map": r"show( me)? (the )?map|display( the)? map|open maps",
        # Productivity
        "create_reminder": r"remind me to|set a reminder|create a reminder|new reminder",
        "set_alarm": r"set (an|a) alarm|wake me up at|alarm for",
        "create_note": r"(create|make|take) (a )?note|write (this|that) down|note that",
        "check_calendar": r"check (my )?calendar|what.?s on my calendar|appointments|schedule",
        # Home
        "lights_on": r"turn on (the )?lights|lights on",
        "lights_off": r"turn off (the )?lights|lights off",
        "adjust_temperature": r"set (the )?temperature|adjust (the )?thermostat|make it (warmer|cooler)",
        "lock_doors": r"lock (the )?(doors?|house)|secure the (doors?|house)",
    }

    def __init__(
        self,
        config: Optional[IntentConfig] = None,
        model_path: Optional[str] = None,
        cache_dir: Optional[Union[str, Path]] = None,
        log_level: int = logging.INFO,
    ):
        """
        Initialize the intent handler.

        Args:
            config: Configuration for intent handling
            model_path: Path to a custom intent detection model
            cache_dir: Directory to cache models and data
            log_level: Logging level

        Raises:
            ImportError: If SiriKit integration is enabled but not available
            ValueError: If invalid configuration is provided
        """
        self.logger = setup_logger("intent_handler", log_level)

        self.config = config or IntentConfig()
        self.model_path = model_path
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".llama_voice" / "models"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Check SiriKit availability if enabled
        if self.config.enable_sirikit and not HAS_SIRIKIT:
            self.logger.warning("SiriKit integration enabled but pyobjc not available")
            self.config.enable_sirikit = False

        # Load intents
        self.intents = self._load_intents()

        # Compile regex patterns
        self.patterns = self._compile_patterns()

        # Initialize SiriKit if enabled
        self.sirikit_handler = None
        if self.config.enable_sirikit:
            self._init_sirikit()

        # Initialize MLX model if available
        self.mlx_model = None
        if HAS_MLX and self.model_path:
            self._load_mlx_model()

        self.logger.info(f"Intent Handler initialized with {len(self.intents)} intents")

    def _load_intents(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all configured intents.

        Returns:
            Dictionary of intents with metadata
        """
        intents = {}

        # Load base intents for enabled domains
        for domain in self.config.enabled_domains:
            if domain == IntentDomain.CUSTOM:
                continue

            if domain in self.BASE_INTENTS:
                for intent_name in self.BASE_INTENTS[domain.value]:
                    intents[intent_name] = {
                        "domain": domain.value,
                        "requires_params": self._intent_requires_params(intent_name),
                    }

        # Load custom intents if specified
        if IntentDomain.CUSTOM in self.config.enabled_domains and self.config.custom_intents_path:
            custom_path = Path(self.config.custom_intents_path)
            if custom_path.exists():
                try:
                    with open(custom_path, "r") as f:
                        custom_intents = json.load(f)

                    # Add custom intents
                    for intent_name, intent_data in custom_intents.items():
                        intents[intent_name] = {
                            "domain": "custom",
                            "pattern": intent_data.get("pattern", ""),
                            "requires_params": intent_data.get("requires_params", False),
                            "sample_phrases": intent_data.get("sample_phrases", []),
                        }

                    self.logger.info(f"Loaded {len(custom_intents)} custom intents")
                except Exception as e:
                    self.logger.error(f"Failed to load custom intents: {str(e)}")

        return intents

    def _compile_patterns(self):
        """Pre-compile regex patterns for faster matching."""
        # Implementation would go here
        pass  # Placeholder
