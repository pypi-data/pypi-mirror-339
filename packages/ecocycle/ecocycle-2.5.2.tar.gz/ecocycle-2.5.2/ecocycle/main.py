import getpass
import importlib.util
import json
import logging
import os
import random
import smtplib
import subprocess
import sys
import time
import warnings
import webbrowser
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import GetPassWarning

import requests
from colorama import Fore, Style, init
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from tqdm import tqdm

warnings.filterwarnings("ignore", category=GetPassWarning)

os.environ["TERM"] = "xterm-256color"

logging.basicConfig(filename='ecocycle_debug.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    logging.debug("Module: %s, Function: %s - Screen cleared.", __name__, clear_screen.__name__)


def is_package_installed(package_name):
    is_installed = importlib.util.find_spec(package_name) is not None
    logging.debug("Module: %s, Function: %s - Checking if package '%s' is installed: %s", __name__, is_package_installed.__name__, package_name, is_installed)
    return is_installed

def install_packages(packages):
    logging.info("Module: %s, Function: %s - Starting package installation process.", __name__, install_packages.__name__)
    packages_to_install = [pkg for pkg in packages if not is_package_installed(pkg)]
    if not packages_to_install:
        print("All required packages are already installed. Skipping installation.")
        logging.info("Module: %s, Function: %s - All packages already installed.", __name__, install_packages.__name__)
        return

    print("Installing required packages...")
    for package in tqdm(packages_to_install, desc="Installing packages", unit="package", colour='green', position=0, leave=True): # position and leave added
        logging.debug("Module: %s, Function: %s - Installing package: %s", __name__, install_packages.__name__, package)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package, "--quiet"])
            logging.info("Module: %s, Function: %s - Successfully installed/upgraded package: %s", __name__, install_packages.__name__, package)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install/upgrade {package}. Continuing...")
            logging.warning(f"Module: %s, Function: %s - Package installation warning for {package}: %s", __name__, install_packages.__name__, package, e)

    print("Package installation complete.")
    logging.info("Module: %s, Function: %s - Package installation completed.", __name__, install_packages.__name__)


def update_google_sheets(user_data, sheet_service, google_sheet_id, google_sheets_available, debug_mode, user_data_sheet_name):
    logging.info("Module: %s, Function: %s - Starting Google Sheets update process.", __name__, update_google_sheets.__name__)
    if not google_sheets_available:
        print(Fore.RED + "Google Sheets service is temporarily unavailable." + Style.RESET_ALL)
        logging.warning("Module: %s, Function: %s - Google Sheets service unavailable, skipping update.", __name__, update_google_sheets.__name__)
        return

    try:
        sheet = sheet_service.values()
        logging.debug("Module: %s, Function: %s - Fetching existing data from Google Sheets.", __name__, update_google_sheets.__name__)
        existing_data = sheet.get(spreadsheetId=google_sheet_id, range=user_data_sheet_name).execute().get('values', [])
        headers = existing_data[0] if existing_data else []
        data_rows = existing_data[1:] if existing_data else []
        logging.debug("Module: %s, Function: %s - Existing data fetched from Google Sheets.", __name__, update_google_sheets.__name__)

        name_to_check = user_data[0]
        name_found_row_index = -1
        existing_row_data = None

        for index, row in enumerate(data_rows):
            if row and row[0] == name_to_check:
                name_found_row_index = index + 2
                existing_row_data = row
                logging.debug("Module: %s, Function: %s - User '%s' found in existing data at row index %s.", __name__, update_google_sheets.__name__, name_to_check, name_found_row_index)
                break

        if name_found_row_index != -1:
            logging.info("Module: %s, Function: %s - Updating existing user data for '%s'.", __name__, update_google_sheets.__name__, name_to_check)
            range_to_update = f'{user_data_sheet_name}!A{name_found_row_index}:H{name_found_row_index}'

            existing_distance = float(existing_row_data[1]) if len(existing_row_data) > 1 and existing_row_data[1] else 0
            existing_price = float(existing_row_data[2]) if len(existing_row_data) > 2 and existing_row_data[2] else 0
            existing_pedal_points = int(existing_row_data[3]) if len(existing_row_data) > 3 and existing_row_data[3] else 0
            existing_total_price = float(existing_row_data[4]) if len(existing_row_data) > 4 and existing_row_data[4] else 0
            existing_total_distance = float(existing_row_data[5]) if len(existing_row_data) > 5 and existing_row_data[5] else 0
            existing_co2_saved = int(existing_row_data[6]) if len(existing_row_data) > 6 and existing_row_data[6] else 0
            existing_calories_burned = int(existing_row_data[7]) if len(existing_row_data) > 7 and existing_row_data[7] else 0

            new_distance = float(user_data[1])
            new_price = float(user_data[2])
            new_pedal_points = int(user_data[3])
            new_calories_burned = int(user_data[7])
            new_co2_saved = int(user_data[6])

            updated_distance = existing_distance + new_distance
            updated_price = existing_price + new_price
            updated_pedal_points = existing_pedal_points + new_pedal_points
            updated_total_price = existing_total_price
            updated_total_distance = existing_total_distance + new_distance
            updated_co2_saved = existing_co2_saved + new_co2_saved
            updated_calories_burned = existing_calories_burned + new_calories_burned

            values_to_update = [
                name_to_check,
                updated_distance,
                updated_price,
                updated_pedal_points,
                updated_total_price,
                updated_total_distance,
                updated_co2_saved,
                updated_calories_burned
            ]
            logging.debug("Module: %s, Function: %s - Aggregated values for update: %s", __name__, update_google_sheets.__name__, values_to_update)

            if debug_mode:
                print(f"Debug: Existing row data: {existing_row_data}")
                print(f"Debug: New user data: {user_data}")
                print(f"Debug: Aggregated values: {values_to_update}")

            update_body = {
                'values': [values_to_update]
            }

            try:
                sheet.update(
                    spreadsheetId=google_sheet_id,
                    range=range_to_update,
                    valueInputOption='USER_ENTERED',
                    body=update_body
                ).execute()
                logging.info("Module: %s, Function: %s - User data updated (aggregated) in Google Sheets for '%s'.", __name__, update_google_sheets.__name__, name_to_check)
                if debug_mode:
                    print(f"Debug: User data updated (aggregated) in existing row for '{name_to_check}' in Google Sheets: {values_to_update}")
                else:
                    print(f"User data updated in Google Sheets.")
            except Exception as update_e:
                logging.error(f"Module: %s, Function: %s - Error updating existing row in Google Sheets for user '{name_to_check}': %s", __name__, update_google_sheets.__name__, update_e)
                raise update_e

        else:
            logging.info("Module: %s, Function: %s - Appending new user data for '%s'.", __name__, update_google_sheets.__name__, name_to_check)
            try:
                sheet.append(
                    spreadsheetId=google_sheet_id,
                    range=user_data_sheet_name,
                    valueInputOption='USER_ENTERED',
                    body={'values': [user_data]}
                ).execute()
                logging.info("Module: %s, Function: %s - New user data appended to Google Sheets for '%s'.", __name__, update_google_sheets.__name__, name_to_check)
                if debug_mode:
                    print(f"Debug: New user data appended to Google Sheets: {user_data}")
                else:
                    print("New user data recorded.")
            except Exception as append_e:
                logging.error(f"Module: %s, Function: %s - Error appending new row to Google Sheets for user '{name_to_check}': %s", __name__, update_google_sheets.__name__, append_e)
                raise append_e


    except Exception as e:
        print(Fore.RED + "Error updating data. Please try again later." + Style.RESET_ALL)
        logging.error(f"Module: %s, Function: %s - General error updating Google Sheets: %s", __name__, update_google_sheets.__name__, e)
        if debug_mode:
            print(f"Debug: Google Sheets update error details: {e}")

def check_headers(sheet_service, google_sheet_id, google_sheets_available, debug_mode, user_data_sheet_name, email_log_sheet_name):
    """
    Checks and adds headers to both sheets in Google Sheets if they are missing.
    """
    logging.info("Module: %s, Function: %s - Checking Google Sheets headers.", __name__, check_headers.__name__)
    if not google_sheets_available:
        logging.warning("Module: %s, Function: %s - Google Sheets service unavailable, skipping header check.", __name__, check_headers.__name__)
        return

    # Headers for user data sheet
    user_data_headers = [["Name", "Distance (km)", "Price (SGD)", "Pedal Points", "Total Price", "Total Distance",
                "CO2 Saved (kg)", "Calories Burned"]]
    # Headers for email log sheet
    email_log_headers = [["Email Address", "Date and Time", "Action Description", "Verification Status", "Target User Name"]] # Added "Target User Name" header

    try:
        # No loading bar for header check as it's usually fast
        # with tqdm(total=100, desc="Checking Headers", unit="%", colour='green', position=0, leave=True) as pbar: # position and leave added
        # Check and update headers for User Data Sheet
        logging.debug("Module: %s, Function: %s - Checking headers for User Data Sheet.", __name__, check_headers.__name__)
        result_user_data = sheet_service.values().get(spreadsheetId=google_sheet_id, range=f'{user_data_sheet_name}!A1:H1').execute()
        values_user_data = result_user_data.get('values', [])
        # pbar.update(50) # Removed pbar update
        if not values_user_data or not values_user_data[0] or values_user_data[0] != user_data_headers[0]:
            logging.info("Module: %s, Function: %s - Headers are missing or incorrect in User Data Sheet, updating headers.", __name__, check_headers.__name__)
            sheet_service.values().update(
                spreadsheetId=google_sheet_id,
                range=f'{user_data_sheet_name}!A1:H1',
                valueInputOption='RAW',
                body={'values': user_data_headers}
            ).execute()
            print(f"Google Sheet '{user_data_sheet_name}' headers updated.")
            logging.info("Module: %s, Function: %s - Google Sheet '%s' headers updated successfully.", __name__, check_headers.__name__, user_data_sheet_name)
        elif debug_mode:
            print(f"Debug: Headers already exist in {user_data_sheet_name}.")
            logging.debug("Module: %s, Function: %s - Headers already exist in %s.", __name__, check_headers.__name__, user_data_sheet_name)
        else:
            logging.debug("Module: %s, Function: %s - Headers already exist in %s.", __name__, check_headers.__name__, user_data_sheet_name)


        # Check and update headers for Email Log Sheet
        logging.debug("Module: %s, Function: %s - Checking headers for EmailLog sheet.", __name__, check_headers.__name__)
        try: # Need to check if sheet exists first, if not, add it.
            result_email_log = sheet_service.values().get(spreadsheetId=google_sheet_id, range=f'{email_log_sheet_name}!A1:E1').execute() # Modified range to A1:E1
        except: # Sheet probably does not exist
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': email_log_sheet_name
                        }
                    }
                }]
            }
            sheet_service.batchUpdate(spreadsheetId=google_sheet_id, body=request_body).execute()
            logging.info("Module: %s, Function: %s - EmailLog sheet created as it did not exist.", __name__, check_headers.__name__)
            result_email_log = sheet_service.values().get(spreadsheetId=google_sheet_id, range=f'{email_log_sheet_name}!A1:E1').execute() # Get again after creating

        values_email_log = result_email_log.get('values', [])
        # pbar.update(50) # Removed pbar update


        if not values_email_log or not values_email_log[0] or values_email_log[0] != email_log_headers[0]:
            logging.info("Module: %s, Function: %s - Headers are missing or incorrect in EmailLog sheet, updating headers.", __name__, check_headers.__name__)
            sheet_service.values().update(
                spreadsheetId=google_sheet_id,
                range=f'{email_log_sheet_name}!A1:E1', # Modified range to A1:E1
                valueInputOption='RAW',
                body={'values': email_log_headers}
            ).execute()
            print(f"Google Sheet '{email_log_sheet_name}' headers updated.")
            logging.info("Module: %s, Function: %s - Google Sheet '%s' headers updated successfully.", __name__, check_headers.__name__, email_log_sheet_name)
        elif debug_mode:
            print(f"Debug: Headers already exist in {email_log_sheet_name} sheet.")
            logging.debug("Module: %s, Function: %s - Headers already exist in {email_log_sheet_name} sheet.", __name__, check_headers.__name__)
        else:
            logging.debug("Module: %s, Function: %s - Headers already exist in {email_log_sheet_name} sheet.", __name__, check_headers.__name__)


    except Exception as e:
        print(Fore.RED + "Error accessing Google Sheets headers." + Style.RESET_ALL)
        logging.error(f"Module: %s, Function: %s - Error checking/adding headers to Google Sheets: %e", __name__, check_headers.__name__, e)
        if debug_mode:
            print(f"Debug: Header check/add error details: {e}")


def delete_all_inputs(sheet_service, google_sheet_id, google_sheets_available, debug_mode, user_data_sheet_name, email_log_sheet_name):
    logging.info("Module: %s, Function: %s - Starting data deletion from Google Sheets.", __name__, delete_all_inputs.__name__)
    if not google_sheets_available:
        print(Fore.RED + "Google Sheets service is temporarily unavailable. Cannot delete data." + Style.RESET_ALL)
        logging.warning("Module: %s, Function: %s - Google Sheets service unavailable, skipping data deletion.", __name__, delete_all_inputs.__name__)
        return
    try:
        clear_range = f'{user_data_sheet_name}!A2:H'
        clear_body = {}
        logging.debug("Module: %s, Function: %s - Clearing data range '%s' in User Data Sheet.", __name__, delete_all_inputs.__name__, clear_range)
        sheet_service.values().clear(spreadsheetId=google_sheet_id, range=clear_range, body=clear_body).execute()

        clear_range_log = f'{email_log_sheet_name}!A2:E' # Clear EmailLog sheet as well # Modified range to A2:E
        logging.debug("Module: %s, Function: %s - Clearing data range '%s' in EmailLog.", __name__, delete_all_inputs.__name__, clear_range_log)
        sheet_service.values().clear(spreadsheetId=google_sheet_id, range=clear_range_log, body=clear_body).execute()


        print("All user inputs deleted from Google Sheets.")
        logging.info("Module: %s, Function: %s - User data deletion from Google Sheets successful.", __name__, delete_all_inputs.__name__)
        if debug_mode:
            print("Debug: User data deletion from Google Sheets successful.")
    except Exception as e:
        print(Fore.RED + "Error deleting data. Please try again later." + Style.RESET_ALL)
        logging.error(f"Module: %s, Function: %s - Error deleting data from Google Sheets: %e", __name__, delete_all_inputs.__name__, e)
        if debug_mode:
            print(f"Debug: Data deletion error details: {e}")

def calculate_calories(distance, weight_kg=70, met_value=7.0):
    logging.debug("Module: %s, Function: %s - Calculating calories for distance: %s km, weight: %s kg, MET: %s.", __name__, calculate_calories.__name__, distance, weight_kg, met_value)
    calories_per_minute = (met_value * weight_kg * 3.5) / 200
    minutes_cycled = distance * 4
    total_calories_burned = calories_per_minute * minutes_cycled
    logging.debug("Module: %s, Function: %s - Calculated calories burned: %s kcal.", __name__, calculate_calories.__name__, total_calories_burned)
    return total_calories_burned

def get_coordinates(location, api_key):
    logging.info("Module: %s, Function: %s - Geocoding location: '%s'.", __name__, get_coordinates.__name__, location)
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
    logging.debug("Module: %s, Function: %s - Geocoding API URL: %s", __name__, get_coordinates.__name__, geo_url)
    response = requests.get(geo_url)
    logging.debug("Module: %s, Function: %s - Geocoding API response status code: %s", __name__, get_coordinates.__name__, response.status_code)
    data = response.json()

    if data['status'] == 'OK':
        latlng = data['results'][0]['geometry']['location']
        coordinates = f"{latlng['lat']},{latlng['lng']}"
        logging.info("Module: %s, Function: %s - Successfully geocoded location '%s' to coordinates: %s", __name__, get_coordinates.__name__, location, coordinates)
        return coordinates
    else:
        print("Could not retrieve location coordinates.")
        logging.warning(f"Module: %s, Function: %s - Error retrieving coordinates for location '{location}': {data}", __name__, get_coordinates.__name__, data)
        return None

def get_biking_duration(origin, destination, api_key):
    logging.info("Module: %s, Function: %s - Estimating biking duration from '%s' to '%s'.", __name__, get_biking_duration.__name__, origin, destination)
    origin = str(origin).strip()
    destination = str(destination).strip()

    origin_coords = get_coordinates(origin, api_key) if origin.isdigit() else origin
    destination_coords = get_coordinates(destination, api_key) if destination.isdigit() else destination

    if not origin_coords or not destination_coords:
        print("Invalid origin or destination provided.")
        logging.warning("Module: %s, Function: %s - Invalid origin or destination coordinates, cannot estimate duration.", __name__, get_biking_duration.__name__)
        return None

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin_coords}&destinations={destination_coords}&mode=bicycling&key={api_key}"
    logging.debug("Module: %s, Function: %s - Distance Matrix API URL: %s", __name__, get_biking_duration.__name__, url)

    response = requests.get(url)
    logging.debug("Module: %s, Function: %s - Distance Matrix API response status code: %s", __name__, get_biking_duration.__name__, response.status_code)
    data = response.json()

    if 'rows' in data and data['rows'] and data['rows'][0]['elements'] and data['rows'][0]['elements'][0].get('status') == 'OK':
        duration_seconds = data['rows'][0]['elements'][0]['duration']['value']

        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        logging.info("Module: %s, Function: %s - Estimated biking duration: %s hours, %s minutes.", __name__, get_biking_duration.__name__, hours, minutes)
        return hours, minutes
    else:
        print("Could not estimate biking duration.")
        logging.warning(f"Module: %s, Function: %s - Error retrieving biking duration data for origin '{origin}', destination '{destination}': {data}", __name__, get_biking_duration.__name__, data)
        return None

def get_weather_forecast(city, weather_api_key, debug_mode):
    logging.info("Module: %s, Function: %s - Fetching weather forecast for city: '%s'.", __name__, get_weather_forecast.__name__, city)
    city = str(city).strip()

    url = f'https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}'
    logging.debug("Module: %s, Function: %s - Current weather API URL: %s", __name__, get_weather_forecast.__name__, url)
    response = requests.get(url)
    logging.debug("Module: %s, Function: %s - Current weather API response status code: %s", __name__, get_weather_forecast.__name__, response.status_code)
    data = response.json()

    if response.status_code == 200:
        clear_screen()
        print(f"\nCurrent temperature in {city}: {data['current']['temp_c']}°C")
        logging.info("Module: %s, Function: %s - Successfully retrieved current weather for '%s'.", __name__, get_weather_forecast.__name__, city)
    else:
        print("Error. City not found for current weather.")
        logging.warning(f"Module: %s, Function: %s - Current weather API error for city '{city}': {data}", __name__, get_weather_forecast.__name__, data)
        if debug_mode:
            print(f"Debug: Current weather API error: {data}")

    forecast_url = f'https://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={city}&days=2'
    logging.debug("Module: %s, Function: %s - Forecast weather API URL: %s", __name__, get_weather_forecast.__name__, forecast_url)
    forecast_response = requests.get(forecast_url)
    logging.debug("Module: %s, Function: %s - Forecast weather API response status code: %s", __name__, get_weather_forecast.__name__, forecast_response.status_code)
    forecast_data = forecast_response.json()

    if forecast_response.status_code == 200:
        print(f"Weather forecast for {city}:\n")

        print(f"The next 3 hours in {city}:")
        if 'forecast' in forecast_data and 'forecastday' in forecast_data['forecast']:
            for hour in forecast_data['forecast']['forecastday'][0]['hour'][:3]:
                temp = hour['temp_c']
                condition = hour['condition']['text']
                time_hour = hour['time']
                print(f"Time: {time_hour}, Temperature: {temp}°C, Condition: {condition}")
            logging.info("Module: %s, Function: %s - Successfully retrieved and printed hourly and daily forecast for '%s'.", __name__, get_weather_forecast.__name__, city)
        else:
            print("No hourly forecast data available.")
            logging.warning(f"Module: %s, Function: %s - No hourly forecast data in response for city '{city}': {forecast_data}", __name__, get_weather_forecast.__name__, forecast_data)
            if debug_mode:
                print(f"Debug: No hourly forecast data in response: {forecast_data}")

        print(f"\nThe next 2 days in {city}:")
        for day in forecast_data['forecast']['forecastday']:
            date = day['date']
            avg_temp = day['day']['condition']['text']
            condition = day['day']['condition']['text'] # Added to get condition for daily forecast
            print(f"Date: {date}, Average Temp: {avg_temp}°C, Condition: {condition}")
    else:
        print("Error fetching weather forecast.")
        logging.warning(f"Module: %s, Function: %s - Forecast API error for city '{city}': {forecast_data}", __name__, get_weather_forecast.__name__, forecast_data)
        if debug_mode:
            print(f"Debug: Forecast API error: {forecast_data}")

def get_user_stats_from_sheets(sheet_service, google_sheet_id, google_sheets_available, name, debug_mode, user_data_sheet_name):
    logging.info("Module: %s, Function: %s - Fetching user stats from Google Sheets for user: '%s'.", __name__, get_user_stats_from_sheets.__name__, name)
    name = str(name).strip()

    if not google_sheets_available:
        print(Fore.RED + "Google Sheets service is temporarily unavailable. Cannot fetch stats." + Style.RESET_ALL)
        logging.warning("Module: %s, Function: %s - Google Sheets service unavailable, cannot fetch user stats.", __name__, get_user_stats_from_sheets.__name__)
        return None
    try:
        sheet = sheet_service.values()
        logging.debug("Module: %s, Function: %s - Fetching all data from Google Sheets to find user stats.", __name__, get_user_stats_from_sheets.__name__)
        existing_data = sheet.get(spreadsheetId=google_sheet_id, range=user_data_sheet_name).execute().get('values', [])
        headers = existing_data[0] if existing_data else []
        data_rows = existing_data[1:] if existing_data else []

        for row in data_rows:
            if row and row[0] == name:
                stats = {
                    "Name": row[0],
                    "Distance (km)": float(row[1]) if len(row) > 1 and row[1] else 0,
                    "Price (SGD)": float(row[2]) if len(row) > 2 and row[2] else 0,
                    "Pedal Points": int(row[3]) if len(row) > 3 and row[3] else 0,
                    "Total Price": float(row[4]) if len(row) > 4 and row[4] else 0,
                    "Total Distance": float(row[5]) if len(row) > 5 and row[5] else 0,
                    "CO2 Saved (kg)": int(row[6]) if len(row) > 6 and row[6] else 0,
                    "Calories Burned": int(row[7]) if len(row) > 7 and row[7] else 0,
                }
                logging.info("Module: %s, Function: %s - User stats found for '%s'.", __name__, get_user_stats_from_sheets.__name__, name)
                return stats
        print("User stats not found.")
        logging.info("Module: %s, Function: %s - User stats not found for '%s'.", __name__, get_user_stats_from_sheets.__name__, name)
        return None
    except Exception as e:
        print(Fore.RED + "Error fetching user stats. Please try again later." + Style.RESET_ALL)
        logging.error(f"Module: %s, Function: %s - Error fetching user stats from Google Sheets for name '{name}': %e", __name__, get_user_stats_from_sheets.__name__, e)
        if debug_mode:
            print(f"Debug: Error details: {e}")
        return None

def get_all_user_stats_from_sheets(sheet_service, google_sheet_id, google_sheets_available, debug_mode, user_data_sheet_name, email_log_sheet_name):
    logging.info("Module: %s, Function: %s - Fetching all user stats from Google Sheets.", __name__, get_all_user_stats_from_sheets.__name__)
    if not google_sheets_available:
        print(Fore.RED + "Google Sheets service is temporarily unavailable. Cannot fetch user list." + Style.RESET_ALL)
        logging.warning("Module: %s, Function: %s - Google Sheets service unavailable, cannot fetch all user stats.", __name__, get_all_user_stats_from_sheets.__name__)
        return None
    try:
        sheet = sheet_service.values()
        logging.debug("Module: %s, Function: %s - Fetching data from User Data Sheet for all user stats.", __name__, get_all_user_stats_from_sheets.__name__)
        sheet1_data = sheet.get(spreadsheetId=google_sheet_id, range=user_data_sheet_name).execute().get('values', [])
        sheet1_headers = sheet1_data[0] if sheet1_data else []
        sheet1_rows = sheet1_data[1:] if sheet1_data else []

        logging.debug("Module: %s, Function: %s - Fetching data from EmailLog.", __name__, get_all_user_stats_from_sheets.__name__)
        emaillog_data = sheet.get(spreadsheetId=google_sheet_id, range=email_log_sheet_name).execute().get('values', []) # Fetch EmailLog data
        emaillog_headers = emaillog_data[0] if emaillog_data else []
        emaillog_rows = emaillog_data[1:] if emaillog_data else []


        user_stats_list = []
        for row in sheet1_rows:
            if row:
                user_stats = {
                    "Name": row[0] if len(row) > 0 else "",
                    "Distance (km)": float(row[1]) if len(row) > 1 and row[1] else 0,
                    "Price (SGD)": float(row[2]) if len(row) > 2 and row[2] else 0,
                    "Pedal Points": int(row[3]) if len(row) > 3 and row[3] else 0,
                    "Total Price": float(row[4]) if len(row) > 4 and row[4] else 0,
                    "Total Distance": float(row[5]) if len(row) > 5 and row[5] else 0,
                    "CO2 Saved (kg)": int(row[6]) if len(row) > 6 and row[6] else 0,
                    "Calories Burned": int(row[7]) if len(row) > 7 and row[7] else 0,
                }
                user_stats_list.append(user_stats)

        email_log_list = [] # Prepare Email Log data to be returned as well
        for row in emaillog_rows:
            if row:
                email_log_entry = {
                    "Email Address": row[0] if len(row) > 0 else "",
                    "Date and Time": row[1] if len(row) > 1 else "",
                    "Action Description": row[2] if len(row) > 2 else "", # Changed to "Action Description"
                    "Verification Status": row[3] if len(row) > 3 else "", # Changed to "Verification Status"
                    "Target User Name": row[4] if len(row) > 4 else ""  # Added "Target User Name"
                }
                email_log_list.append(email_log_entry)


        logging.info("Module: %s, Function: %s - Successfully fetched all user stats and EmailLog data from Google Sheets.", __name__, get_all_user_stats_from_sheets.__name__)
        return {"user_stats": user_stats_list, "email_log": email_log_list} # Return both datasets
    except Exception as e:
        print(Fore.RED + "Error fetching user list. Please try again later." + Style.RESET_ALL)
        logging.error(f"Module: %s, Function: %s - Error fetching all user stats and EmailLog from Google Sheets: %e", __name__, get_all_user_stats_from_sheets.__name__, e)
        if debug_mode:
            print(f"Debug: Error details: {e}")
        return None

def generate_verification_code():
    code = str(random.randint(100000, 999999))
    logging.debug("Module: %s, Function: %s - Verification code generated: %s", __name__, generate_verification_code.__name__, code)
    return code


def send_verification_email(email_address, verification_code, email_sender, email_password, smtp_server, smtp_port):
    logging.info("Module: %s, Function: %s - Sending verification email to: %s", __name__, send_verification_email.__name__, email_address)
    subject = 'EcoCycle Program - Email Verification Code'
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = email_address

    html_body = f"""
    <html>
    <head>
        <style>
            body {{font-family: Arial, sans-serif; color: #333;}}
            .container {{width: 80%; margin: 20px auto; border: 1px solid #ddd; padding: 20px; border-radius: 5px;}}
            h2 {{color: #0056b3;}}
            .code {{background-color: #f4f4f4; padding: 10px; border-radius: 3px; font-size: 1.2em; font-weight: bold; text-align: center; margin: 20px 0;}}
            p {{line-height: 1.6;}}
            .footer {{margin-top: 20px; font-size: 0.8em; color: #777; border-top: 1px solid #eee; padding-top: 10px;}}
            .logo {{display: block; margin: 0 auto 20px auto; max-width: 150px;}}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="https://i.imgur.com/hFTRjpb.png" alt="EcoCycle Logo" class="logo">
            <h2>EcoCycle Program - Verification Code</h2>
            <p>Hello,</p>
            <p>Thank you for using the EcoCycle program. To proceed with your request, please use the following verification code:</p>
            <div class="code"><strong>{verification_code}</strong></div>
            <p>This code is valid for a short period. Please enter it in the program to continue.</p>
            <p>If you did not request this verification, please ignore this email. No action is needed.</p>
            <div class="footer">
                <p>This is an automated email from the EcoCycle Program. Please do not reply to this email.</p>
                <p>© 2025 EcoCycle Program Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    html_part = MIMEText(html_body, 'html')
    msg.attach(html_part)

    text_body = f"EcoCycle Program - Verification Code\n\nHello,\n\nThank you for using the EcoCycle program. To proceed with your request, please use the following verification code: {verification_code}. This code is valid for a short period. Please enter it in the program to continue.\n\nIf you did not request this verification, please ignore this email.\n\nThis is an automated email from the EcoCycle Program."
    text_part = MIMEText(text_body, 'plain')
    msg.attach(text_part)


    try:
        with tqdm(total=100, desc="Sending Email", unit="%", colour='green', position=0, leave=True) as pbar: # position and leave added
            server = smtplib.SMTP(smtp_server, smtp_port)
            pbar.update(10)
            server.starttls()
            pbar.update(30)
            server.login(email_sender, email_password)
            pbar.update(30)
            server.sendmail(email_sender, [email_address], msg.as_string())
            pbar.update(30)
            server.quit()
        print(f"Verification code sent to {email_address}. Please check your inbox (and spam folder).")
        logging.info("Module: %s, Function: %s - Verification email sent successfully to: %s", __name__, send_verification_email.__name__, email_address)
        return True
    except Exception as e:
        print(Fore.RED + f"Error sending verification email. Please check your email settings and try again." + Style.RESET_ALL)
        logging.error(f"Module: %s, Function: %s - Error sending verification email to {email_address}: %e", __name__, send_verification_email.__name__, e)
        if debug_mode:
            print(f"Debug: Email sending error: {e}")
        return False

def log_email_attempt(email_address, action_description, verification_status, sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name, target_user_name=None): # Added target_user_name parameter
    """
    Logs email address, timestamp, action description, verification status, and target user name to 'EmailLog' sheet.
    """
    if not google_sheets_available:
        logging.warning("Module: %s, Function: %s - Google Sheets service unavailable, cannot log email attempt.", __name__, log_email_attempt.__name__)
        return

    log_data = [
        email_address,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        action_description, # Changed variable name
        verification_status,
        target_user_name if target_user_name else "" # Added target user name to log data
    ]
    logging.debug("Module: %s, Function: %s - Email log data: %s", __name__, log_email_attempt.__name__, log_data)

    try:
        sheet = sheet_service.values()
        sheet.append(
            spreadsheetId=google_sheet_id,
            range=email_log_sheet_name,
            valueInputOption='USER_ENTERED',
            body={'values': [log_data]}
        ).execute()
        logging.info("Module: %s, Function: %s - Email attempt logged to Google Sheets: %s", __name__, log_email_attempt.__name__, log_data)
        if debug_mode:
            print(f"Debug: Email attempt logged to Google Sheets: {log_data}")
    except Exception as e:
        print(Fore.RED + "Error logging email attempt to Google Sheets." + Style.RESET_ALL)
        logging.error(f"Module: %s, Function: %s - Error logging email attempt to Google Sheets: %e", __name__, log_email_attempt.__name__, e)
        if debug_mode:
            print(f"Debug: Email log error details: {e}")


def main_program():
    global debug_mode
    global google_sheets_available

    logging.info("Module: %s, Function: %s - Program started.", __name__, main_program.__name__)
    clear_screen()
    os.environ['PIP_DISABLE_PIP_VERSION_CHECK'] = '1'

    initial_packages = ["requests", "ipython", "colorama", "python-dotenv", "tqdm",
                        "google-auth", "google-auth-oauthlib", "google-auth-httplib2", "google-api-python-client"]
    install_packages(initial_packages)


    init()
    clear_screen()
    load_dotenv()

    program_password = os.getenv('PROGRAM_PASSWORD')
    distance_api_key = os.getenv('API_DISTANCE_KEY')
    weather_api_key = os.getenv('API_WEATHER_KEY')
    service_account_info_str = os.getenv("SERVICE_ACCOUNT_INFO")
    google_sheet_id = os.getenv("GOOGLE_SHEET_ID")
    email_sender = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    user_data_sheet_name = os.getenv("USER_DATA_SHEET_NAME", "Sheet1") # Default to Sheet1 if not set
    email_log_sheet_name = os.getenv("EMAIL_LOG_SHEET_NAME", "EmailLog") # Default to EmailLog if not set


    if debug_mode:
        print("Debug: Environment variables loaded.")
        logging.debug("Module: %s, Function: %s - Debug mode: Environment variables loaded.", __name__, main_program.__name__)

    if not distance_api_key:
        print(Fore.RED + "Error: Distance API key not configured correctly." + Style.RESET_ALL)
        logging.critical("Module: %s, Function: %s - Missing API_DISTANCE_KEY environment variable.", __name__, main_program.__name__)
        return
    if not weather_api_key:
        print(Fore.RED + "Error: Weather API key not configured correctly." + Style.RESET_ALL)
        logging.critical("Module: %s, Function: %s - Missing API_WEATHER_KEY environment variable.", __name__, main_program.__name__)
        return
    if not service_account_info_str:
        print(Fore.RED + "Error: Google Sheets configuration is missing." + Style.RESET_ALL)
        logging.critical("Module: %s, Function: %s - Missing SERVICE_ACCOUNT_INFO environment variable.", __name__, main_program.__name__)
        return
    if not program_password:
        print(Fore.RED + "Error: Admin password not configured." + Style.RESET_ALL)
        logging.critical("Module: %s, Function: %s - Missing PROGRAM_PASSWORD environment variable.", __name__, main_program.__name__)
        return
    if not google_sheet_id:
        print(Fore.RED + "Warning: Google Sheets integration is not configured." + Style.RESET_ALL)
        logging.warning("Module: %s, Function: %s - Missing GOOGLE_SHEET_ID environment variable. Google Sheets integration disabled.", __name__, main_program.__name__)
        google_sheets_available = False
    else:
        google_sheets_available = True
        if debug_mode:
            print("Debug: GOOGLE_SHEET_ID is set and Google Sheets is available.")
            logging.debug("Module: %s, Function: %s - GOOGLE_SHEET_ID is set and Google Sheets is available.", __name__, main_program.__name__)
    if not email_sender or not email_password:
        print(Fore.RED + "Warning: Email settings for verification are not configured. Email verification will not work." + Style.RESET_ALL)
        logging.warning("Module: %s, Function: %s - Email settings (EMAIL_SENDER or EMAIL_PASSWORD) missing. Email verification disabled.")


    clear_screen()
    debug_key = input("\n\n\nPress Enter/↵ to start EcoCycle: ")
    debug_mode = debug_key.lower() == 'debug'
    if debug_mode:
        print(Fore.YELLOW + "\nDebug mode activated. Detailed information will be shown in console and logs." + Style.RESET_ALL)
        logging.info("Module: %s, Function: %s - Debug mode activated by user input.", __name__, main_program.__name__)
        time.sleep(1.5)


    if debug_mode:
        clear_screen()
        last_updated = "Friday, March 21, 23:04:31, 2025"
        print(Fore.RED + "You are running a demo of the EcoCycle app in DEBUG MODE.\n" + Style.RESET_ALL)
        print("This program is regularly updated for your safety.")
        print(f"This program was last updated on: {Fore.RED}{last_updated}{Style.RESET_ALL}")
        view_spreadsheet = input(
            "\n\n**To access the Google Sheet integrated with this program enter '1'; otherwise press the Enter/↵ key: ")
        if view_spreadsheet in yes_responses:
            url = "https://tinyurl.com/48jkcae9"
            webbrowser.open(url)
            print("https://tinyurl.com/48jkcae9")
            time.sleep(2.5)
            logging.debug("Module: %s, Function: %s - Debug mode: Google Sheet link opened in browser.", __name__, main_program.__name__)
        start = input("\n\n\nTo start the program, press Enter/↵: ")
        print("Starting program...")
        time.sleep(0.75)
        clear_screen()
        logging.debug("Module: %s, Function: %s - Debug mode: Program started after debug prompts.", __name__, main_program.__name__)


    clear_screen()
    print("\n\n\nWelcome to the EcoCycle app!")

    while True:
        want_estimate = input("\nDo you want an estimation of your travel time? (Y/N): ")
        if want_estimate.lower() in [resp.lower() for resp in yes_responses + no_responses]:
            logging.debug("Module: %s, Function: %s - User input for travel time estimation: %s", __name__, main_program.__name__, want_estimate)
            break
        else:
            print("Invalid input. Please enter Y or N.")

    if want_estimate in yes_responses:
        clear_screen()
        print("You are currently running the travel time estimator. To skip this part, at any time, enter 0.\n\n")
        while True:
            origin = input("Please enter your starting location: ")
            origin = origin.strip()
            if origin != "":
                logging.debug("Module: %s, Function: %s - User input for origin location: %s", __name__, main_program.__name__, origin)
                break
            else:
                print("Location cannot be empty. Please enter a starting location or '0' to skip.")

        if origin != "0":
            while True:
                destination = input("Please enter your destination: ")
                destination = destination.strip()
                if destination != "":
                    logging.debug("Module: %s, Function: %s - User input for destination location: %s", __name__, main_program.__name__, destination)
                    break
                else:
                    print("Location cannot be empty. Please enter a destination or '0' to skip.")

            if destination != "0":
                travel_time_estimation = get_biking_duration(origin, destination, distance_api_key) # Removed loading bar
                if travel_time_estimation:
                    hours, minutes = travel_time_estimation
                    clear_screen()
                    print(f"\nEstimated Travel Time By Bicycle: {hours} hours and {minutes} minutes\n")
                    logging.info("Module: %s, Function: %s - Travel time estimation successful: %s hours, %s minutes.", __name__, main_program.__name__, hours, minutes)
                elif debug_mode:
                    print("Debug: Travel time estimation failed or returned None.")
                    logging.debug("Module: %s, Function: %s - Travel time estimation failed or returned None.", __name__, main_program.__name__)
        else:
            print("Skipping travel time estimation...\n")
            logging.info("Module: %s, Function: %s - Travel time estimation skipped by user.", __name__, main_program.__name__)
        time.sleep(1)
        clear_screen()

    while True:
        weather_want = input("\nWould you like the weather forecast along your route? (Y/N): ")
        if weather_want.lower() in [resp.lower() for resp in yes_responses + no_responses]:
            logging.debug("Module: %s, Function: %s - User input for weather forecast: %s", __name__, main_program.__name__, weather_want)
            break
        else:
            print("Invalid input. Please enter Y or N.")

    if weather_want in yes_responses:
        print("Loading weather program...  \n", end="")
        # No loading bar for weather program load as it's fast
        # with tqdm(total=100, desc="Loading weather program", unit="%", colour='green', position=0, leave=False) as pbar_weather_load: # Loading bar
        #     time.sleep(1) # Simulate loading
        #     pbar_weather_load.update(100) # Loading bar complete
        time.sleep(0.5) # Reduced time to simulate load
        clear_screen()
        print("You are currently running the weather forecaster. To skip this part, at any time, enter 0.\n\n")
        while True:
            city = input("Enter your city for this route: ")
            city = city.strip()
            if city != "":
                logging.debug("Module: %s, Function: %s - User input for weather city: %s", __name__, main_program.__name__, city)
                break
            else:
                print("City name cannot be empty. Please enter a city or '0' to skip.")
        if city != "0":
            print("Fetching weather forecast... ")
            get_weather_forecast(city, weather_api_key, debug_mode) # Removed loading bar
        else:
            print("Skipping weather forecaster...\n")
            logging.info("Module: %s, Function: %s - Weather forecast skipped by user.", __name__, main_program.__name__)
        time.sleep(1)
        clear_screen()


    if isinstance(service_account_info_str, str):
        if service_account_info_str.startswith("'") and service_account_info_str.endswith("'"):
            service_account_info_str = service_account_info_str[1:-1]

        try:
            service_account_info = json.loads(service_account_info_str)
            logging.debug("Module: %s, Function: %s - Service account JSON string parsed successfully.", __name__, main_program.__name__)
        except json.JSONDecodeError as e:
            print(Fore.RED + "Error in Google Sheets configuration. Please check settings." + Style.RESET_ALL)
            logging.error(f"Module: %s, Function: %s - Error parsing service account JSON: %e. Check SERVICE_ACCOUNT_INFO env variable.", __name__, main_program.__name__, e)
            google_sheets_available = False
            if debug_mode:
                print(f"Debug: JSON parsing error: {e}")
                return

    sheet_service = None
    if google_sheets_available:
        try:
            creds = service_account.Credentials.from_service_account_info(service_account_info)
            service = build("sheets", "v4", credentials=creds)
            sheet_service = service.spreadsheets()

            # Fetch sheet metadata to dynamically get sheet names
            spreadsheet = sheet_service.get(spreadsheetId=google_sheet_id).execute()
            sheets = spreadsheet.get('sheets', [])
            sheet_titles = [sheet['properties']['title'] for sheet in sheets]

            if user_data_sheet_name not in sheet_titles:
                print(Fore.RED + f"Warning: User data sheet named '{user_data_sheet_name}' not found. Using default 'Sheet1' if it exists." + Style.RESET_ALL)
                user_data_sheet_name = "Sheet1" if "Sheet1" in sheet_titles else user_data_sheet_name # Fallback and check if default exists
                if user_data_sheet_name not in sheet_titles: # Double check if even default does not exist
                    print(Fore.RED + f"Error: Default 'Sheet1' also not found. Please ensure at least one sheet exists or correct sheet names are configured." + Style.RESET_ALL)
                    google_sheets_available = False # Disable sheets if essential sheet is missing
            if email_log_sheet_name not in sheet_titles:
                print(Fore.YELLOW + f"Warning: Email log sheet named '{email_log_sheet_name}' not found. Creating it now." + Style.RESET_ALL)
                request_body = {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': email_log_sheet_name
                            }
                        }
                    }]
                }
                sheet_service.batchUpdate(spreadsheetId=google_sheet_id, body=request_body).execute()
                print(Fore.GREEN + f"Sheet '{email_log_sheet_name}' created." + Style.RESET_ALL)


            check_headers(sheet_service, google_sheet_id, google_sheets_available, debug_mode, user_data_sheet_name, email_log_sheet_name) # Removed loading bar
            if debug_mode:
                print("Debug: Google Sheets service built successfully.")
            logging.info("Module: %s, Function: %s - Google Sheets service built successfully.", __name__, main_program.__name__)
        except Exception as e:
            print(Fore.RED + "Failed to connect to Google Sheets service." + Style.RESET_ALL)
            logging.error(f"Module: %s, Function: %s - Failed to build Google Sheets service: %e", __name__, main_program.__name__, e)
            google_sheets_available = False
            if debug_mode:
                print(f"Debug: Google Sheets service build error details: {e}")
                return


    iterate = "Y"
    total_price = 0
    total_distance = 0
    pedal_points = 0
    free_ride_num = 0
    coupon_num = random.randint(10000000, 99999999)
    user_names = []
    user_total_dist = []
    user_total_price = []
    user_total_pedal_point = []
    co2_saved = 0
    user_co2_saved = 0
    total_calories = 0
    calories_burned = 0


    while iterate in yes_responses:
        while True:
            name = input("\nPlease enter your name: ")
            name = name.strip()
            if name != "":
                logging.debug("Module: %s, Function: %s - User input for name: %s", __name__, main_program.__name__, name)
                break
            else:
                print("Name cannot be empty. Please enter your name.")

        if name.upper() == "RESET":
            clear_screen()
            if google_sheets_available:
                print("Deleting all user inputs... ")
                with tqdm(total=100, desc="Deleting User Inputs", unit="%", colour='red', position=0, leave=True) as pbar_delete_inputs: # Loading bar
                    delete_all_inputs(sheet_service, google_sheet_id, google_sheets_available, debug_mode, user_data_sheet_name, email_log_sheet_name)
                    pbar_delete_inputs.update(100) # Loading bar complete
            print("Database reset initiated. Please restart the program to ensure proper function.")
            logging.info("Module: %s, Function: %s - Database reset initiated by user command 'RESET'.", __name__, main_program.__name__)
            return

        while True:
            distance_str = input(f"Please input the distance {name} cycled this week in kilometers: ")
            try:
                distance = float(distance_str)
                if distance < 0:
                    print("Distance cannot be negative. Please enter a valid positive distance.")
                    continue
                distance = round(distance, 2)
                logging.debug("Module: %s, Function: %s - User input for distance: %s km", __name__, main_program.__name__, distance)
                break
            except ValueError:
                print("Invalid distance input. Please enter a numerical value (e.g., 10.5).")
                logging.warning("Module: %s, Function: %s - Invalid distance input received: %s", __name__, main_program.__name__, distance_str)

        pedal_points = 0
        calories_burned = calculate_calories(distance)
        calories_burned = round(calories_burned)
        print(f"Calories Burned for this trip: {calories_burned} kcal")
        logging.info("Module: %s, Function: %s - Calories calculated for this trip: %s kcal.", __name__, main_program.__name__, calories_burned)

        if distance < 10:
            pedal_points += 1
            logging.debug("Module: %s, Function: %s - Pedal points incremented by 1 (distance < 10km).", __name__, main_program.__name__)
        else:
            pedal_points += round(distance / 10)
            logging.debug("Module: %s, Function: %s - Pedal points incremented by distance/10 (distance >= 10km): %s points.", __name__, main_program.__name__, round(distance/10))

        price = distance * 0.25
        price = round(price * 20) / 20
        price = round(price, 2)
        logging.debug("Module: %s, Function: %s - Base price calculated: $%s", __name__, main_program.__name__, price)

        distance_ranges = [
            (9, 20), (19, 30), (29, 40), (39, 50), (49, 60), (59, 70), (69, 80), (79, 90), (89, 100), (99, 200)
        ]
        reductions = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
        reduction_applied = False
        for (lower, upper), reduction in zip(distance_ranges, reductions):
            if lower < distance <= upper:
                price -= reduction
                reduction_applied = True
                logging.debug("Module: %s, Function: %s - Price reduction of %s applied for distance range %s-%s km.", __name__, main_program.__name__, reduction, lower+1, upper)
                break
        if distance > 200:
            price = 0
            logging.debug("Module: %s, Function: %s - Price set to $0 for distance > 200km.", __name__, main_program.__name__)
        price = max(0, price)
        if price < 0:
            logging.warning("Module: %s, Function: %s - Price calculated to be negative, corrected to $0.", __name__, main_program.__name__)


        print(f"Your distance is: {distance} km")
        print(f"Your price is: ${price} SGD")
        logging.info("Module: %s, Function: %s - User distance: %s km, price: $%s.", __name__, main_program.__name__, distance, price)

        total_price = round(total_price + price, 2)
        total_distance = round(total_distance + distance, 2)

        if name in user_names:
            index = user_names.index(name)
            user_total_dist[index] += distance
            user_total_price[index] += price
            user_total_pedal_point[index] += pedal_points
            logging.debug("Module: %s, Function: %s - Existing user '%s' data updated in program memory.", __name__, main_program.__name__, name)
        else:
            user_names.append(name)
            user_total_dist.append(distance)
            user_total_price.append(price)
            user_total_pedal_point.append(pedal_points)
            logging.debug("Module: %s, Function: %s - New user '%s' data added to program memory.", __name__, main_program.__name__, name)
        index = user_names.index(name)
        user_co2_saved = user_total_dist[index] * 0.06 if name in user_names else distance * 0.06
        user_co2_saved = round(user_co2_saved)

        if pedal_points > 1:
            print(f"You have {pedal_points} pedal points ")
        else:
            print(f"You have {pedal_points} pedal point ")
        logging.info("Module: %s, Function: %s - User '%s' earned %s pedal points.", __name__, main_program.__name__, name, pedal_points)

        user_data = [name, distance, price, pedal_points, total_price, total_distance, user_co2_saved, calories_burned]

        update_google_sheets(user_data, sheet_service, google_sheet_id, google_sheets_available, debug_mode, user_data_sheet_name)

        input("\nPress Enter/↵ to continue: ")
        clear_screen()
        while True:
            iterate = input("\nWould you like to input another distance? (Y/N): ")
            if iterate.lower() in [resp.lower() for resp in yes_responses + no_responses]:
                logging.debug("Module: %s, Function: %s - User input for another distance input: %s", __name__, main_program.__name__, iterate)
                break
            else:
                print("Invalid input. Please enter Y or N.")


    if pedal_points > 99:
        free_ride_num = round(pedal_points / 100)
        if free_ride_num > 1:
            clear_screen()
            print(f"You have {free_ride_num} free rides ")
            while True:
                free_ride = input("Would you like to use 1 free ride now? (Y/N): ")
                if free_ride.lower() in [resp.lower() for resp in yes_responses + no_responses]:
                    logging.debug("Module: %s, Function: %s - User input for using free ride: %s", __name__, main_program.__name__, free_ride)
                    break
                else:
                    print("Invalid input. Please enter Y or N.")
        else:
            print(f"You have {free_ride_num} free ride ")
            while True:
                free_ride = input("Would you like to use 1 free ride now? (Y/N): ")
                if free_ride.lower() in [resp.lower() for resp in yes_responses + no_responses]:
                    logging.debug("Module: %s, Function: %s - User input for using free ride: %s", __name__, main_program.__name__, free_ride)
                    break
                else:
                    print("Invalid input. Please enter Y or N.")

        if free_ride in yes_responses:
            pedal_points -= 100
            free_ride_num -= 1
            print("Your next ride is free!")
            coupon_num = random.randint(10000000, 99999999)
            print(f"Your coupon number is {coupon_num}")
            if name == "":
                while True:
                    name = input("Please input your name: ")
                    name = name.strip()
                    if name != "":
                        break
                    else:
                        print("Name cannot be empty. Please enter your name.")
            else:
                print(f"{name} now have {free_ride_num} free rides remaining")
                input("\nPress Enter/↵ to continue: ")
            logging.info("Module: %s, Function: %s - Free ride redeemed by user '%s'. Coupon number: %s, remaining free rides: %s.", __name__, main_program.__name__, name, coupon_num, free_ride_num)


    clear_screen()
    view_stats_session = "Y" # Control session of viewing stats

    while view_stats_session in yes_responses: # Loop for stats viewing session
        view_individual_stats = "N" # Default to no individual stats for each session

        while True: # Ask if they want to view *their* individual stats
            view_individual_stats_prompt = "Would you like to view your individual stats? (Y/N): "
            view_individual_stats = input(view_individual_stats_prompt)
            if view_individual_stats.lower() in [resp.lower() for resp in yes_responses + no_responses]:
                logging.debug(f"User input for viewing individual stats: {view_individual_stats}")
                break
            else:
                print("Invalid input. Please enter Y or N.")

        if view_individual_stats in yes_responses: # If they want individual stats
            stats_email = input("Enter your email for stats verification: ")
            log_email_attempt(stats_email, "Individual Stats View - Verification Requested", None, sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name) # Log verification requested

            verification_code = generate_verification_code()
            email_sent = send_verification_email(stats_email, verification_code, email_sender, email_password, smtp_server, smtp_port)


            if email_sent:
                user_verification_code = input("Enter the verification code sent to your email: ")
                is_code_correct = user_verification_code == verification_code


                if is_code_correct:
                    log_email_attempt(stats_email, "Individual Stats View - Verification Success", "Success", sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name) # Log verification success
                    print(Fore.GREEN + "Email verified successfully for stats viewing session." + Style.RESET_ALL)
                    logging.info("Email verification successful for stats viewing session.")

                    clear_screen()
                    while True:
                        name_stats = input("Please enter your name to view your stats: ") # Specific prompt for *their* stats
                        name_stats = name_stats.strip()
                        if name_stats != "":
                            logging.debug(f"User input for name to view individual stats: {name_stats}")
                            break
                        else:
                            print("Name cannot be empty. Please enter your name.")

                    user_stats = get_user_stats_from_sheets(sheet_service, google_sheet_id, google_sheets_available, name_stats, debug_mode, user_data_sheet_name)

                    if user_stats:
                        print(f"\nStats for {name_stats}:\n")
                        print(Fore.CYAN + "-" * 30 + Style.RESET_ALL)
                        for key, value in user_stats.items():
                            print(f"{Fore.GREEN}{key}:{Style.RESET_ALL} {value}")
                        print(Fore.CYAN + "-" * 30 + Style.RESET_ALL)
                        print(f"Your coupon number is {coupon_num}")
                        logging.info(f"Individual stats displayed for user '{name_stats}'.")
                        log_email_attempt(stats_email, "Viewed Own Stats", "Stats Displayed", sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name, target_user_name=name_stats) # Log stats displayed, include target user name
                    else:
                        print("User stats not found.")
                        logging.warning(f"User stats not found for '{name_stats}' when viewing individual stats.")
                        log_email_attempt(stats_email, "Individual Stats View - Stats Not Found", "Stats Not Found", sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name, target_user_name=name_stats) # Log stats not found, include target user name

                    input("\nPress Enter/↵ to continue: ")
                    clear_screen()

                else:
                    log_email_attempt(stats_email, "Individual Stats View - Verification Failed", "Incorrect Code", sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name) # Log verification failed
                    print(Fore.RED + "Verification code incorrect. Stats viewing session cancelled." + Style.RESET_ALL)
                    logging.warning("Incorrect verification code entered for stats viewing session.")
                    view_stats_session = "N" # Cancel the entire stats viewing session
                    clear_screen()
                    continue # Skip to the next iteration of the *outer* loop, which will now terminate due to view_stats_session = "N"
            else: # Email sending failed
                log_email_attempt(stats_email, "Individual Stats View - Email Send Error", "Email Send Error", sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name) # Log email send error
                print(Fore.RED + "Email verification failed. Stats viewing session cancelled." + Style.RESET_ALL)
                logging.warning("Email sending failed for stats viewing session.")
                view_stats_session = "N" # Cancel the entire stats viewing session
                clear_screen()
                continue # Skip to the next iteration of the *outer* loop, which will now terminate due to view_stats_session = "N"

        else: # If they do *not* want individual stats, ask for another user's name
            clear_screen()
            while True:
                name_stats = input("Whose stats do you want to view? (Enter user name): ") # General prompt for any user
                name_stats = name_stats.strip()
                if name_stats != "":
                    logging.debug(f"User input for name to view another user's stats: {name_stats}")
                    break
                else:
                    print("Name cannot be empty. Please enter a user name.")

            user_stats = get_user_stats_from_sheets(sheet_service, google_sheet_id, google_sheets_available, name_stats, debug_mode, user_data_sheet_name)

            if user_stats:
                print(f"\nStats for {name_stats}:\n")
                print(Fore.CYAN + "-" * 30 + Style.RESET_ALL)
                for key, value in user_stats.items():
                    print(f"{Fore.GREEN}{key}:{Style.RESET_ALL} {value}")
                print(Fore.CYAN + "-" * 30 + Style.RESET_ALL)
                print(f"Coupon number (if available): {coupon_num}") # More general coupon message
                logging.info(f"Stats displayed for another user '{name_stats}'.")
                log_email_attempt(None, "Viewed Other User's Stats", "Stats Displayed", sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name, target_user_name=name_stats) # Log viewing other user's stats, include target user name
            else:
                print("User stats not found.")
                logging.warning(f"User stats not found for '{name_stats}' when viewing another user's stats.")
                log_email_attempt(None, "Viewed Other User's Stats", "Stats Not Found", sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name, target_user_name=name_stats) # Log stats not found for other user, include target user name


            input("\nPress Enter/↵ to continue: ")
            clear_screen()


        while True: # Ask if they want to view stats again (for another user or themselves)
            view_stats_again_prompt = "Would you like to view stats for another user? (Y/N): " # Iterative prompt
            view_stats_session = input(view_stats_again_prompt) # Control the *session* loop now
            if view_stats_session.lower() in [resp.lower() for resp in yes_responses + no_responses]:
                logging.debug(f"User input for viewing stats again: {view_stats_session}")
                break
            else:
                print("Invalid input. Please enter Y or N.")
        clear_screen()
    else:
        print("Stats viewing session ended.") # Indicate end of stats viewing

    while True:
        view_student = input("Would you like to see the full user info list (Admin)? (Y/N): ") # Clarified prompt for admin function
        if view_student.lower() in [resp.lower() for resp in yes_responses + no_responses]:
            logging.debug("Module: %s, Function: %s - User input for viewing full user info list: %s", __name__, main_program.__name__, view_student)
            break
        else:
            print("Invalid input. Please enter Y or N.")

    if view_student in yes_responses:
        admin_email = input("Enter admin email for verification: ")


        verification_code = generate_verification_code()
        email_sent = send_verification_email(admin_email, verification_code, email_sender, email_password, smtp_server, smtp_port)
        log_email_attempt(admin_email, "Admin Access - Email Sent", str(email_sent), sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name) # More descriptive action

        if email_sent:
            user_verification_code = input("Enter the verification code sent to your email: ")
            is_code_correct = user_verification_code == verification_code
            log_email_attempt(admin_email, "Admin Access - Code Verification", str(is_code_correct), sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name) # More descriptive action

            if is_code_correct:
                print(Fore.GREEN + "Email verified successfully." + Style.RESET_ALL)
                logging.info("Module: %s, Function: %s - Email verification successful for admin functions.", __name__, main_program.__name__)
                password_attempt = getpass.getpass("Please enter the admin password: ")
                if password_attempt == program_password:
                    clear_screen()
                    all_user_data = get_all_user_stats_from_sheets(sheet_service, google_sheet_id, google_sheets_available, debug_mode, user_data_sheet_name, email_log_sheet_name) # Get both datasets
                    if all_user_data and all_user_data["user_stats"]: # Check if user_stats data exists
                        user_stats_list = all_user_data["user_stats"] # Extract user_stats
                        print("Summary of all users (Sheet1):")
                        print(Fore.CYAN + "=" * 70 + Style.RESET_ALL)
                        print(f"{Fore.CYAN}|{Style.RESET_ALL:<20} | {Fore.CYAN}{'Distance (km)':<15}{Style.RESET_ALL} | {Fore.CYAN}{'Price (SGD)':<12}{Style.RESET_ALL} | {Fore.CYAN}{'Pedal Points':<12}{Style.RESET_ALL}|")
                        print(Fore.CYAN + "-" * 70 + Style.RESET_ALL)

                        for user_stat in user_stats_list:
                            print(f"| {user_stat['Name']:<20} | {user_stat['Distance (km)']:<15.2f} | ${user_stat['Price (SGD)']:<11.2f} {Style.RESET_ALL}| {user_stat['Pedal Points']:<12} |")

                        print(Fore.CYAN + "=" * 70 + Style.RESET_ALL)
                        logging.info("Module: %s, Function: %s - Full user info list from User Data Sheet displayed for admin after email and password verification.", __name__, main_program.__name__)
                    else:
                        print(f"Could not retrieve user data from Google Sheets ({user_data_sheet_name}).")
                        logging.warning(f"Module: %s, Function: %s - Could not retrieve user data from Google Sheets ({user_data_sheet_name}) when viewing full list after email and password verification.", __name__, main_program.__name__)

                    if all_user_data and all_user_data["email_log"]: # Check if email_log data exists
                        email_log_list = all_user_data["email_log"] # Extract email_log
                        print("\n\nEmail Log (EmailLog Sheet):")
                        print(Fore.CYAN + "=" * 110 + Style.RESET_ALL) # Increased width for table
                        print(f"{Fore.CYAN}| {'Email Address':<30} | {'Date and Time':<25} | {'Action Description':<35} | {'Verification Status':<15} | {'Target User Name':<20}|{Style.RESET_ALL}") # Adjusted headers and width, added "Target User Name"
                        print(Fore.CYAN + "-" * 110 + Style.RESET_ALL) # Increased width for separator
                        for log_entry in email_log_list:
                            print(f"| {log_entry['Email Address']:<30} | {log_entry['Date and Time']:<25} | {log_entry['Action Description']:<35} | {log_entry['Verification Status']:<15} | {log_entry['Target User Name']:<20}|") # Adjusted formatting, added "Target User Name"
                        print(Fore.CYAN + "=" * 110 + Style.RESET_ALL) # Increased width for table bottom border
                        logging.info("Module: %s, Function: %s - Email Log data from EmailLog displayed for admin.", __name__, main_program.__name__)
                    else:
                        print(f"Could not retrieve email log data from Google Sheets ({email_log_sheet_name}).")
                        logging.warning(f"Module: %s, Function: %s - Could not retrieve email log data from Google Sheets ({email_log_sheet_name}) when viewing full list after email and password verification.", __name__, main_program.__name__)


                    print(
                        f"\n\n\n\n\nUser stats (for admin): \n\nTotal distance travelled by all users: {total_distance} km, Total price owed by customers: ${total_price}. Coupon numbers (if any): {coupon_num}")

                    while True:
                        delete_data = input("\nWould you like to delete all user inputs? (Y/N): ")
                        if delete_data.lower() in [resp.lower() for resp in yes_responses + no_responses]:
                            logging.debug("Module: %s, Function: %s - Admin input for deleting all user inputs after email and password verification: %s", __name__, main_program.__name__, delete_data)
                            break
                        else:
                            print("Invalid input. Please enter Y or N.")

                    if delete_data in yes_responses:
                        delete_verification_code = generate_verification_code()
                        delete_email_sent = send_verification_email(admin_email, delete_verification_code, email_sender, email_password, smtp_server, smtp_port)
                        log_email_attempt(admin_email, "Data Deletion Request - Email Sent", str(delete_email_sent), sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name) # More descriptive action

                        if delete_email_sent:
                            delete_user_verification_code = input("Enter the verification code sent to your email again to CONFIRM DATA DELETION: ")
                            is_delete_code_correct = delete_user_verification_code == delete_verification_code
                            log_email_attempt(admin_email, "Data Deletion Confirmation - Code Verification", str(is_delete_code_correct), sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name) # More descriptive action

                            if is_delete_code_correct:
                                print("Deleting user inputs... ")
                                with tqdm(total=100, desc="Deleting Data", unit="%", colour='red', position=0, leave=True) as pbar_delete: # Loading bar for deletion
                                    if google_sheets_available:
                                        delete_all_inputs(sheet_service, google_sheet_id, google_sheets_available, debug_mode, user_data_sheet_name, email_log_sheet_name)
                                        logging.info("Module: %s, Function: %s - User data deletion initiated by admin after double email and password verification.", __name__, main_program.__name__)
                                    pbar_delete.update(100) # Loading bar complete
                                print(Fore.YELLOW + "Data deletion confirmed and executed." + Style.RESET_ALL)
                            else:
                                print(Fore.RED + "Data deletion verification code incorrect. Data NOT deleted." + Style.RESET_ALL)
                                logging.warning("Module: %s, Function: %s - Incorrect data deletion verification code entered. Data NOT deleted.", __name__, main_program.__name__)
                        else:
                             print(Fore.RED + "Data deletion email verification failed. Data NOT deleted." + Style.RESET_ALL)
                             logging.warning("Module: %s, Function: %s - Data deletion email verification failed. Data NOT deleted.", __name__, main_program.__name__)


                else:
                    log_email_attempt(admin_email, "Admin Access - Incorrect Password", "Incorrect Password Entered", sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name) # More descriptive action
                    print(Fore.RED + "Incorrect program password. Access denied." + Style.RESET_ALL)
                    logging.warning("Module: %s, Function: %s - Incorrect program password entered for admin access after email verification.", __name__, main_program.__name__)

            else: # Added logging for incorrect code for admin access
                log_email_attempt(admin_email, "Admin Access - Incorrect Code", "Incorrect Code Entered", sheet_service, google_sheet_id, google_sheets_available, debug_mode, email_log_sheet_name) # More descriptive action
                print(Fore.RED + "Verification code incorrect. Access denied." + Style.RESET_ALL)
                logging.warning("Module: %s, Function: %s - Incorrect verification code entered by admin.", __name__, main_program.__name__)
        else:
            print("Email verification failed. Cannot proceed to view user list." + Style.RESET_ALL)
            logging.warning("Module: %s, Function: %s - Email sending failed, admin access to user list denied.", __name__, main_program.__name__)


    co2_saved = total_distance * 0.06
    co2_saved = round(co2_saved)

    clear_screen()
    print(f"\nA total of {co2_saved}kg of CO2 was saved thanks to EcoCycle. Keep up the good work!")
    print("Thank you for using EcoCycle! ")
    logging.info("Module: %s, Function: %s - Program finished. Total CO2 saved: %s kg.", __name__, main_program.__name__, co2_saved)
    return

yes_responses = ['1', 'y', 'yes', 'Y', 'Yes', 'Yeah', 'yeah', 'Yep', 'yep', 'Yup', 'yup', 'Yea', 'yea', 'i guess',
               'I guess', 'kind of', 'Kind of', 'kinda', 'Kinda', 'maybe', 'Maybe', 'possibly', 'YES']
no_responses = ['n', 'no', 'N', 'No', 'NO', 'nah', 'Nah', 'Nope', 'nope', 'No way', 'no way', 'No way', 'not really',
              'Not really']
debug_mode = False
google_sheets_available = False

if __name__ == "__main__":
    main_program()