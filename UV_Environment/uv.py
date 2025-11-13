
import requests
from datetime import datetime
from plyer import notification
import time
from  win10toast import ToastNotifier

API_KEY = "65e6a28d426d41e0b79434da2e7564d4"
#lats, lons = 17.3850, 78.4867 for Hyderabad

def get_location():
    res = requests.get('https://ipinfo.io/json', verify=False).json()
    lat, lon = map(float, res['loc'].split(','))
    return lat, lon


def main():
    while True:
        lats, lons = get_location()
        #lats, lons = 13.0843, 80.2705
        url = f"http://api.openweathermap.org/data/2.5/uvi?lat={lats}&lon={lons}&appid={API_KEY}"
        data = requests.get(url).json()
        uv_index = data["value"]



        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lats}&lon={lons}&appid={API_KEY}&units=metric"
        weather_data = requests.get(weather_url).json()

        temp = weather_data.get("main",{}).get("temp", "N/A")
        humidity = weather_data.get("main", {}).get("humidity", "N/A")
        date = weather_data.get("dt", None)

        if date:
            dt = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S UTC')

        message = (f"Date: {dt}\n"
                   f"UV Index: {uv_index}\n"
                   f"Temperature: {temp}°C\n"
                   f"Humidity: {humidity}%")
        


        # if uv_index >= 6:
        #     notification.notify(
        #         title = "High UV Alert ⚠️",
        #         message = message,
        #         app_icon = r"C:\Users\sai.gandlapalli\OneDrive - ION\Desktop\UV_Environment\2025-11-13_11h59_52.ico",
        #         timeout = 15
        #     )


        if uv_index >= 6:
            toaster = ToastNotifier()
            toaster.show_toast("High UV Alert ⚠️", message, icon_path= r"C:\Users\sai.gandlapalli\OneDrive - ION\Desktop\UV_Environment\2025-11-13_11h59_52.ico", duration = 15)
        time.sleep(86400)

if __name__ == "__main__":
    main()