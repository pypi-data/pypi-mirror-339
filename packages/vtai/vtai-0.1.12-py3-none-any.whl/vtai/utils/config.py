"""
Configuration utilities for the VT.ai application.
"""

import importlib.resources
import logging
import os
import tempfile
from typing import Tuple

# Set TOKENIZERS_PARALLELISM explicitly at module level before any imports
# This prevents the HuggingFace tokenizers warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import dotenv
import httpx
import json
import litellm
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

# Update imports to use vtai namespace
from vtai.router.constants import RouteLayer
from vtai.utils import constants as const

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("vt.ai")

# Create temporary directory for TTS audio files
temp_dir = tempfile.TemporaryDirectory()

# List of allowed mime types
allowed_mime = [
    "text/csv",
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
    "audio/mpeg",
    "audio/mp3",
    "audio/wav",
]


def load_api_keys() -> None:
    """
    Load API keys from environment variables and set them in os.environ.
    Prioritizes user-specific .env file before falling back to project .env
    Logs which keys were successfully loaded to help with debugging.
    """
    # First try to load from user config directory
    user_config_dir = os.path.expanduser("~/.config/vtai")
    user_env_path = os.path.join(user_config_dir, ".env")

    env_loaded = False

    # Try user config first
    if os.path.exists(user_env_path):
        load_dotenv(dotenv_path=user_env_path, override=True)
        logger.info(f"Loaded API keys from user config: {user_env_path}")
        env_loaded = True

    # Fall back to project .env if user config not found or as additional source
    project_env_path = dotenv.find_dotenv()
    if project_env_path:
        load_dotenv(
            dotenv_path=project_env_path, override=False
        )  # Don't override user config
        if not env_loaded:
            logger.info(f"Loaded API keys from project .env: {project_env_path}")
            env_loaded = True

    # Get API keys from environment
    api_keys = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "COHERE_API_KEY": os.getenv("COHERE_API_KEY"),
        "HUGGINGFACE_API_KEY": os.getenv("HUGGINGFACE_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "MISTRAL_API_KEY": os.getenv("MISTRAL_API_KEY"),
        "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY"),
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
        "LM_STUDIO_API_BASE": os.getenv("LM_STUDIO_API_BASE"),
    }

    # Log which keys are loaded
    loaded_keys = [key for key, value in api_keys.items() if value]
    logger.info(f"Loaded API keys: {', '.join(loaded_keys)}")


def create_openai_clients() -> Tuple[OpenAI, AsyncOpenAI]:
    """
    Create OpenAI clients with optimized connection settings.

    Returns:
        Tuple of (sync_client, async_client)
    """
    # Configure timeout settings for better connection handling
    timeout_settings = httpx.Timeout(
        connect=10.0,  # Connection timeout
        read=300.0,  # Read timeout for longer operations
        write=60.0,  # Write timeout
        pool=10.0,  # Connection pool timeout
    )

    # Create synchronous client with custom timeout
    sync_client = OpenAI(
        timeout=timeout_settings,
        max_retries=3,  # Increase retries to handle transient errors
        http_client=httpx.Client(timeout=timeout_settings),
    )

    # Create asynchronous client with custom timeout
    async_client = AsyncOpenAI(
        timeout=timeout_settings,
        max_retries=3,
        http_client=httpx.AsyncClient(
            timeout=timeout_settings,
            limits=httpx.Limits(
                max_connections=100, max_keepalive_connections=20, keepalive_expiry=30.0
            ),
        ),
    )

    return sync_client, async_client


def initialize_app() -> Tuple[RouteLayer, str, OpenAI, AsyncOpenAI]:
    """
    Initialize the application configuration.

    Returns:
        Tuple of (route_layer, assistant_id, openai_client, async_openai_client)
    """
    # Load API keys
    load_api_keys()

    # Model alias map for litellm
    litellm.model_alias_map = const.MODEL_ALIAS_MAP

    # Configure litellm for better timeout handling
    litellm.request_timeout = 60  # 60 seconds timeout

    # Load semantic router layer from JSON file - use proper path for installed package
    from semantic_router import Route
    from semantic_router.encoders import FastEmbedEncoder

    # Set the default encoder explicitly to disable any potential fallback to OpenAIEncoder
    # Create the FastEmbedEncoder instance with explicit model specification
    model_name = "BAAI/bge-small-en-v1.5"
    encoder = FastEmbedEncoder(model_name=model_name)

    # Attempt to load routes with proper package-aware path handling
    routes = []
    try:
        # Try to load from package resources - this works for installed packages
        layers_json_path = None
        try:
            # For Python 3.9+
            layers_json_path = importlib.resources.files("vtai.router").joinpath("layers.json")
        except (ImportError, AttributeError):
            # Fallback for older Python versions
            try:
                with importlib.resources.path("vtai.router", "layers.json") as path:
                    layers_json_path = path
            except (ImportError, AttributeError):
                layers_json_path = None

        # If we found a path, try to open it
        if layers_json_path:
            try:
                with open(layers_json_path, "r") as f:
                    router_json = json.load(f)
                    
                    # Create routes from the JSON data
                    for route_data in router_json["routes"]:
                        route_name = route_data["name"]
                        route_utterances = route_data["utterances"]

                        # Create Route object - passing the required utterances field and our encoder
                        route = Route(
                            name=route_name,
                            utterances=route_utterances,
                            encoder=encoder,  # Pass the same encoder instance to each route
                        )
                        routes.append(route)
                        
                logger.info(f"Loaded routes from package resource: {layers_json_path}")
            except Exception as e:
                logger.warning(f"Error reading layers.json from path {layers_json_path}: {e}")

    except Exception as e:
        logger.warning(f"Error loading routes from package resources: {e}")

    # If routes is still empty, try with a direct path as last resort 
    if not routes:
        try:
            # Try relative paths that might work in development
            possible_paths = [
                "./vtai/router/layers.json",  # From project root
                "../router/layers.json",      # Relative to utils directory
                "vtai/router/layers.json",    # Alternative from project root
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, "r") as f:
                        router_json = json.load(f)
                        
                        # Create routes from the JSON data
                        for route_data in router_json["routes"]:
                            route_name = route_data["name"]
                            route_utterances = route_data["utterances"]

                            # Create Route object
                            route = Route(
                                name=route_name,
                                utterances=route_utterances,
                                encoder=encoder,
                            )
                            routes.append(route)
                        
                    logger.info(f"Loaded routes from direct path: {path}")
                    break
        except Exception as e:
            logger.error(f"Failed to load routes from any path: {e}")

    # Create RouteLayer with the routes we found (or empty list if all efforts failed)
    route_layer = RouteLayer(routes=routes, encoder=encoder)

    # Get assistant ID
    assistant_id = os.environ.get("ASSISTANT_ID")

    # Initialize OpenAI clients
    openai_client, async_openai_client = create_openai_clients()

    return route_layer, assistant_id, openai_client, async_openai_client
