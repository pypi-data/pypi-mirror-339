#!/usr/bin/env python3
"""
EcoCycle CLI - Command line interface for the EcoCycle program
"""

import argparse
import requests
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from colorama import Fore, Back, Style

    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

from ecocycle import __version__, main_program
from ecocycle.main import (
    clear_screen,
    get_weather_forecast,
    get_user_stats_from_sheets,
    get_all_user_stats_from_sheets,
    check_headers
)

# Setup logger
logger = logging.getLogger('ecocycle.cli')

# Constants
VERSION = __version__
CONFIG_DIR = os.path.expanduser("~/.ecocycle")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
LOG_DIR = os.path.join(CONFIG_DIR, "logs")
DATA_DIR = os.path.join(CONFIG_DIR, "data")
REPORTS_DIR = os.path.join(CONFIG_DIR, "reports")

class Colors:
    """
    ANSI color codes for terminal output formatting.
    These are used when COLORAMA_AVAILABLE is False.
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def ensure_dir_exists(directory):
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory (str): Path to the directory

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False


def supports_color():
    """
    Check if the current terminal supports color output.

    Returns:
        bool: True if color is supported, False otherwise
    """
    # Return True if we have colorama
    if COLORAMA_AVAILABLE:
        return True

    # Otherwise, try to determine if the terminal supports colors
    plat = sys.platform
    supported_platform = plat != 'win32' or 'ANSICON' in os.environ

    # isatty is not always implemented, so we use this fallback
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

    if not supported_platform or not is_a_tty:
        return False

    return True


use_colors = supports_color()


def colorize(text, color, bold=False, underline=False):
    """
    Colorize text for terminal output.

    Args:
        text (str): Text to colorize
        color (str): Color to use
        bold (bool): Whether to make the text bold
        underline (bool): Whether to underline the text

    Returns:
        str: Colorized text
    """
    if not use_colors:
        return text

    result = text

    if COLORAMA_AVAILABLE:
        color_map = {
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
            'header': Fore.MAGENTA
        }

        if color.lower() in color_map:
            result = f"{color_map[color.lower()]}{result}{Style.RESET_ALL}"
        if bold:
            result = f"{Style.BRIGHT}{result}"
        # Colorama doesn't have underline, so we use the ANSI code
        if underline:
            result = f"\033[4m{result}\033[0m"
    else:
        color_map = {
            'red': Colors.RED,
            'green': Colors.GREEN,
            'yellow': Colors.YELLOW,
            'blue': Colors.BLUE,
            'header': Colors.HEADER,
        }

        if color.lower() in color_map:
            result = f"{color_map[color.lower()]}{result}{Colors.ENDC}"
        if bold:
            result = f"{Colors.BOLD}{result}{Colors.ENDC}"
        if underline:
            result = f"{Colors.UNDERLINE}{result}{Colors.ENDC}"

    return result


def print_banner():
    """Print the EcoCycle banner, adapting to terminal width."""
    import shutil

    # Get terminal size
    terminal_width, _ = shutil.get_terminal_size((80, 20))  # Default to 80x20 if detection fails

    # Define the full ECOCYCLE ASCII art
    ecocycle_ascii = [
        "███████╗ ██████╗ ██████╗  ██████╗██╗   ██╗ ██████╗██╗     ███████╗",
        "██╔════╝██╔════╝██╔═══██╗██╔════╝╚██╗ ██╔╝██╔════╝██║     ██╔════╝",
        "█████╗  ██║     ██║   ██║██║      ╚████╔╝ ██║     ██║     █████╗  ",
        "██╔══╝  ██║     ██║   ██║██║       ╚██╔╝  ██║     ██║     ██╔══╝  ",
        "███████╗╚██████╗╚██████╔╝╚██████╗   ██║   ╚██████╗███████╗███████╗",
        "╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝╚══════╝╚══════╝"
    ]

    # Calculate the width of the ASCII art
    ascii_width = len(ecocycle_ascii[0])

    # Determine if we need to use the full banner or a simplified version
    use_full_banner = terminal_width >= ascii_width + 10  # +10 for padding and borders

    if use_full_banner:
        # Calculate banner width with some padding
        banner_width = min(terminal_width - 2, ascii_width + 8)

        # Create top and bottom borders
        top_border = "╔" + "═" * (banner_width - 2) + "╗"
        bottom_border = "╚" + "═" * (banner_width - 2) + "╝"
        empty_line = "║" + " " * (banner_width - 2) + "║"

        # Print the banner with the full ASCII art
        print(colorize(top_border, Colors.GREEN, bold=True))
        print(colorize(empty_line, Colors.GREEN, bold=True))

        # Print each line of the ASCII art, centered
        for line in ecocycle_ascii:
            padding = (banner_width - 2 - len(line)) // 2
            formatted_line = "║" + " " * padding + line + " " * (banner_width - 2 - len(line) - padding) + "║"
            print(colorize(formatted_line, Colors.GREEN, bold=True))

        # Add the tagline, centered
        tagline = "Cycle Into A Greener Tomorrow"
        padding = (banner_width - 2 - len(tagline)) // 2
        tagline_line = "║" + " " * padding + tagline + " " * (banner_width - 2 - len(tagline) - padding) + "║"

        print(colorize(empty_line, Colors.GREEN, bold=True))
        print(colorize(tagline_line, Colors.GREEN, bold=True))
        print(colorize(empty_line, Colors.GREEN, bold=True))
        print(colorize(bottom_border, Colors.GREEN, bold=True))
    else:
        # For narrow terminals, use a simplified banner
        simplified_banner = f"{'═' * (terminal_width - 2)}\n  ECOCYCLE: Cycle Into A Greener Tomorrow\n{'═' * (terminal_width - 2)}"
        print(colorize(simplified_banner, Colors.GREEN, bold=True))

    # Print version and help information
    version_info = f"Version: {VERSION}"
    help_info = "Run 'ecocycle --help' for available commands"

    # Make sure these lines don't exceed the terminal width
    if len(version_info) > terminal_width:
        version_info = version_info[:terminal_width - 3] + "..."
    if len(help_info) > terminal_width:
        help_info = help_info[:terminal_width - 3] + "..."

    print(colorize(version_info, Colors.BLUE))
    print(colorize(help_info, Colors.YELLOW))
    print()


def load_config():
    """
    Load the configuration file.

    Returns:
        dict: Configuration data
    """
    # Default configuration
    default_config = {
        "user_profile": "",
        "google_sheets_id": "",
        "api_key": "",
        "debug_mode": False,
        "color_output": True,
        "auto_update_check": True,
        "last_update_check": "",
        "last_backup": ""
    }

    # Ensure config directory exists
    ensure_dir_exists(CONFIG_DIR)

    # Try to load existing config
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with default config to add any missing keys
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")

    # Return default config if loading fails
    return default_config


def save_config(config):
    """
    Save the configuration file.

    Args:
        config (dict): Configuration data

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        ensure_dir_exists(CONFIG_DIR)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Failed to save config: {e}")
        return False


def print_section(title):
    """
    Print a section title.

    Args:
        title (str): Section title
    """
    width = min(os.get_terminal_size().columns - 4, 80)
    print()
    print(colorize("╔" + "═" * width + "╗", 'blue'))
    print(colorize("║ " + title.ljust(width-1) + "║", 'blue', bold=True))
    print(colorize("╚" + "═" * width + "╝", 'blue'))


def print_key_value(key, value, color_key='yellow', color_value='white', indent=2):
    """
    Print a key-value pair.

    Args:
        key (str): Key to print
        value (str): Value to print
        color_key (str): Color for the key
        color_value (str): Color for the value
        indent (int): Indentation level
    """
    spaces = ' ' * indent
    print(f"{spaces}{colorize(key, color_key)}: {colorize(str(value), color_value)}")


def show_config():
    """Display the current configuration."""
    config = load_config()

    print_banner()
    print_section("Current Configuration")

    # User profile
    print_key_value("User Profile", config.get("user_profile") or "Not set")

    # Google Sheets integration
    sheets_id = config.get("google_sheets_id") or "Not configured"
    if len(sheets_id) > 30 and sheets_id != "Not configured":
        sheets_id = sheets_id[:15] + "..." + sheets_id[-15:]
    print_key_value("Google Sheets ID", sheets_id)

    # API key (masked)
    api_key = config.get("api_key")
    if api_key:
        masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else "****"
        print_key_value("API Key", masked_key)
    else:
        print_key_value("API Key", "Not set")

    # Other settings
    print_key_value("Debug Mode", "Enabled" if config.get("debug_mode") else "Disabled")
    print_key_value("Color Output", "Enabled" if config.get("color_output", True) else "Disabled")
    print_key_value("Auto Update Check", "Enabled" if config.get("auto_update_check", True) else "Disabled")

    # Dates
    last_update = config.get("last_update_check")
    if last_update:
        print_key_value("Last Update Check", last_update)

    last_backup = config.get("last_backup")
    if last_backup:
        print_key_value("Last Backup", last_backup)

    # Data directories
    print()
    print_section("Data Directories")
    print_key_value("Config Directory", CONFIG_DIR)
    print_key_value("Logs Directory", LOG_DIR)
    print_key_value("Data Directory", DATA_DIR)
    print_key_value("Reports Directory", REPORTS_DIR)


def config_command(args):
    """
    Handle configuration commands.

    Args:
        args (argparse.Namespace): Command line arguments
    """
    config = load_config()

    if args.action == 'show':
        show_config()
        return

    if args.action == 'set':
        if len(args.key) < 1 or len(args.value) < 1:
            print(colorize("Error: Both key and value are required for 'set' action", 'red'))
            return

        key = args.key
        value = args.value

        # Handle boolean values
        if value.lower() in ('true', 'yes', 'on', 'enable', 'enabled'):
            value = True
        elif value.lower() in ('false', 'no', 'off', 'disable', 'disabled'):
            value = False

        # Set the configuration value
        config[key] = value
        if save_config(config):
            print(colorize(f"Configuration updated: {key} = {value}", 'green'))
        else:
            print(colorize("Failed to save configuration", 'red'))

    if args.action == 'reset':
        key = args.key
        if key == 'all':
            # Reset all configuration
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
            print(colorize("Configuration reset to defaults", 'green'))
        else:
            # Reset specific key
            if key in config:
                del config[key]
                if save_config(config):
                    print(colorize(f"Reset configuration value: {key}", 'green'))
                else:
                    print(colorize("Failed to save configuration", 'red'))
            else:
                print(colorize(f"Unknown configuration key: {key}", 'yellow'))


def run_command(args):
    """Run the main EcoCycle program."""
    print_banner()

    config = load_config()

    # Set debug mode based on config or command line args
    debug_mode = args.debug or config.get("debug_mode", False)

    # Configure logging
    log_level = logging.DEBUG if debug_mode else logging.INFO

    ensure_dir_exists(LOG_DIR)
    log_file = os.path.join(LOG_DIR, f"ecocycle_{datetime.now().strftime('%Y%m%d')}.log")

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler() if debug_mode else logging.NullHandler()
        ]
    )

    logger.info("Starting EcoCycle main program")

    try:
        # Run the main program with any provided user profile
        profile = args.profile or config.get("user_profile", "")
        if profile:
            print(colorize(f"Using profile: {profile}", 'blue'))

        # Check for updates if enabled
        if config.get("auto_update_check", True):
            should_check = True
            last_check = config.get("last_update_check", "")

            if last_check:
                try:
                    last_check_date = datetime.strptime(last_check, "%Y-%m-%d %H:%M:%S")
                    time_diff = datetime.now() - last_check_date
                    # Only check once per day
                    if time_diff.days < 1:
                        should_check = False
                except ValueError:
                    pass

            if should_check:
                print(colorize("Checking for updates...", 'blue'))
                check_updates(silent=True)

                # Update last check time
                config["last_update_check"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_config(config)

        # Run the main program
        main_program()
    except KeyboardInterrupt:
        print(colorize("\nProgram terminated by user", 'yellow'))
    except Exception as e:
        logger.error(f"Error in main program: {e}", exc_info=True)
        print(colorize(f"An error occurred: {e}", 'red'))
        if debug_mode:
            import traceback
            traceback.print_exc()

    logger.info("EcoCycle main program completed")


def stats_command(args):
    """
    Display user statistics from Google Sheets.

    Args:
        args (argparse.Namespace): Command line arguments
    """
    print_banner()
    print_section("User Statistics")

    config = load_config()

    # Check if Google Sheets ID is configured
    sheets_id = config.get("google_sheets_id")
    if not sheets_id:
        print(colorize("Google Sheets ID not configured. Please set it with:", 'red'))
        print(colorize("  ecocycle config --set google_sheets_id YOUR_SHEET_ID", 'yellow'))
        return

    # Get user profile
    profile = args.profile or config.get("user_profile")

    try:
        if profile and not args.all:
            # Get stats for a specific user
            print(colorize(f"Loading statistics for user: {profile}", 'blue'))
            stats = get_user_stats_from_sheets(profile)

            if not stats:
                print(colorize(f"No statistics found for user: {profile}", 'yellow'))
                return

            # Display user stats
            print()
            print_key_value("Total Distance", f"{stats.get('total_distance', 0):.2f} km")
            print_key_value("Total CO2 Saved", f"{stats.get('co2_saved', 0):.2f} kg")
            print_key_value("Total Calories Burned", f"{stats.get('calories_burned', 0):.0f} kcal")
            print_key_value("Pedal Points", f"{stats.get('pedal_points', 0)}")
            print_key_value("Rides Completed", f"{stats.get('rides_completed', 0)}")

            # Recent activity
            if 'recent_activity' in stats and stats['recent_activity']:
                print()
                print_section("Recent Activity")
                for i, activity in enumerate(stats['recent_activity'][:5]):
                    print(colorize(f"Ride {i+1}:", 'blue', bold=True))
                    print_key_value("Date", activity.get('date', 'Unknown'), indent=4)
                    print_key_value("Distance", f"{activity.get('distance', 0):.2f} km", indent=4)
                    print_key_value("CO2 Saved", f"{activity.get('co2_saved', 0):.2f} kg", indent=4)
                    print_key_value("Calories", f"{activity.get('calories', 0):.0f} kcal", indent=4)
                    print()

        else:
            # Get stats for all users
            print(colorize("Loading statistics for all users...", 'blue'))

            # Check if headers are correct first
            if not check_headers():
                print(colorize("Google Sheets headers not properly set up", 'red'))
                return

            all_stats = get_all_user_stats_from_sheets()

            if not all_stats:
                print(colorize("No statistics found", 'yellow'))
                return

            # Display summary stats
            total_users = len(all_stats)
            total_distance = sum(user.get('total_distance', 0) for user in all_stats.values())
            total_co2 = sum(user.get('co2_saved', 0) for user in all_stats.values())
            total_calories = sum(user.get('calories_burned', 0) for user in all_stats.values())
            total_rides = sum(user.get('rides_completed', 0) for user in all_stats.values())

            print_section("Summary Statistics")
            print_key_value("Total Users", total_users)
            print_key_value("Total Distance", f"{total_distance:.2f} km")
            print_key_value("Total CO2 Saved", f"{total_co2:.2f} kg")
            print_key_value("Total Calories Burned", f"{total_calories:.0f} kcal")
            print_key_value("Total Rides Completed", total_rides)

            if args.detail:
                # Display detailed user stats
                print()
                print_section("User Details")

                # Sort users by total distance
                sorted_users = sorted(
                    all_stats.items(),
                    key=lambda x: x[1].get('total_distance', 0),
                    reverse=True
                )

                for i, (username, stats) in enumerate(sorted_users[:10]):
                    print(colorize(f"{i+1}. {username}", 'blue', bold=True))
                    print_key_value("Distance", f"{stats.get('total_distance', 0):.2f} km", indent=4)
                    print_key_value("CO2 Saved", f"{stats.get('co2_saved', 0):.2f} kg", indent=4)
                    print_key_value("Calories", f"{stats.get('calories_burned', 0):.0f} kcal", indent=4)
                    print_key_value("Pedal Points", f"{stats.get('pedal_points', 0)}", indent=4)
                    print_key_value("Rides", f"{stats.get('rides_completed', 0)}", indent=4)
                    print()

                if len(sorted_users) > 10:
                    print(colorize(f"... and {len(sorted_users) - 10} more users", 'yellow'))

    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}", exc_info=True)
        print(colorize(f"Error retrieving statistics: {e}", 'red'))


def weather_command(args):
    """
    Display weather forecast for cycling.

    Args:
        args (argparse.Namespace): Command line arguments
    """
    print_banner()
    print_section("Weather Forecast for Cycling")

    config = load_config()
    api_key = config.get("api_key")

    if not api_key:
        print(colorize("Weather API key not configured. Please set it with:", 'red'))
        print(colorize("  ecocycle config --set api_key YOUR_API_KEY", 'yellow'))
        return

    location = args.location
    if not location:
        print(colorize("Please provide a location:", 'yellow'))
        location = input("> ")

    if not location:
        print(colorize("No location provided", 'red'))
        return

    try:
        print(colorize(f"Getting weather forecast for {location}...", 'blue'))

        # Get weather forecast
        forecast = get_weather_forecast(location, api_key)

        if not forecast:
            print(colorize(f"Could not retrieve weather data for {location}", 'red'))
            return

        # Display current weather
        current = forecast.get('current', {})
        print()
        print_key_value("Current Temperature", f"{current.get('temp_c', 'N/A')}°C")
        print_key_value("Condition", current.get('condition', {}).get('text', 'N/A'))
        print_key_value("Wind", f"{current.get('wind_kph', 'N/A')} km/h {current.get('wind_dir', '')}")
        print_key_value("Humidity", f"{current.get('humidity', 'N/A')}%")
        print_key_value("Feels Like", f"{current.get('feelslike_c', 'N/A')}°C")
        print_key_value("Precipitation", f"{current.get('precip_mm', 'N/A')} mm")
        print_key_value("UV Index", current.get('uv', 'N/A'))

        # Cycling recommendation
        print()
        print_section("Cycling Recommendation")

        # Simple cycling recommendation logic
        temp = current.get('temp_c', 0)
        precip = current.get('precip_mm', 0)
        wind = current.get('wind_kph', 0)

        if precip > 5:
            recommendation = "Not recommended - Heavy rain"
            color = 'red'
        elif precip > 1:
            recommendation = "Challenging - Light rain, bring rain gear"
            color = 'yellow'
        elif wind > 30:
            recommendation = "Challenging - High winds"
            color = 'yellow'
        elif temp < 5:
            recommendation = "Cold - Dress warmly"
            color = 'yellow'
        elif temp > 35:
            recommendation = "Very hot - Stay hydrated and avoid midday"
            color = 'yellow'
        else:
            recommendation = "Good conditions for cycling"
            color = 'green'

        print(colorize(recommendation, color, bold=True))

        # Display forecast for next 3 days
        print()
        print_section("3-Day Forecast")

        forecasts = forecast.get('forecast', {}).get('forecastday', [])
        for day in forecasts[:3]:
            date = day.get('date', 'Unknown')
            day_data = day.get('day', {})

            print(colorize(date, 'blue', bold=True))
            print_key_value("Max Temperature", f"{day_data.get('maxtemp_c', 'N/A')}°C", indent=4)
            print_key_value("Min Temperature", f"{day_data.get('mintemp_c', 'N/A')}°C", indent=4)
            print_key_value("Condition", day_data.get('condition', {}).get('text', 'N/A'), indent=4)
            print_key_value("Chance of Rain", f"{day_data.get('daily_chance_of_rain', 'N/A')}%", indent=4)
            print_key_value("Max Wind", f"{day_data.get('maxwind_kph', 'N/A')} km/h", indent=4)
            print()

    except Exception as e:
        logger.error(f"Error retrieving weather forecast: {e}", exc_info=True)
        print(colorize(f"Error retrieving weather forecast: {e}", 'red'))


def export_command(args):
    """
    Export statistics to a file.

    Args:
        args (argparse.Namespace): Command line arguments
    """
    print_banner()
    print_section("Export Statistics")

    config = load_config()

    # Check if Google Sheets ID is configured
    sheets_id = config.get("google_sheets_id")
    if not sheets_id:
        print(colorize("Google Sheets ID not configured. Please set it with:", 'red'))
        print(colorize("  ecocycle config --set google_sheets_id YOUR_SHEET_ID", 'yellow'))
        return

    # Get user profile
    profile = args.profile or config.get("user_profile")

    # Create reports directory
    ensure_dir_exists(REPORTS_DIR)

    # Format for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        if profile and not args.all:
            # Export stats for a specific user
            print(colorize(f"Exporting statistics for user: {profile}", 'blue'))
            stats = get_user_stats_from_sheets(profile)

            if not stats:
                print(colorize(f"No statistics found for user: {profile}", 'yellow'))
                return

            # Create filename
            filename = os.path.join(REPORTS_DIR, f"{profile.lower().replace(' ', '_')}_stats_{timestamp}.json")

            # Save to file
            with open(filename, 'w') as f:
                json.dump(stats, f, indent=4)

            print(colorize(f"Statistics exported to: {filename}", 'green'))

        else:
            # Export stats for all users
            print(colorize("Exporting statistics for all users...", 'blue'))

            # Check if headers are correct first
            if not check_headers():
                print(colorize("Google Sheets headers not properly set up", 'red'))
                return

            all_stats = get_all_user_stats_from_sheets()

            if not all_stats:
                print(colorize("No statistics found", 'yellow'))
                return

            # Create filename
            filename = os.path.join(REPORTS_DIR, f"all_user_stats_{timestamp}.json")

            # Save to file
            with open(filename, 'w') as f:
                json.dump(all_stats, f, indent=4)

            print(colorize(f"Statistics exported to: {filename}", 'green'))

            # Create a summary CSV file if requested
            if args.format == 'csv':
                csv_filename = os.path.join(REPORTS_DIR, f"user_summary_{timestamp}.csv")

                with open(csv_filename, 'w') as f:
                    # Write header
                    f.write("Username,Total Distance (km),CO2 Saved (kg),Calories Burned,Pedal Points,Rides Completed\n")

                    # Write data for each user
                    for username, stats in all_stats.items():
                        f.write(f"{username},{stats.get('total_distance', 0):.2f},{stats.get('co2_saved', 0):.2f},{stats.get('calories_burned', 0):.0f},{stats.get('pedal_points', 0)},{stats.get('rides_completed', 0)}\n")

                print(colorize(f"Summary CSV exported to: {csv_filename}", 'green'))

    except Exception as e:
        logger.error(f"Error exporting statistics: {e}", exc_info=True)
        print(colorize(f"Error exporting statistics: {e}", 'red'))


def user_guide(args=None):
    """Display the user guide."""
    print_banner()
    print_section("EcoCycle User Guide")

    guide = """
EcoCycle helps you track your cycling activities, calculate environmental
benefits, and manage user data through Google Sheets integration.

Available Commands:
------------------

* run                  Run the main EcoCycle program
* stats                Show user statistics
* weather              Display weather forecast for cycling
* config               View or modify configuration
* export               Export statistics to a file
* update               Check for updates
* help                 Display this user guide

Examples:
--------

* ecocycle run                     Start the main program
* ecocycle run --profile "John"    Start with a specific user profile
* ecocycle stats                   Show statistics for current user
* ecocycle stats --all             Show statistics for all users
* ecocycle weather "New York"      Show weather forecast for New York
* ecocycle config --list           View current configuration
* ecocycle config --set key value  Set a configuration value
* ecocycle export --all            Export all user statistics to file

For more information on a specific command, use:
ecocycle COMMAND --help

Visit https://rebrand.ly/ecocycle for full documentation.
    """

    print(guide)


def check_updates(silent=False):
    """
    Check for updates to the EcoCycle package.

    Args:
        silent (bool): If True, only show output if updates are available
    """
    if not silent:
        print_banner()
        print_section("Update Check")
        print(colorize("Checking for updates...", 'blue'))

    try:
        import requests
        from packaging import version

        # Get the latest version from PyPI
        response = requests.get("https://pypi.org/pypi/ecocycle/json", timeout=5)
        data = response.json()
        latest_version = data["info"]["version"]

        # Compare with current version
        current_version = VERSION

        if version.parse(latest_version) > version.parse(current_version):
            print(colorize(f"Update available: {current_version} → {latest_version}", 'yellow', bold=True))
            print(colorize("To update, run: pip install --upgrade ecocycle", 'green'))

            # Check release notes
            releases = data.get("releases", {})
            if latest_version in releases:
                print()
                print_section("Release Notes")
                # Try to get release notes from the description or summary
                notes = data["info"].get("summary", "No notes available")
                print(colorize(notes, 'blue'))
            return True
        else:
            if not silent:
                print(colorize(f"You're using the latest version ({current_version})", 'green'))
            return False
    except Exception as e:
        if not silent:
            print(colorize(f"Error checking for updates: {str(e)}", 'red'))
            logger.error(f"Update check failed: {str(e)}")
        return False


def backup_data(args):
    """
    Backup all user data to a compressed archive file.

    Args:
        args: Command-line arguments with output location
    """
    print_banner()
    print_section("Data Backup")

    try:
        import shutil
        import datetime

        # Create backup filename with timestamp if not specified
        backup_file = args.output if args.output else os.path.join(
            CONFIG_DIR, f"ecocycle_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        )

        # Create a temporary directory for organizing files
        import tempfile
        temp_dir = tempfile.mkdtemp()

        try:
            # Copy data directories to temp location
            for dir_name, source_dir in [
                ('config', CONFIG_DIR),
                ('data', DATA_DIR),
                ('reports', REPORTS_DIR)
            ]:
                if os.path.exists(source_dir):
                    dest_dir = os.path.join(temp_dir, dir_name)
                    shutil.copytree(source_dir, dest_dir)

            # Create zip archive
            shutil.make_archive(
                backup_file.rstrip('.zip'),
                'zip',
                temp_dir
            )

            print(colorize(f"Backup created successfully: {backup_file}", 'green', bold=True))

            # Show backup size
            backup_size = os.path.getsize(backup_file + ".zip" if not backup_file.endswith('.zip') else backup_file)
            print(colorize(f"Backup size: {backup_size / (1024 * 1024):.2f} MB", 'blue'))

        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir)

    except Exception as e:
        print(colorize(f"Backup failed: {str(e)}", 'red'))
        logger.error(f"Backup failed: {str(e)}", exc_info=True)
        raise


def restore_data(args):
    """
    Restore user data from a backup file.

    Args:
        args: Command-line arguments with backup file location
    """
    print_banner()
    print_section("Data Restore")

    if not args.file:
        print(colorize("Error: Backup file not specified. Use --file parameter.", 'red'))
        return

    if not os.path.exists(args.file):
        print(colorize(f"Error: Backup file not found: {args.file}", 'red'))
        return

    # Confirm restore operation
    if not args.force:
        print(colorize("WARNING: This will overwrite your current data!", 'yellow', bold=True))
        confirmation = input("Do you want to continue? (yes/no): ")
        if confirmation.lower() not in ['yes', 'y']:
            print(colorize("Restore operation cancelled.", 'yellow'))
            return

    try:
        import shutil
        import zipfile
        import tempfile

        temp_dir = tempfile.mkdtemp()

        try:
            # Extract backup archive
            with zipfile.ZipFile(args.file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Restore directories
            for dir_name, target_dir in [
                ('config', CONFIG_DIR),
                ('data', DATA_DIR),
                ('reports', REPORTS_DIR)
            ]:
                source_dir = os.path.join(temp_dir, dir_name)
                if os.path.exists(source_dir):
                    # Create target directory if it doesn't exist
                    ensure_dir_exists(target_dir)

                    # Remove existing files
                    for item in os.listdir(target_dir):
                        item_path = os.path.join(target_dir, item)
                        if os.path.isfile(item_path):
                            os.unlink(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)

                    # Copy files from backup
                    for item in os.listdir(source_dir):
                        source_item = os.path.join(source_dir, item)
                        target_item = os.path.join(target_dir, item)
                        if os.path.isdir(source_item):
                            shutil.copytree(source_item, target_item)
                        else:
                            shutil.copy2(source_item, target_item)

            print(colorize("Data restored successfully!", 'green', bold=True))

        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir)

    except Exception as e:
        print(colorize(f"Restore failed: {str(e)}", 'red'))
        logger.error(f"Restore failed: {str(e)}", exc_info=True)
        raise


def get_ride_data(period='all'):
    """
    Load ride data from the data directory.

    Args:
        period (str): Time period to load ('day', 'week', 'month', 'year', 'all')

    Returns:
        list: List of ride data dictionaries
    """
    import json
    import datetime

    # Calculate the start date based on period
    now = datetime.datetime.now()
    if period == 'day':
        start_date = now - datetime.timedelta(days=1)
    elif period == 'week':
        start_date = now - datetime.timedelta(weeks=1)
    elif period == 'month':
        start_date = now - datetime.timedelta(days=30)
    elif period == 'year':
        start_date = now - datetime.timedelta(days=365)
    else:  # 'all'
        start_date = datetime.datetime.min

    rides = []

    # Find all ride data files
    ride_files = []
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith('.json') and file.startswith('ride_'):
                ride_files.append(os.path.join(root, file))

    # Load each ride file
    for ride_file in ride_files:
        try:
            with open(ride_file, 'r') as f:
                ride_data = json.load(f)

                # Check if the ride is within the requested period
                ride_date = datetime.datetime.fromisoformat(ride_data.get('timestamp', '1970-01-01T00:00:00'))
                if ride_date >= start_date:
                    rides.append(ride_data)

        except Exception as e:
            logger.error(f"Error loading ride data from {ride_file}: {str(e)}")

    # Sort rides by date
    rides.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    return rides


def quick_ride_command(args):
    """
    Log a quick ride without running a tracking session.

    Args:
        args: Command-line arguments with ride details
    """
    print_banner()
    print_section("Quick Ride Logging")

    try:
        import json
        import datetime
        import uuid

        # Generate a unique ride ID
        ride_id = str(uuid.uuid4())

        # Create ride data structure
        ride_data = {
            'id': ride_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'distance': args.distance,
            'duration': args.duration,
            'transport_mode': args.mode,
            'start_location': args.start,
            'end_location': args.end,
            'notes': args.notes,
            'manually_logged': True
        }

        # Calculate environmental impact
        # These are simplified calculations - in a real app, you'd use more sophisticated models
        carbon_savings = 0
        if args.mode == 'bike':
            # Assuming car would emit ~150g CO2 per km
            carbon_savings = args.distance * 0.15  # kg of CO2
        elif args.mode == 'walk':
            carbon_savings = args.distance * 0.15  # same as bike vs. car
        elif args.mode == 'public_transport':
            # Assuming public transport emits ~1/3 of a car
            carbon_savings = args.distance * 0.1  # kg of CO2

        ride_data['carbon_savings'] = carbon_savings

        # Save ride data
        ensure_dir_exists(DATA_DIR)
        file_path = os.path.join(DATA_DIR, f"ride_{ride_id}.json")
        with open(file_path, 'w') as f:
            json.dump(ride_data, f, indent=4)

        print(colorize("Ride logged successfully!", 'green', bold=True))
        print_key_value("Distance", f"{args.distance} km")
        print_key_value("Duration", f"{args.duration} minutes")
        print_key_value("Transport Mode", args.mode)
        print_key_value("Carbon Savings", f"{carbon_savings:.2f} kg CO2")

    except Exception as e:
        print(colorize(f"Error logging ride: {str(e)}", 'red'))
        logger.error(f"Quick ride logging failed: {str(e)}", exc_info=True)
        raise


def history_command(args):
    """
    View ride history.

    Args:
        args: Command-line arguments with filtering options
    """
    print_banner()
    print_section("Ride History")

    try:
        # Get ride data for the specified period
        rides = get_ride_data(args.period)

        if not rides:
            print(colorize("No rides found for the specified period.", 'yellow'))
            return

        # Apply filters if specified
        if args.mode:
            rides = [r for r in rides if r.get('transport_mode') == args.mode]

        if args.min_distance:
            rides = [r for r in rides if r.get('distance', 0) >= args.min_distance]

        if args.max_distance:
            rides = [r for r in rides if r.get('distance', 0) <= args.max_distance]

        # Display ride history
        print(colorize(f"Found {len(rides)} rides", 'blue'))

        # Limit the number of displayed rides if needed
        display_rides = rides[:args.limit] if args.limit else rides

        # Calculate totals
        total_distance = sum(r.get('distance', 0) for r in rides)
        total_duration = sum(r.get('duration', 0) for r in rides)
        total_carbon_savings = sum(r.get('carbon_savings', 0) for r in rides)

        # Print summary
        print()
        print_key_value("Total Distance", f"{total_distance:.2f} km")
        print_key_value("Total Duration", f"{total_duration:.0f} minutes")
        print_key_value("Total Carbon Savings", f"{total_carbon_savings:.2f} kg CO2")
        print()

        # Print detailed ride list
        for i, ride in enumerate(display_rides):
            import datetime
            ride_date = datetime.datetime.fromisoformat(ride.get('timestamp', '')).strftime('%Y-%m-%d %H:%M')
            print(colorize(f"Ride {i + 1} - {ride_date}", 'green', bold=True))
            print_key_value("  Distance", f"{ride.get('distance', 0):.2f} km")
            print_key_value("  Duration", f"{ride.get('duration', 0):.0f} minutes")
            print_key_value("  Transport Mode", ride.get('transport_mode', 'unknown'))
            print_key_value("  Carbon Savings", f"{ride.get('carbon_savings', 0):.2f} kg CO2")
            if ride.get('notes'):
                print_key_value("  Notes", ride.get('notes'))
            print()

        # Show if there are more rides not displayed
        if args.limit and len(rides) > args.limit:
            print(colorize(f"... and {len(rides) - args.limit} more rides.", 'yellow'))

    except Exception as e:
        print(colorize(f"Error displaying ride history: {str(e)}", 'red'))
        logger.error(f"History command failed: {str(e)}", exc_info=True)
        raise


def impact_report_command(args):
    """
    Generate environment impact reports.

    Args:
        args: Command-line arguments with reporting options
    """
    print_banner()
    print_section("Environmental Impact Report")

    try:
        # Get ride data for the specified period
        rides = get_ride_data(args.period)

        if not rides:
            print(colorize("No data available for impact report.", 'yellow'))
            return

        # Calculate impact metrics
        total_distance = sum(r.get('distance', 0) for r in rides)
        total_carbon_savings = sum(r.get('carbon_savings', 0) for r in rides)

        # Additional environmental metrics
        trees_equivalent = total_carbon_savings / 20  # rough estimate: 1 tree absorbs ~20kg CO2 per year
        gasoline_saved = total_carbon_savings / 2.3  # kg CO2 per liter of gasoline

        # Group by transport mode
        transport_modes = {}
        for ride in rides:
            mode = ride.get('transport_mode', 'unknown')
            if mode not in transport_modes:
                transport_modes[mode] = {
                    'count': 0,
                    'distance': 0,
                    'carbon_savings': 0
                }
            transport_modes[mode]['count'] += 1
            transport_modes[mode]['distance'] += ride.get('distance', 0)
            transport_modes[mode]['carbon_savings'] += ride.get('carbon_savings', 0)

        # Display the report
        print(colorize("Summary Impact Metrics", 'blue', bold=True))
        print_key_value("Period", args.period)
        print_key_value("Total Rides", len(rides))
        print_key_value("Total Distance", f"{total_distance:.2f} km")
        print_key_value("Carbon Emissions Saved", f"{total_carbon_savings:.2f} kg CO2")
        print_key_value("Equivalent to", f"{trees_equivalent:.1f} tree-years of carbon absorption")
        print_key_value("Gasoline Saved", f"{gasoline_saved:.2f} liters")

        print()
        print(colorize("Impact by Transport Mode", 'blue', bold=True))
        for mode, data in transport_modes.items():
            print_key_value(f"{mode.title()}",
                            f"{data['count']} rides, {data['distance']:.2f} km, {data['carbon_savings']:.2f} kg CO2 saved")

        # Generate visualizations if matplotlib is available
        if args.visualize:
            try:
                import matplotlib.pyplot as plt
                import numpy as np
                from matplotlib.dates import DateFormatter
                import datetime

                # Create a directory for saving visualizations
                viz_dir = os.path.join(REPORTS_DIR, 'visualizations')
                ensure_dir_exists(viz_dir)

                # Prepare time series data
                dates = [datetime.datetime.fromisoformat(r.get('timestamp', '')) for r in rides]
                distances = [r.get('distance', 0) for r in rides]
                carbon_savings = [r.get('carbon_savings', 0) for r in rides]

                # Sort by date
                sorted_data = sorted(zip(dates, distances, carbon_savings))
                dates, distances, carbon_savings = zip(*sorted_data) if sorted_data else ([], [], [])

                # Time series plot
                plt.figure(figsize=(12, 6))
                plt.subplot(2, 1, 1)
                plt.plot(dates, distances, 'b-', marker='o')
                plt.title('Distance Over Time')
                plt.ylabel('Distance (km)')
                plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
                plt.xticks(rotation=45)
                plt.tight_layout()

                plt.subplot(2, 1, 2)
                plt.plot(dates, carbon_savings, 'g-', marker='o')
                plt.title('Carbon Savings Over Time')
                plt.ylabel('CO2 Saved (kg)')
                plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Save the plot
                time_series_plot = os.path.join(viz_dir, f"impact_time_series_{args.period}.png")
                plt.savefig(time_series_plot)

                # Transport mode distribution pie chart
                plt.figure(figsize=(10, 8))
                modes = list(transport_modes.keys())
                mode_distances = [transport_modes[m]['distance'] for m in modes]

                plt.pie(mode_distances, labels=modes, autopct='%1.1f%%',
                        startangle=90, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
                plt.axis('equal')
                plt.title('Distance by Transport Mode')

                # Save the plot
                mode_plot = os.path.join(viz_dir, f"impact_mode_distribution_{args.period}.png")
                plt.savefig(mode_plot)

                print()
                print(colorize("Visualizations generated:", 'green'))
                print(colorize(f"Time series: {time_series_plot}", 'blue'))
                print(colorize(f"Mode distribution: {mode_plot}", 'blue'))

            except ImportError:
                print(colorize("Visualizations not available: matplotlib is required.", 'yellow'))
            except Exception as viz_error:
                print(colorize(f"Error creating visualizations: {str(viz_error)}", 'yellow'))
                logger.error(f"Visualization error: {str(viz_error)}", exc_info=True)

        # Save report as file if requested
        if args.output:
            report_file = args.output
            with open(report_file, 'w') as f:
                f.write(f"EcoCycle Environmental Impact Report\n")
                f.write(f"Period: {args.period}\n")
                f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

                f.write("Summary Impact Metrics\n")
                f.write(f"Total Rides: {len(rides)}\n")
                f.write(f"Total Distance: {total_distance:.2f} km\n")
                f.write(f"Carbon Emissions Saved: {total_carbon_savings:.2f} kg CO2\n")
                f.write(f"Equivalent to: {trees_equivalent:.1f} tree-years of carbon absorption\n")
                f.write(f"Gasoline Saved: {gasoline_saved:.2f} liters\n\n")

                f.write("Impact by Transport Mode\n")
                for mode, data in transport_modes.items():
                    f.write(
                        f"{mode.title()}: {data['count']} rides, {data['distance']:.2f} km, {data['carbon_savings']:.2f} kg CO2 saved\n")

            print()
            print(colorize(f"Report saved to: {report_file}", 'green'))

    except Exception as e:
        print(colorize(f"Error generating impact report: {str(e)}", 'red'))
        logger.error(f"Impact report failed: {str(e)}", exc_info=True)
        raise


def validate_input(value, validator_func, error_message):
    """Validate user input using the provided validator function."""
    try:
        if not validator_func(value):
            logger.error(error_message)
            return False
        return True
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return False


def safe_file_operation(operation_func, *args, **kwargs):
    """Execute file operations with proper error handling."""
    try:
        return operation_func(*args, **kwargs)
    except PermissionError:
        logger.error(f"Permission denied when accessing file. Please check your access rights.")
        return None
    except FileNotFoundError:
        logger.error(f"File not found. Please check the path.")
        return None
    except Exception as e:
        logger.error(f"File operation error: {str(e)}")
        return None


def get_platform_specific_path(path):
    """Handle cross-platform path issues."""
    import os
    import platform

    # Replace forward/backward slashes according to the platform
    if platform.system() == "Windows":
        return path.replace("/", "\\")
    else:
        return path.replace("\\", "/")


def manage_resources(resource_func, cleanup_func=None):
    """Resource management decorator for proper cleanup."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            resource = None
            try:
                resource = resource_func()
                return func(resource, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error managing resources: {str(e)}")
                raise
            finally:
                if cleanup_func and resource:
                    try:
                        cleanup_func(resource)
                    except Exception as e:
                        logger.error(f"Error during resource cleanup: {str(e)}")

        return wrapper

    return decorator


def doctor_command(args):
    """
        Perform system diagnostics for the development environment.

        This command scans for:
        - Missing dependencies
        - Version mismatches
        - Configuration issues
        - Common errors

        It reports problems and suggests practical fixes.
        """
    import sys
    import platform
    import subprocess
    import pkg_resources
    from importlib import util

    print_banner()
    print_section("ECOCYCLE DEVELOPMENT ENVIRONMENT DIAGNOSTICS")

    issues_found = 0
    warnings_found = 0

    # List of required dependencies
    required_packages = {
        'requests': '2.25.0',
        'lxml': '4.6.0',
        'protobuf': '3.0.0',
        'pyparsing': '2.4.0',
        'docutils': '0.16',
        'ipython': '7.0.0',
    }

    # List of optional dependencies
    optional_packages = {
        'requests',
        'ipython',
        'colorama',
        'python-dotenv',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'google-auth',
        'tqdm',
        'cryptography',
        'yagmail',
    }

    # -----------------
    # 1. SYSTEM CHECK
    # -----------------
    print_section("1. SYSTEM ENVIRONMENT")

    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    min_py_version = (3, 7)

    if sys.version_info >= min_py_version:
        print(f"✅ Python version: {colorize(py_version, Colors.GREEN)}")
    else:
        print(
            f"❌ Python version: {colorize(py_version, Colors.RED)} (>= {min_py_version[0]}.{min_py_version[1]} required)")
        print(f"   {colorize('Fix:', Colors.BOLD)} Install Python {min_py_version[0]}.{min_py_version[1]} or newer")
        issues_found += 1

    # Check OS compatibility
    os_name = platform.system()
    print(f"ℹ️ Operating System: {os_name} ({platform.version()})")

    # Check for virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if in_venv:
        print(f"✅ Virtual Environment: {colorize('Active', Colors.GREEN)} ({sys.prefix})")
    else:
        print(f"⚠️ Virtual Environment: {colorize('Not detected', Colors.YELLOW)}")
        print(f"   {colorize('Recommendation:', Colors.BOLD)} Consider using a virtual environment for isolation")
        warnings_found += 1

    # Check for sufficient disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage(DATA_DIR)
        free_gb = free / (1024 ** 3)

        if free_gb > 1.0:
            print(f"✅ Disk Space: {colorize(f'{free_gb:.2f} GB available', Colors.GREEN)}")
        else:
            print(f"⚠️ Disk Space: {colorize(f'Only {free_gb:.2f} GB available', Colors.YELLOW)}")
            print(f"   {colorize('Recommendation:', Colors.BOLD)} Free up disk space for optimal performance")
            warnings_found += 1
    except Exception:
        print(f"⚠️ Disk Space: {colorize('Unable to check', Colors.YELLOW)}")
        warnings_found += 1

    # -----------------
    # 2. DEPENDENCIES
    # -----------------
    print_section("2. DEPENDENCY CHECK")

    # Check for pip
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "--version"], stderr=subprocess.STDOUT)
        print(f"✅ Package Manager: {colorize('pip is available', Colors.GREEN)}")
    except subprocess.CalledProcessError:
        print(f"❌ Package Manager: {colorize('pip not found', Colors.RED)}")
        print(
            f"   {colorize('Fix:', Colors.BOLD)} Install pip: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py")
        issues_found += 1

    # Check required dependencies
    print("\nRequired Packages:")
    for package, min_version in required_packages.items():
        try:
            spec = util.find_spec(package)
            if spec is None:
                print(f"❌ {package}: {colorize('Not installed', Colors.RED)}")
                print(f"   {colorize('Fix:', Colors.BOLD)} Install with: pip install {package}>={min_version}")
                issues_found += 1
                continue

            installed_version = pkg_resources.get_distribution(package).version
            min_version_parsed = pkg_resources.parse_version(min_version)
            installed_version_parsed = pkg_resources.parse_version(installed_version)

            if installed_version_parsed >= min_version_parsed:
                print(f"✅ {package}: {colorize(installed_version, Colors.GREEN)}")
            else:
                print(f"❌ {package}: {colorize(installed_version, Colors.RED)} (>= {min_version} required)")
                print(
                    f"   {colorize('Fix:', Colors.BOLD)} Upgrade with: pip install --upgrade {package}>={min_version}")
                issues_found += 1

        except (pkg_resources.DistributionNotFound, ImportError):
            print(f"❌ {package}: {colorize('Not installed', Colors.RED)}")
            print(f"   {colorize('Fix:', Colors.BOLD)} Install with: pip install {package}>={min_version}")
            issues_found += 1

    # Check optional dependencies
    print("\nOptional Packages:")
    for package in optional_packages:
        try:
            spec = util.find_spec(package)
            if spec is None:
                print(f"⚠️ {package}: {colorize('Not installed', Colors.YELLOW)} (optional)")
                print(f"   {colorize('Enhancement:', Colors.BOLD)} Install with: pip install {package}>={min_version}")
                warnings_found += 1
                continue

            installed_version = pkg_resources.get_distribution(package).version
            min_version_parsed = pkg_resources.parse_version(min_version)
            installed_version_parsed = pkg_resources.parse_version(installed_version)

            if installed_version_parsed >= min_version_parsed:
                print(f"✅ {package}: {colorize(installed_version, Colors.GREEN)}")
            else:
                print(f"⚠️ {package}: {colorize(installed_version, Colors.YELLOW)} (>= {min_version} recommended)")
                print(
                    f"   {colorize('Enhancement:', Colors.BOLD)} Upgrade with: pip install --upgrade {package}>={min_version}")
                warnings_found += 1

        except (pkg_resources.DistributionNotFound, ImportError):
            print(f"⚠️ {package}: {colorize('Not installed', Colors.YELLOW)} (optional)")
            print(f"   {colorize('Enhancement:', Colors.BOLD)} Install with: pip install {package}>={min_version}")
            warnings_found += 1

    # ------------------
    # 3. CONFIGURATION
    # ------------------
    print_section("3. CONFIGURATION CHECK")

    # Check directories
    directories = {
        "Config Directory": CONFIG_DIR,
        "Log Directory": LOG_DIR,
        "Data Directory": DATA_DIR,
        "Reports Directory": REPORTS_DIR
    }

    for name, dir_path in directories.items():
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            # Check if directory is writable
            if os.access(dir_path, os.W_OK):
                print(f"✅ {name}: {colorize(dir_path, Colors.GREEN)} (writable)")
            else:
                print(f"❌ {name}: {colorize(dir_path, Colors.RED)} (not writable)")
                print(f"   {colorize('Fix:', Colors.BOLD)} Set proper permissions: chmod u+w {dir_path}")
                issues_found += 1
        else:
            print(f"❌ {name}: {colorize('Missing', Colors.RED)} ({dir_path})")
            print(f"   {colorize('Fix:', Colors.BOLD)} Run: ecocycle config --setup")
            issues_found += 1

    # Check configuration file
    if os.path.exists(CONFIG_FILE):
        if os.access(CONFIG_FILE, os.R_OK):
            try:
                config = load_config()
                print(f"✅ Configuration file: {colorize('Valid', Colors.GREEN)} ({CONFIG_FILE})")

                # Check for required config keys
                required_keys = ["username", "default_transportation", "distance_unit"]
                missing_keys = [key for key in required_keys if key not in config]

                if missing_keys:
                    print(
                        f"❌ Configuration: {colorize('Missing required settings', Colors.RED)}: {', '.join(missing_keys)}")
                    print(f"   {colorize('Fix:', Colors.BOLD)} Run: ecocycle config")
                    issues_found += 1

                # Check for deprecated settings
                deprecated_keys = ["old_setting", "legacy_option"]
                used_deprecated = [key for key in deprecated_keys if key in config]

                if used_deprecated:
                    print(
                        f"⚠️ Configuration: {colorize('Using deprecated settings', Colors.YELLOW)}: {', '.join(used_deprecated)}")
                    print(
                        f"   {colorize('Recommendation:', Colors.BOLD)} Update your configuration to remove deprecated settings")
                    warnings_found += 1

            except Exception as e:
                print(f"❌ Configuration file: {colorize('Invalid format', Colors.RED)}")
                print(f"   Error: {str(e)}")
                print(f"   {colorize('Fix:', Colors.BOLD)} Run: ecocycle config --reset")
                issues_found += 1
        else:
            print(f"❌ Configuration file: {colorize('Not readable', Colors.RED)} ({CONFIG_FILE})")
            print(f"   {colorize('Fix:', Colors.BOLD)} Set proper permissions: chmod u+r {CONFIG_FILE}")
            issues_found += 1
    else:
        print(f"❌ Configuration file: {colorize('Missing', Colors.RED)} ({CONFIG_FILE})")
        print(f"   {colorize('Fix:', Colors.BOLD)} Run: ecocycle config --setup")
        issues_found += 1

    # ------------------
    # 4. DATA INTEGRITY
    # ------------------
    print_section("4. DATA INTEGRITY CHECK")

    # Check ride data
    try:
        ride_data = get_ride_data()
        if ride_data is not None:
            if isinstance(ride_data, list) and len(ride_data) > 0:
                print(f"✅ Ride data: {colorize('Available', Colors.GREEN)} ({len(ride_data)} records)")

                # Validate data structure
                valid_structure = True
                for entry in ride_data[:5]:  # Check first few entries
                    required_fields = ["date", "distance", "transportation"]
                    missing_fields = [field for field in required_fields if field not in entry]
                    if missing_fields:
                        valid_structure = False
                        break

                if not valid_structure:
                    print(f"❌ Ride data structure: {colorize('Invalid format', Colors.RED)}")
                    print(f"   {colorize('Fix:', Colors.BOLD)} Run: ecocycle backup && ecocycle restore")
                    issues_found += 1
                else:
                    print(f"✅ Ride data structure: {colorize('Valid', Colors.GREEN)}")
            else:
                print(f"⚠️ Ride data: {colorize('Empty', Colors.YELLOW)}")
                print(f"   {colorize('Note:', Colors.BOLD)} No rides recorded yet. Use 'ecocycle run' to add rides.")
                warnings_found += 1
        else:
            print(f"❌ Ride data: {colorize('Could not load data', Colors.RED)}")
            print(f"   {colorize('Fix:', Colors.BOLD)} Run: ecocycle doctor --repair-data")
            issues_found += 1
    except Exception as e:
        print(f"❌ Ride data: {colorize('Error accessing data', Colors.RED)}")
        print(f"   Error: {str(e)}")
        print(f"   {colorize('Fix:', Colors.BOLD)} Run: ecocycle doctor --repair-data")
        issues_found += 1

    # ------------------
    # 5. CONNECTIVITY
    # ------------------
    print_section("5. NETWORK CONNECTIVITY")

    # Check internet connection
    try:
        import socket
        socket.create_connection(("www.google.com", 80), timeout=2)
        print(f"✅ Internet connection: {colorize('Available', Colors.GREEN)}")

        # Check API endpoints if internet is available
        try:
            import requests
            weather_endpoint = "https://api.openweathermap.org/"
            response = requests.head(weather_endpoint, timeout=3)
            if response.status_code < 400:
                print(f"✅ Weather API: {colorize('Accessible', Colors.GREEN)}")
            else:
                print(f"⚠️ Weather API: {colorize('Returned status code ' + str(response.status_code), Colors.YELLOW)}")
                print(f"   {colorize('Note:', Colors.BOLD)} Weather data may not be available")
                warnings_found += 1
        except Exception:
            print(f"⚠️ Weather API: {colorize('Not accessible', Colors.YELLOW)}")
            print(f"   {colorize('Note:', Colors.BOLD)} Weather data may not be available")
            warnings_found += 1

    except (socket.timeout, socket.error):
        print(f"⚠️ Internet connection: {colorize('Not available', Colors.YELLOW)}")
        print(f"   {colorize('Note:', Colors.BOLD)} Weather and update features will not work without internet")
        warnings_found += 1

    # ------------------
    # 6. COMMON ERRORS
    # ------------------
    print_section("6. COMMON ERROR DETECTION")

    # Check for common permission errors
    permission_issues = False
    for dir_path in [CONFIG_DIR, DATA_DIR, LOG_DIR, REPORTS_DIR]:
        if os.path.exists(dir_path) and not os.access(dir_path, os.W_OK | os.R_OK):
            if not permission_issues:
                print(f"❌ Permission errors: {colorize('Found', Colors.RED)}")
                permission_issues = True
                issues_found += 1
            print(f"   - {dir_path} has insufficient permissions")

    if not permission_issues:
        print(f"✅ Permissions: {colorize('No issues found', Colors.GREEN)}")
    else:
        print(f"   {colorize('Fix:', Colors.BOLD)} Set proper permissions: chmod -R u+rw " + CONFIG_DIR)

    # Check for path length issues (Windows)
    if os.name == 'nt':  # Windows
        long_paths = []
        for dir_path in [CONFIG_DIR, DATA_DIR, LOG_DIR, REPORTS_DIR]:
            if len(dir_path) > 240:
                long_paths.append(dir_path)

        if long_paths:
            print(f"⚠️ Path length: {colorize('Potentially problematic paths', Colors.YELLOW)}")
            for path in long_paths:
                print(f"   - {path}")
            print(
                f"   {colorize('Note:', Colors.BOLD)} Windows has a 260 character path limit. Consider shorter paths.")
            warnings_found += 1
        else:
            print(f"✅ Path length: {colorize('No issues found', Colors.GREEN)}")

    # Check for conflicting versions in dependencies
    try:
        import pkg_resources
        dependency_issues = []
        dist_requirements = {}

        for dist in pkg_resources.working_set:
            dist_requirements[dist.key] = dist.requires()

        for dist, reqs in dist_requirements.items():
            for req in reqs:
                req_name = req.key
                if req_name in dist_requirements:
                    # Check if requirement is satisfied
                    try:
                        pkg_resources.get_distribution(str(req))
                    except pkg_resources.VersionConflict:
                        dependency_issues.append(f"{dist} requires {req}")

        if dependency_issues:
            print(f"❌ Dependency conflicts: {colorize('Found', Colors.RED)}")
            for issue in dependency_issues[:3]:  # Show only first few conflicts
                print(f"   - {issue}")
            if len(dependency_issues) > 3:
                print(f"   - ...and {len(dependency_issues) - 3} more")
            print(f"   {colorize('Fix:', Colors.BOLD)} Create a fresh virtual environment and reinstall dependencies")
            issues_found += 1
        else:
            print(f"✅ Dependency conflicts: {colorize('No issues found', Colors.GREEN)}")
    except Exception:
        print(f"⚠️ Dependency conflicts: {colorize('Unable to check', Colors.YELLOW)}")
        warnings_found += 1

    # ------------------
    # SUMMARY
    # ------------------
    print_section("DIAGNOSIS SUMMARY")

    if issues_found == 0 and warnings_found == 0:
        print(f"\n{colorize('✨ All systems operational! ✨', Colors.GREEN)}")
        print("Your development environment is properly configured and ready to use.")
    else:
        if issues_found > 0:
            print(f"\n{colorize(f'❌ Found {issues_found} critical issue(s) that need attention', Colors.RED)}")
        if warnings_found > 0:
            print(f"{colorize(f'⚠️ Found {warnings_found} warning(s) that may affect functionality', Colors.YELLOW)}")

        print("\nRecommended actions:")
        if issues_found > 0:
            print(f"{colorize('1. Fix critical issues first', Colors.BOLD)} - These prevent proper operation")
        if warnings_found > 0:
            print(f"{colorize('2. Address warnings', Colors.BOLD)} - These may limit functionality")
        print(f"{colorize('3. Run doctor again', Colors.BOLD)} - Verify all issues are resolved: ecocycle doctor")

    print("\nFor additional help, run:")
    print(f"  {colorize('ecocycle --help', Colors.BOLD)}")

    # Return success (0) if no issues, otherwise return error code
    return 1 if issues_found > 0 else 0


def run_doctor_diagnostics():
    """Run diagnostics checks."""
    # Check system environment
    check_system_environment()

    # Check configuration
    check_configuration()

    # Check data directories
    check_directories()

    # Check API accessibility
    check_api_connectivity()

    # Check dependencies
    check_dependencies()

    # Provide summary
    print_section("Diagnosis Summary")
    print("Diagnostics completed. See above for any issues that need attention.")
    print("Run 'ecocycle doctor fix' to attempt automatic fixes for common issues.")


def check_system_environment():
    """Check system environment for compatibility issues."""
    print_section("System Environment")

    # Check Python version
    import sys
    python_version = ".".join(map(str, sys.version_info[:3]))
    python_ok = sys.version_info >= (3, 11)
    status = "OK" if python_ok else "WARNING"
    color = Colors.GREEN if python_ok else Colors.YELLOW
    print_key_value("Python Version", f"{python_version} [{colorize(status, color)}]")

    if not python_ok:
        print(colorize("  - Python 3.11 or higher is recommended", Colors.YELLOW))

    # Check operating system
    import platform
    os_name = platform.system()
    os_version = platform.version()
    print_key_value("Operating System", f"{os_name} {os_version}")


def check_configuration():
    """Check configuration files for validity and completeness."""
    print_section("Configuration Check")

    config_exists = os.path.exists(CONFIG_FILE)
    status = "FOUND" if config_exists else "MISSING"
    color = Colors.GREEN if config_exists else Colors.RED
    print_key_value("Config File", f"{CONFIG_FILE} [{colorize(status, color)}]")

    if not config_exists:
        print(colorize("  - Configuration file is missing. Run 'ecocycle config setup' to create it.", Colors.RED))
        return

    try:
        config = load_config()
        # Check required config values
        required_keys = ["user_name", "location", "unit_system"]
        missing_keys = [key for key in required_keys if key not in config or not config[key]]

        if missing_keys:
            print(colorize(f"  - Missing configuration: {', '.join(missing_keys)}", Colors.YELLOW))
            print(colorize("  - Run 'ecocycle config set <key> <value>' to update missing fields", Colors.YELLOW))
        else:
            print(colorize("  - All required configuration values present", Colors.GREEN))
    except Exception as e:
        print(colorize(f"  - Error loading config: {str(e)}", Colors.RED))


def check_directories():
    """Check if all required directories exist and are writable."""
    print_section("Directory Check")

    directories = {
        "Config Directory": CONFIG_DIR,
        "Log Directory": LOG_DIR,
        "Data Directory": DATA_DIR,
        "Reports Directory": REPORTS_DIR
    }

    for name, directory in directories.items():
        exists = os.path.exists(directory)
        writable = os.access(directory, os.W_OK) if exists else False

        if exists and writable:
            status = "OK"
            color = Colors.GREEN
        elif exists and not writable:
            status = "NOT WRITABLE"
            color = Colors.RED
        else:
            status = "MISSING"
            color = Colors.RED

        print_key_value(name, f"{directory} [{colorize(status, color)}]")

        if not exists:
            print(colorize(f"  - Directory does not exist", Colors.RED))
        elif not writable:
            print(colorize(f"  - Directory is not writable", Colors.RED))


def check_api_connectivity():
    """Check connectivity to required APIs."""
    print_section("API Connectivity")

    # List of APIs to check
    apis = [
        {"name": "Weather API", "url": "https://api.weatherapi.com/v1/current.json?key=test&q=London"},
        {"name": "Google API", "url": "https://www.googleapis.com/discovery/v1/apis"}
    ]

    for api in apis:
        try:
            import requests
            response = requests.get(api["url"], timeout=5)
            if response.status_code < 400:  # Consider any non-4xx/5xx as reachable
                status = "REACHABLE"
                color = Colors.GREEN
            else:
                status = f"ERROR ({response.status_code})"
                color = Colors.RED
        except requests.exceptions.RequestException:
            status = "UNREACHABLE"
            color = Colors.RED

        print_key_value(api["name"], f"[{colorize(status, color)}]")


def check_dependencies():
    import shutil
    import importlib.metadata
    """Check for required and optional dependencies."""
    results = {}
    results["pip_installed"] = shutil.which("pip") is not None

    # Required packages with version requirements
    required_packages = {
        "requests": "2.0.0",
        "lxml": "4.0.0",
        "protobuf": "3.0.0",
        "pyparsing": "2.0.0",
        "docutils": "0.14",
        "ipython": "7.0.0"
    }

    # Optional packages should be a dictionary, not a set
    optional_packages = {'colorama', 'requests', 'matplotlib', 'seaborn', 'tabulate', 'tqdm'}

    results["required_packages"] = {}
    for package, min_version in required_packages.items():
        try:
            version = importlib.metadata.version(package)
            results["required_packages"][package] = version
        except importlib.metadata.PackageNotFoundError:
            results["required_packages"][package] = False

    results["optional_packages"] = {}
    for package in optional_packages:
        try:
            version = importlib.metadata.version(package)
            results["optional_packages"][package] = version
        except importlib.metadata.PackageNotFoundError:
            results["optional_packages"][package] = False

    return results


def run_doctor_fixes():
    """Attempt to fix common issues automatically."""
    print_section("Attempting Fixes")

    # Fix missing directories
    fix_directories()

    # Fix config file
    fix_config_file()

    print_section("Fix Summary")
    print("Automatic fixes completed. Some issues may require manual intervention.")
    print("Run 'ecocycle doctor' to see if there are remaining problems.")


def fix_directories():
    """Fix missing directories."""
    directories = [CONFIG_DIR, LOG_DIR, DATA_DIR, REPORTS_DIR]

    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(colorize(f"✓ Created missing directory: {directory}", Colors.GREEN))
            except Exception as e:
                print(colorize(f"✗ Failed to create directory {directory}: {str(e)}", Colors.RED))


def fix_config_file():
    """Fix missing or invalid config file."""
    if not os.path.exists(CONFIG_FILE):
        try:
            default_config = {
                "user_name": "",
                "location": "",
                "unit_system": "metric",
                "weather_api_key": "",
                "google_sheets_enabled": False
            }
            save_config(default_config)
            print(colorize(f"✓ Created default config file: {CONFIG_FILE}", Colors.GREEN))
            print(colorize("  Please run 'ecocycle config' to complete your configuration", Colors.YELLOW))
        except Exception as e:
            print(colorize(f"✗ Failed to create config file: {str(e)}", Colors.RED))


def generate_doctor_report():
    """Generate a detailed diagnostic report."""
    import datetime
    import platform
    import subprocess

    print("Generating diagnostic report...")

    report_file = os.path.join(REPORTS_DIR,
                               f"diagnostic_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    try:
        with open(report_file, 'w') as f:
            # System info
            f.write("=== ECOCYCLE DIAGNOSTIC REPORT ===\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Version: {VERSION}\n\n")

            f.write("=== SYSTEM INFORMATION ===\n")
            f.write(f"Python: {platform.python_version()}\n")
            f.write(f"OS: {platform.system()} {platform.version()}\n")
            f.write(f"Platform: {platform.platform()}\n\n")

            # Installed packages
            f.write("=== INSTALLED PACKAGES ===\n")
            try:
                pip_output = subprocess.check_output(["pip", "list"], universal_newlines=True)
                f.write(pip_output)
            except Exception as e:
                f.write(f"Error getting package list: {str(e)}\n")
            f.write("\n")

            # Config (sanitized)
            f.write("=== CONFIGURATION ===\n")
            try:
                config = load_config()
                # Remove sensitive information
                if "weather_api_key" in config:
                    config["weather_api_key"] = "***REDACTED***"

                for key, value in config.items():
                    f.write(f"{key}: {value}\n")
            except Exception as e:
                f.write(f"Error loading config: {str(e)}\n")

        print(colorize(f"✓ Diagnostic report saved to: {report_file}", Colors.GREEN))
        print(f"Please include this file if you're reporting an issue.")
    except Exception as e:
        print(colorize(f"✗ Failed to generate diagnostic report: {str(e)}", Colors.RED))


def add_doctor_subparsers(subparsers):
    """Add doctor command subparsers."""
    doctor_parser = subparsers.add_parser("doctor", help="Run diagnostics and fix issues")
    doctor_subparsers = doctor_parser.add_subparsers(dest="subcommand")

    # Doctor subcommands
    doctor_subparsers.add_parser("fix", help="Attempt to fix common issues automatically")
    doctor_subparsers.add_parser("report", help="Generate a detailed diagnostic report")

    # Set the default function if no subcommand is provided
    doctor_parser.set_defaults(func=doctor_command)


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(description="EcoCycle - Track and analyze your eco-friendly transportation")

    # Set up the parser with common arguments
    parser.add_argument('--version', action='version', version=f'EcoCycle {VERSION}')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress output messages')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    # Create subparsers for each command
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add all the various command subparsers
    # Each command gets its own subparser with specific arguments

    # Config command
    config_parser = subparsers.add_parser('config', help='Manage configuration settings')
    config_parser.add_argument('action', choices=['show', 'set', 'reset'], help='Action to perform')
    config_parser.add_argument('key', nargs='?', help='Configuration key')
    config_parser.add_argument('value', nargs='?', help='New value for key')
    config_parser.set_defaults(func=config_command)

    # Run command
    run_parser = subparsers.add_parser('run', help='Log a new eco-friendly trip')
    run_parser.add_argument('--distance', '-d', type=float, required=True, help='Distance in kilometers')
    run_parser.add_argument('--mode', '-m', required=True,
                            choices=['bike', 'walk', 'public_transit', 'carpool'],
                            help='Transportation mode')
    run_parser.add_argument('--date', type=str, help='Date of the trip (YYYY-MM-DD), defaults to today')
    run_parser.add_argument('--notes', '-n', type=str, help='Additional notes about the trip')
    run_parser.set_defaults(func=run_command)

    # Quick ride command
    quick_ride_parser = subparsers.add_parser('quick', help='Log a quick ride with minimal input')
    quick_ride_parser.add_argument('mode', choices=['bike', 'walk'], help='Mode of transportation')
    quick_ride_parser.add_argument('distance', type=float, help='Distance in kilometers')
    quick_ride_parser.set_defaults(func=quick_ride_command)

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='View your eco-impact statistics')
    stats_parser.add_argument('--period', '-p',
                              choices=['day', 'week', 'month', 'year', 'all'],
                              default='month',
                              help='Time period for statistics')
    stats_parser.add_argument('--export', '-e', help='Export statistics to a file')
    stats_parser.set_defaults(func=stats_command)

    # History command
    history_parser = subparsers.add_parser('history', help='View your trip history')
    history_parser.add_argument('--limit', '-l', type=int, default=10, help='Number of entries to show')
    history_parser.add_argument('--mode', '-m', help='Filter by transportation mode')
    history_parser.set_defaults(func=history_command)

    # Impact report command
    impact_parser = subparsers.add_parser('impact', help='Generate an environmental impact report')
    impact_parser.add_argument('--period', type=str, default='all',
                               help='Period for the report (e.g., "week", "month", "year", "all")')
    impact_parser.add_argument('--format', '-f',
                               choices=['text', 'json', 'csv', 'html'],
                               default='text',
                               help='Output format for the report')
    impact_parser.add_argument('--output', '-o', help='Output file path')
    impact_parser.set_defaults(func=impact_report_command)

    # Weather command
    weather_parser = subparsers.add_parser('weather', help='Check weather conditions for eco-friendly travel')
    weather_parser.add_argument('--location', '-l', help='City name or coordinates')
    weather_parser.add_argument('--forecast', '-f', action='store_true', help='Show forecast for next few days')
    weather_parser.set_defaults(func=weather_command)

    # Export command
    export_parser = subparsers.add_parser('export', help='Export your data')
    export_parser.add_argument('format', choices=['json', 'csv', 'html'], help='Export format')
    export_parser.add_argument('--output', '-o', required=True, help='Output file path')
    export_parser.set_defaults(func=export_command)

    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup your EcoCycle data')
    backup_parser.add_argument('--output', '-o', help='Backup destination path')
    backup_parser.set_defaults(func=backup_data)

    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from a backup')
    restore_parser.add_argument('backup_file', help='Path to backup file')
    restore_parser.set_defaults(func=restore_data)

    # Guide command
    guide_parser = subparsers.add_parser('guide', help='Show the user guide')
    guide_parser.set_defaults(func=user_guide)

    # Doctor command and its subparsers
    doctor_subparsers = subparsers.add_parser('doctor', help='Run diagnostics and fix issues')
    doctor_subparsers.set_defaults(func=doctor_command)

    # Doctor subcommands
    doctor_subparser = doctor_subparsers.add_subparsers(dest='subcommand')
    doctor_subparser.add_parser('fix', help='Attempt to fix common issues automatically')
    doctor_subparser.add_parser('report', help='Generate a detailed diagnostic report')

    # Parse arguments
    args = parser.parse_args()

    # Set up global color preferences based on arguments
    global use_colors
    if args.no_color:
        use_colors = False

    # Configure logging based on verbosity
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    elif args.quiet:
        log_level = logging.WARNING

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(LOG_DIR, "ecocycle.log")),
            logging.StreamHandler()
        ]
    )

    try:
        # Execute the appropriate command function if specified
        if hasattr(args, 'func'):
            args.func(args)
        elif args.command:
            # Fallback for commands without explicit func
            if args.command == 'doctor':
                doctor_command(args)
        else:
            # No command was specified, show help
            parser.print_help()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {str(e)}")
            print("Use --verbose for more details.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
