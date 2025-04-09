"""Utilities around Pydantic settings."""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, TypeVar

from pydantic import SecretStr, ValidationError, fields
from pydantic_settings import BaseSettings
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from starbridge import __project_name__
from starbridge.utils.console import console
from starbridge.utils.di import locate_subclasses

T = TypeVar("T", bound=BaseSettings)

logger = logging.getLogger(__name__)


def load_settings(settings_class: type[T]) -> T:
    """
    Load settings with error handling and nice formatting.

    Args:
        settings_class: The Pydantic settings class to instantiate

    Returns:
        (T): Instance of the settings class

    Raises:
        SystemExit: If settings validation fails

    """
    try:
        return settings_class()
    except ValidationError as e:
        errors = json.loads(e.json())
        text = Text()
        text.append(
            "Validation error(s): \n\n",
            style="debug",
        )

        prefix = settings_class.model_config.get("env_prefix", "")
        for error in errors:
            env_var = f"{prefix}{error['loc'][0]}".upper()
            logger.fatal(f"Configuration invalid! {env_var}: {error['msg']}")
            text.append(f"• {env_var}", style="yellow bold")
            text.append(f": {error['msg']}\n")

        text.append(
            "\nCheck settings defined in the process environment and in file ",
            style="info",
        )
        env_file = str(settings_class.model_config.get("env_file", ".env") or ".env")
        text.append(
            str(Path(__file__).parent.parent.parent.parent / env_file),
            style="bold blue underline",
        )

        console.print(
            Panel(
                text,
                title="Configuration invalid!",
                border_style="error",
            ),
        )
        sys.exit(78)


def get_starbridge_env() -> dict[str, str]:
    """
    Get all environment variables prefixed with the project name.

    Returns:
        dict[str, str]: Dictionary of environment variables.

    """
    return {k: v for k, v in os.environ.items() if k.startswith(__project_name__.upper())}


def prompt_for_env() -> dict[str, Any]:
    """
    Collect settings from user input for all BaseSettings subclasses.

    Returns:
        dict[str, Any]: Dictionary of collected settings values.

    """
    all_values = {}
    for settings_set in locate_subclasses(BaseSettings):
        settings = _get_settings_instance(settings_set)
        all_values.update(_collect_settings_values(settings))

    return {key: _transform_value(value) for key, value in all_values.items()}


def _get_field_description(field_name: str, field: fields.FieldInfo) -> str:
    """
    Generate description for a field with optional example.

    Args:
        field_name: Name of the field.
        field: Field instance.

    Returns:
        str: Generated description string.

    """
    description = field.description or field_name
    example = field.examples[0] if field.examples else None
    return f"{description} (e.g. {example})" if example else description


def _get_settings_instance(settings_set: type[BaseSettings]) -> BaseSettings:
    """
    Get settings instance with fallback to model_construct.

    Args:
        settings_set: Settings class to instantiate.

    Returns:
        BaseSettings: Instance of settings.

    """
    try:
        return settings_set()
    except ValidationError:
        return settings_set.model_construct()


def _transform_value(value: type[Any]) -> str:
    """
    Transform a value to its string representation.

    Args:
        value: Value to transform.

    Returns:
        str: String representation of the value.

    """
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, SecretStr):
        return value.get_secret_value()
    return str(value)


def _get_default_value(
    settings: BaseSettings,
    field_name: str,
    is_bool: bool,
) -> str | None:
    """
    Get the default value for a field.

    Args:
        settings: Settings instance.
        field_name: Name of the field.
        is_bool: Whether the field is boolean.

    Returns:
        str | None: Default value as string or None if not found.

    """
    default_value = getattr(settings, field_name, None)
    if is_bool:
        return "1" if default_value else "0"
    if default_value and hasattr(default_value, "get_secret_value"):
        return default_value.get_secret_value()
    return str(default_value) if default_value else None


def _prompt_for_field_value(
    settings: BaseSettings,
    field_name: str,
    description: str,
    prompt_default: str | None,
    is_bool: bool,
) -> str | None:
    """
    Prompt for a field value with validation.

    Args:
        settings: Settings instance to validate against.
        field_name: Name of the field being prompted.
        description: Field description to show.
        prompt_default: Default value to show in prompt.
        is_bool: Whether the field is boolean.

    Returns:
        str | None: Entered value or None if skipped.

    """
    while True:
        value = Prompt.ask(
            description,
            default=prompt_default,
            password=False,
            choices=["0", "1"] if is_bool else None,
        )
        try:
            settings.__pydantic_validator__.validate_assignment(
                settings.model_construct(),
                field_name,
                value,
            )
            return value
        except ValidationError as e:
            console.print(f"[red]{e.errors()[0]['msg']}[/red]")


def _collect_settings_values(settings: BaseSettings) -> dict[str, Any]:
    """
    Collect values for a single settings instance.

    Args:
        settings: Settings instance to collect values for.

    Returns:
        dict[str, Any]: Dictionary of collected values.

    """
    field_prefix = settings.model_config.get("env_prefix", "")
    values = {}

    for field_name, field in settings.model_fields.items():
        is_bool = field.annotation is bool
        description = _get_field_description(field_name, field)
        prompt_default = _get_default_value(settings, field_name, is_bool)
        value = _prompt_for_field_value(
            settings,
            field_name,
            description,
            prompt_default,
            is_bool,
        )
        key = f"{field_prefix}{field_name.upper()}"
        values[key] = value

    return values
