"""
Configuration related commands for the AMAUTA CLI.

This module provides commands for viewing and manipulating AMAUTA configuration.
"""

import json
import os
from typing import Any, Optional, Union

import typer
from rich.console import Console

from amauta_ai.config import ConfigService, ConfigSource

console = Console()


def format_value(value: Any) -> str:
    """Format a configuration value for display."""
    if isinstance(value, dict):
        return json.dumps(value, indent=2)
    elif isinstance(value, list):
        return json.dumps(value, indent=2)
    else:
        return str(value)


def format_source(source: Any) -> str:
    """Format a configuration source for display."""
    # Handle ConfigSource enum values
    if isinstance(source, ConfigSource):
        if source == ConfigSource.DEFAULT:
            return "default"
        elif source == ConfigSource.CONFIG_FILE:
            return "config file"
        elif source == ConfigSource.ENV_VARIABLES:
            return "environment"
        elif source == ConfigSource.CLI_ARGS:
            return "CLI arguments"
        elif source == ConfigSource.RUNTIME:
            return "runtime"

    # Handle string representations of ConfigSource
    source_str = str(source).upper()
    if "DEFAULT" in source_str:
        return "default"
    elif "CONFIG_FILE" in source_str:
        return "config file"
    elif "ENV" in source_str:
        return "environment"
    elif "CLI" in source_str:
        return "CLI arguments"
    elif "RUNTIME" in source_str:
        return "runtime"

    # Default case
    return "unknown"


config_group = typer.Typer(name="config", help="Manage AMAUTA configuration.")


@config_group.callback()
def config_callback() -> None:
    """Manage AMAUTA configuration."""
    pass


@config_group.command("get")
def get_config(
    key: Optional[str] = typer.Argument(None, help="Configuration key to get"),
    source: bool = typer.Option(
        False, help="Show the source of the configuration value"
    ),
) -> None:
    """
    Get configuration value(s).

    If KEY is provided, shows the value for that specific configuration key.
    If KEY is not provided, shows all configuration values.

    Examples:
        amauta config get
        amauta config get log_level
        amauta config get project.name
        amauta config get --source log_level
    """
    config_service = ConfigService()

    if key:
        # Get specific value
        value = config_service.get_value(key)
        if value is None:
            console.print(f"Configuration key '{key}' not found")
            return

        if source:
            value_source = config_service.get_override_source(key)
            console.print(
                f"{key} = {format_value(value)} (from {format_source(value_source)})"
            )
        else:
            console.print(f"{key} = {format_value(value)}")
    else:
        # Get all values
        config = config_service.get_config()
        if source:
            # Get a precedence report and display values with their sources
            report = config_service.get_precedence_report()
            for key, sources in report.items():
                active_source = next((s for s in sources if s["active"]), None)
                if active_source:
                    console.print(
                        f"{key} = {format_value(active_source['value'])} (from {format_source(active_source['source'])})"
                    )
        else:
            # Display all values in a structured format
            console.print(config.model_dump_json(indent=2))


@config_group.command("set")
def set_config(
    key: str = typer.Argument(..., help="Configuration key to set"),
    value: str = typer.Argument(..., help="Value to set"),
    temp: bool = typer.Option(
        False, help="Set value temporarily (won't persist to config file)"
    ),
) -> None:
    """
    Set configuration value.

    Sets a value for the specified configuration KEY.
    The VALUE is automatically converted to the appropriate type.

    If --temp is provided, the value is set only for the current session
    and won't be saved to the config file.

    Examples:
        amauta config set log_level DEBUG
        amauta config set project.name "My Project"
        amauta config set --temp analyzer.max_file_size_kb 2048
    """
    config_service = ConfigService()

    # Try to convert string value to appropriate type
    parsed_value: Union[bool, int, float, str]
    
    if value.lower() == "true":
        parsed_value = True
    elif value.lower() == "false":
        parsed_value = False
    elif value.isdigit():
        parsed_value = int(value)
    elif value.replace(".", "", 1).isdigit() and value.count(".") == 1:
        parsed_value = float(value)
    else:
        parsed_value = value

    # Set the value
    success = config_service.set_value(key, parsed_value, save=not temp)

    if success:
        source = "temporarily" if temp else "permanently"
        console.print(
            f"Value for '{key}' set {source} to: {format_value(parsed_value)}"
        )
    else:
        console.print(f"Failed to set value for '{key}'")


@config_group.command("reset")
def reset_config(
    key: Optional[str] = typer.Argument(None, help="Configuration key to reset"),
    reset_all: bool = typer.Option(
        False, "--all", help="Reset all configuration to defaults"
    ),
    confirm: bool = typer.Option(False, help="Skip confirmation prompt"),
) -> None:
    """
    Reset configuration to default values.

    If KEY is provided, resets only that specific configuration key.
    If --all is provided, resets all configuration to defaults.

    Examples:
        amauta config reset log_level
        amauta config reset --all
        amauta config reset --all --confirm
    """
    if not key and not reset_all:
        console.print(
            "Please provide a key to reset or use --all to reset all configuration"
        )
        return

    config_service = ConfigService()

    if reset_all:
        if not confirm and not typer.confirm(
            "Are you sure you want to reset ALL configuration to defaults?"
        ):
            console.print("Reset canceled")
            return

        config_service.reset_to_defaults(save=True)
        console.print("All configuration reset to defaults")
    else:
        # At this point, we know key is not None because of the earlier check
        assert key is not None, "Key must be provided if reset_all is False"
        
        original_value = config_service.get_value(key)
        if original_value is None:
            console.print(f"Configuration key '{key}' not found")
            return

        # Remove any runtime override for this key
        config_service.override_manager.remove_runtime_value(key)

        # Get default config and extract the default value
        default_config = config_service.get_default_config()
        default_dict = default_config.model_dump()

        # Navigate to the nested key
        parts = key.split(".")
        current = default_dict
        for part in parts[:-1]:
            if part in current and isinstance(current[part], dict):
                current = current[part]
            else:
                # Key doesn't exist in defaults or path is invalid
                console.print(f"Configuration key '{key}' not found in defaults")
                return

        # Get the default value for this key
        if parts[-1] in current:
            default_value = current[parts[-1]]

            # Set the value back to default
            config_service.set_value(key, default_value, save=True)
            console.print(
                f"Value for '{key}' reset to default: {format_value(default_value)}"
            )
        else:
            console.print(f"Configuration key '{key}' not found in defaults")


@config_group.command("init")
def init_config(
    force: bool = typer.Option(False, help="Overwrite existing config file")
) -> None:
    """
    Initialize a new configuration file.

    Creates a new .amautarc.yaml file with default settings in the current directory.

    Examples:
        amauta config init
        amauta config init --force
    """
    config_path = os.path.join(os.getcwd(), ".amautarc.yaml")

    if os.path.exists(config_path) and not force:
        console.print(f"Configuration file already exists at {config_path}")
        console.print("Use --force to overwrite")
        return

    config_service = ConfigService()
    default_config = config_service.get_default_config()

    config_service.save_config(default_config, config_path)
    console.print(f"Configuration file initialized at {config_path}")


@config_group.command("sources")
def show_sources(
    key: Optional[str] = typer.Argument(
        None, help="Configuration key to show sources for"
    )
) -> None:
    """
    Show all sources for a configuration value.

    If KEY is provided, shows all sources for that specific configuration key.
    If KEY is not provided, shows sources for all configuration values.

    Examples:
        amauta config sources
        amauta config sources log_level
    """
    config_service = ConfigService()
    report = config_service.get_precedence_report()

    if key:
        if key not in report:
            console.print(f"Configuration key '{key}' not found")
            return

        console.print(f"Sources for '{key}':")
        for source in report[key]:
            active_marker = "*" if source["active"] else " "
            console.print(
                f"  {active_marker} {format_source(source['source'])}: {format_value(source['value'])}"
            )
    else:
        # Display sources for all keys
        for key, sources in report.items():
            console.print(f"Sources for '{key}':")
            for source in sources:
                active_marker = "*" if source["active"] else " "
                console.print(
                    f"  {active_marker} {format_source(source['source'])}: {format_value(source['value'])}"
                )
            console.print("")


@config_group.command("export")
def export_config(
    output_path: str = typer.Argument(..., help="Path to save the configuration to"),
    format: str = typer.Option("yaml", help="Output format (yaml or json)"),
    include_comments: bool = typer.Option(
        True, help="Include helpful comments in the output file"
    ),
) -> None:
    """
    Export configuration to a file.

    Exports the current active configuration to the specified file.

    Examples:
        amauta config export config.yaml
        amauta config export config.json --format=json
        amauta config export config.yaml --no-include-comments
    """
    config_service = ConfigService()
    config = config_service.get_config()

    # Convert Pydantic model to dict with proper handling of enums
    config_dict = config.model_dump()

    # Convert path to absolute if it's not already
    output_path = os.path.abspath(output_path)

    # Create directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    # Determine format from extension if not specified
    if format == "yaml" and not (
        output_path.endswith(".yaml") or output_path.endswith(".yml")
    ):
        console.print(
            f"Warning: Saving YAML to file without .yaml/.yml extension: {output_path}"
        )
    elif format == "json" and not output_path.endswith(".json"):
        console.print(
            f"Warning: Saving JSON to file without .json extension: {output_path}"
        )

    try:
        if format.lower() == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                if include_comments:
                    f.write(
                        "// AMAUTA Configuration - Generated by 'amauta config export'\n"
                    )
                    f.write(
                        "// Do not edit this file directly unless you know what you're doing.\n"
                    )
                    f.write(
                        "// Use 'amauta config set' to modify configuration values.\n\n"
                    )
                json.dump(config_dict, f, indent=2)
        else:
            # Default to YAML
            import yaml

            # Add proper handling for custom types
            def represent_none(dumper: Any, _: Any) -> Any:
                return dumper.represent_scalar("tag:yaml.org,2002:null", "null")

            yaml.add_representer(type(None), represent_none)

            with open(output_path, "w", encoding="utf-8") as f:
                if include_comments:
                    f.write(
                        "# AMAUTA Configuration - Generated by 'amauta config export'\n"
                    )
                    f.write(
                        "# Do not edit this file directly unless you know what you're doing.\n"
                    )
                    f.write(
                        "# Use 'amauta config set' to modify configuration values.\n\n"
                    )
                yaml.dump(config_dict, f, default_flow_style=False)

        console.print(f"Configuration exported to {output_path}")

    except Exception as e:
        console.print(f"[red]Error exporting configuration: {str(e)}[/red]")


@config_group.command("import")
def import_config(
    input_path: str = typer.Argument(
        ..., help="Path to the configuration file to import"
    ),
    merge: bool = typer.Option(
        True, help="Merge with existing configuration instead of replacing it"
    ),
    save: bool = typer.Option(True, help="Save changes to the configuration file"),
) -> None:
    """
    Import configuration from a file.

    Imports configuration from the specified file and applies it to the current configuration.

    Examples:
        amauta config import config.yaml
        amauta config import config.json --no-merge
        amauta config import config.yaml --no-save
    """
    config_service = ConfigService()

    # Determine file format from extension
    file_format = "yaml"
    if input_path.endswith(".json"):
        file_format = "json"

    # Check if file exists
    if not os.path.exists(input_path):
        console.print(f"[red]Error: File not found: {input_path}[/red]")
        return

    try:
        # Load configuration from file
        if file_format == "json":
            with open(input_path, "r", encoding="utf-8") as f:
                import_data = json.load(f)
        else:
            # Default to YAML
            import yaml

            with open(input_path, "r", encoding="utf-8") as f:
                import_data = yaml.safe_load(f)

        if not isinstance(import_data, dict):
            console.print(
                f"[red]Error: Invalid configuration format in {input_path}[/red]"
            )
            return

        # Apply configuration
        if merge:
            # Merge with existing configuration
            success = config_service.merge_config(import_data, save=save)
            if success:
                console.print(f"Configuration from {input_path} merged successfully")
                if not save:
                    console.print("Note: Changes were not saved to disk (--no-save)")
            else:
                console.print(
                    f"[red]Error merging configuration from {input_path}[/red]"
                )
        else:
            # Replace existing configuration
            try:
                # Create a new configuration object from the imported data
                from amauta_ai.config.models import AmautarcConfig

                new_config = AmautarcConfig.model_validate(import_data)

                # Save it
                if save:
                    config_service.save_config(new_config)
                    console.print(f"Configuration replaced with {input_path}")
                else:
                    # Apply as runtime values
                    config_service.override_manager.reset()
                    config_service.override_manager.set_defaults(
                        config_service.get_default_config()
                    )
                    config_service.merge_config(import_data, save=False)
                    console.print(
                        f"Configuration replaced with {input_path} (not saved to disk)"
                    )
            except Exception as e:
                console.print(
                    f"[red]Error applying configuration from {input_path}: {str(e)}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error importing configuration: {str(e)}[/red]")
