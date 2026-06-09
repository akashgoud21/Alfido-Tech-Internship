import requests
import json
from datetime import datetime
# -------------------------------------------------------------------
# 1. GEOCODING FUNCTION - Search city by name (filtering/search logic)
# -------------------------------------------------------------------
def search_city(city_name):
    """
    Fetches city coordinates using the Open-Meteo Geocoding API.
    Returns a list of matching city results.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 5,        # Return top 5 matches
        "language": "en",
        "format": "json"
    }

    try:
        print(f"\n[INFO] Searching for city: '{city_name}'...")
        response = requests.get(url, params=params, timeout=10)

        # Check HTTP status
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        # Handle empty results
        if "results" not in data or len(data["results"]) == 0:
            print(f"[WARNING] No city found with name '{city_name}'.")
            return None

        print(f"[SUCCESS] Found {len(data['results'])} result(s) for '{city_name}'.")
        return data["results"]

    except requests.exceptions.ConnectionError:
        print("[ERROR] No internet connection. Please check your network.")
        return None
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out. The server took too long to respond.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP Error: {e}")
        return None
    except json.JSONDecodeError:
        print("[ERROR] Failed to parse JSON response from geocoding API.")
        return None


# -------------------------------------------------------------------
# 2. WEATHER FETCH FUNCTION - Fetch weather data for given coordinates
# -------------------------------------------------------------------
def get_weather(latitude, longitude, city_name):
    """
    Fetches current weather and 7-day forecast using Open-Meteo API.
    Returns parsed weather data as a dictionary.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max",
            "weathercode"
        ],
        "timezone": "auto",
        "forecast_days": 7
    }

    try:
        print(f"\n[INFO] Fetching weather data for {city_name}...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        print(f"[SUCCESS] Weather data fetched successfully.")
        return data

    except requests.exceptions.ConnectionError:
        print("[ERROR] No internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP Error: {e}")
        return None
    except json.JSONDecodeError:
        print("[ERROR] Failed to parse JSON from weather API.")
        return None


# -------------------------------------------------------------------
# 3. HELPER - Convert WMO weather code to description
# -------------------------------------------------------------------
def decode_weather_code(code):
    """Converts WMO weather interpretation code to human-readable text."""
    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Heavy thunderstorm with hail"
    }
    return codes.get(code, f"Unknown (code {code})")


# -------------------------------------------------------------------
# 4. DISPLAY FUNCTION - Pretty print current weather
# -------------------------------------------------------------------
def display_current_weather(weather_data, city_name, country):
    """Displays current weather info from parsed JSON."""
    current = weather_data.get("current_weather", {})

    temp = current.get("temperature", "N/A")
    windspeed = current.get("windspeed", "N/A")
    weather_code = current.get("weathercode", -1)
    time_str = current.get("time", "N/A")

    print("\n" + "=" * 50)
    print(f"  CURRENT WEATHER: {city_name}, {country}")
    print("=" * 50)
    print(f"  Date/Time    : {time_str}")
    print(f"  Condition    : {decode_weather_code(weather_code)}")
    print(f"  Temperature  : {temp} °C")
    print(f"  Wind Speed   : {windspeed} km/h")
    print("=" * 50)


# -------------------------------------------------------------------
# 5. DISPLAY FUNCTION - Pretty print 7-day forecast
# -------------------------------------------------------------------
def display_forecast(weather_data):
    """Displays 7-day forecast from parsed JSON daily data."""
    daily = weather_data.get("daily", {})
    dates = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    precipitation = daily.get("precipitation_sum", [])
    wind_max = daily.get("windspeed_10m_max", [])
    codes = daily.get("weathercode", [])

    print("\n  7-DAY FORECAST:")
    print("-" * 70)
    print(f"  {'Date':<12} {'Condition':<22} {'Max':>5} {'Min':>5} {'Rain':>7} {'Wind':>8}")
    print(f"  {'':<12} {'':<22} {'(°C)':>5} {'(°C)':>5} {'(mm)':>7} {'(km/h)':>8}")
    print("-" * 70)

    for i in range(len(dates)):
        date = dates[i] if i < len(dates) else "N/A"
        condition = decode_weather_code(codes[i] if i < len(codes) else -1)
        max_t = max_temps[i] if i < len(max_temps) else "N/A"
        min_t = min_temps[i] if i < len(min_temps) else "N/A"
        rain = precipitation[i] if i < len(precipitation) else "N/A"
        wind = wind_max[i] if i < len(wind_max) else "N/A"

        print(f"  {date:<12} {condition:<22} {str(max_t):>5} {str(min_t):>5} {str(rain):>7} {str(wind):>8}")

    print("-" * 70)


# -------------------------------------------------------------------
# 6. FILTERING LOGIC - Filter days above a temperature threshold
# -------------------------------------------------------------------
def filter_hot_days(weather_data, threshold=30):
    """
    Filters and returns days where max temperature exceeds the given threshold.
    Demonstrates: Apply filtering or search logic on JSON data.
    """
    daily = weather_data.get("daily", {})
    dates = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])

    hot_days = []
    for date, temp in zip(dates, max_temps):
        if temp is not None and temp >= threshold:
            hot_days.append({"date": date, "max_temp": temp})

    return hot_days


# -------------------------------------------------------------------
# 7. SAVE JSON - Save raw API response to a JSON file
# -------------------------------------------------------------------
def save_to_json(data, filename="weather_output.json"):
    """Saves the raw JSON response to a file for reference."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"\n[INFO] Raw JSON data saved to '{filename}'")
    except IOError as e:
        print(f"[ERROR] Could not save JSON file: {e}")


# -------------------------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------------------------
def main():
    print("=" * 50)
    print("  TASK 2: API Integration & JSON Handling")
    print("  Using Open-Meteo Weather API (No API Key)")
    print("=" * 50)

    # --- STEP 1: Search for a city ---
    city_query = input("\nEnter city name to search (e.g., Hyderabad): ").strip()
    if not city_query:
        city_query = "Hyderabad"

    cities = search_city(city_query)

    if not cities:
        print("[INFO] Exiting due to no results.")
        return

    # --- STEP 2: Display search results and let user pick ---
    print("\nMatching cities:")
    for idx, city in enumerate(cities):
        name = city.get("name", "Unknown")
        country = city.get("country", "Unknown")
        state = city.get("admin1", "")
        lat = city.get("latitude", 0)
        lon = city.get("longitude", 0)
        print(f"  [{idx + 1}] {name}, {state}, {country} (lat={lat}, lon={lon})")

    # Pick first result automatically or ask user
    choice = input("\nSelect city number [default=1]: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(cities):
        choice = 1
    else:
        choice = int(choice)

    selected = cities[choice - 1]
    city_name = selected.get("name", "Unknown")
    country = selected.get("country", "Unknown")
    lat = selected.get("latitude")
    lon = selected.get("longitude")

    # --- STEP 3: Fetch weather data ---
    weather_data = get_weather(lat, lon, city_name)

    if not weather_data:
        print("[INFO] Could not retrieve weather data. Exiting.")
        return

    # --- STEP 4: Display current weather ---
    display_current_weather(weather_data, city_name, country)

    # --- STEP 5: Display 7-day forecast ---
    display_forecast(weather_data)

    # --- STEP 6: Apply filtering logic ---
    threshold = 30
    hot_days = filter_hot_days(weather_data, threshold)
    print(f"\n  Days with max temperature >= {threshold}°C:")
    if hot_days:
        for day in hot_days:
            print(f"    {day['date']} -> {day['max_temp']} °C")
    else:
        print(f"    None in the next 7 days.")

    # --- STEP 7: Save raw JSON output ---
    save_to_json(weather_data, "weather_output.json")

    print("\n[DONE] Task 2 completed successfully!\n")


if __name__ == "__main__":
    main()