'''
Eren Çivril 20210601018
Kian Ansarinejad 20210601213
Kaan Aydın 20190601006
'''

import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from PIL import Image

default_city = "Izmir"
default_temperature_unit = "Celsius"

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Weather Application")
app.geometry("720x*480")

mainFrame = ctk.CTkFrame(app, 200, 200)

mainFrame.pack(pady=20, padx=60, fill="both", expand=True)

def load_settings():
    global default_city
    global default_temperature_unit
    with open("settings.txt", "r") as file:
        settings = file.read().splitlines()
        default_city = settings[0]
        default_temperature_unit = settings[1]

def save_settings():
    with open("settings.txt", "w") as file:
        city = chosen_city.get()
        temperature_unit = chosen_degree.get()
        file.write(city + "\n")
        file.write(temperature_unit + "\n")

try:
    load_settings()
except FileNotFoundError:
    with open("settings.txt", "w") as file:
        city = default_city
        temperature_unit = default_temperature_unit
        file.write(city + "\n")
        file.write(temperature_unit + "\n")
except Exception as e:
    print("An error occurred while loading settings:", str(e))

headers = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en",
    "Dnt": "1",
    "Sec-Ch-Ua": "\"Brave\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
}

def celsius_to_fahrenheit(celsius_list, fahrenheit_list):
    for celsius in celsius_list:
            celsius_value = float(celsius[:-1])
            fahrenheit_value = celsius_value * 9/5 + 32
            fahrenheit_list.append(f"{fahrenheit_value}°")
def show():
    try:
        city = chosen_city.get()

        url = ""

        celsius_day_temperatures = []
        celsius_night_temperatures = []

        fahrenheit_day_temperatures = []
        fahrenheit_night_temperatures = []

        day_winds = []
        night_winds = []

        day_logos = []
        night_logos = []

        for day in range(1,4):
            if city == "Izmir":
                url = f"https://www.accuweather.com/en/tr/izmir/318290/daily-weather-forecast/318290?day={day}"
                if day == 1:
                    url = "https://www.accuweather.com/en/tr/izmir/318290/current-weather/318290"
            elif city == "Ankara":
                url = f"https://www.accuweather.com/en/tr/ankara/316938/daily-weather-forecast/316938?day={day}"
                if day == 1:
                    url = "https://www.accuweather.com/en/tr/ankara/316938/current-weather/316938"
            elif city == "Istanbul":
                url = f"https://www.accuweather.com/en/tr/istanbul/318251/daily-weather-forecast/318251?day={day}"
                if day == 1:
                    url = "https://www.accuweather.com/en/tr/istanbul/318251/current-weather/318251"
            elif city == "Antalya":
                url = f"https://www.accuweather.com/en/tr/antalya/316939/daily-weather-forecast/316939?day={day}"
                if day == 1:
                    url = "https://www.accuweather.com/en/tr/antalya/316939/current-weather/316939"
            elif city == "Denizli":
                url = f"https://www.accuweather.com/en/tr/denizli/317679/daily-weather-forecast/317679?day={day}"
                if day == 1:
                    url = "https://www.accuweather.com/en/tr/denizli/317679/current-weather/317679"

            response = requests.get(url, headers=headers)

            soup = BeautifulSoup(response.text, "html.parser")

            weathers = soup.find_all('div', class_="temperature")


            for weather in weathers:
                if "Hi" in weather.text:
                    logo = str(weather.parent.find_next('svg', class_="icon")['data-src'])
                    logo = logo.replace("/images/weathericons/", "")
                    logo = logo.replace(".svg", ".png").strip()
                    day_logos.append(logo)
                    day_temperature = weather.text.replace("Hi", "").strip()
                    celsius_day_temperatures.append(day_temperature)
                elif "Lo" in weather.text:
                    logo = str(weather.parent.find_next('svg', class_="icon")['data-src'])
                    logo = logo.replace("/images/weathericons/", "")
                    logo = logo.replace(".svg", ".png").strip()
                    night_logos.append(logo)
                    night_temperature = weather.text.replace("Lo", "").strip()
                    celsius_night_temperatures.append(night_temperature)

            if len(celsius_day_temperatures) == 0:
                current_temp = soup.find('div', class_="display-temp")
                current_temperature = current_temp.text.replace("C", "").strip()
                celsius_day_temperatures.append(current_temperature)
                current_weather_info = soup.find('div', class_="current-weather-info")
                logo = current_weather_info.find_next('svg', class_="icon")['data-src']
                logo = logo.replace("/images/weathericons/", "")
                logo = logo.replace(".svg", ".png").strip()
                day_logos.append(logo)



            panel_data = soup.find_all('p', class_="panel-item")

            winds = []



            for wind in panel_data:
                if "Wind" in wind.text and "Gusts" not in wind.text:
                    wind = wind.text.strip()
                    wind = wind.replace("Wind", "").strip()
                    winds.append(wind)

            if len(winds) == 1:
                panel_data = soup.find_all('div', class_="detail-item spaced-content")
                for wind in panel_data:
                    if "Wind" in wind.text and "Gusts" not in wind.text:
                        wind = wind.text.strip()
                        wind = wind.replace("Wind", "").strip()
                        night_wind = winds[0]
                        winds.insert(0, wind)
                        winds.insert(1, night_wind)

            day_winds.append(winds[0])
            night_winds.append(winds[1])


        celsius_to_fahrenheit(celsius_day_temperatures, fahrenheit_day_temperatures)
        celsius_to_fahrenheit(celsius_night_temperatures, fahrenheit_night_temperatures)



        city_label.configure(text=city.upper())
        day1 = datetime.today()
        day2 = day1 + timedelta(1)
        day3 = day2 + timedelta(1)

        date_label1.configure(text="TODAY " + day1.strftime("%B %d, %Y"))
        date_label2.configure(text=day2.strftime("%B %d, %Y"))
        date_label3.configure(text=day3.strftime("%B %d, %Y"))


        if chosen_degree.get() == "Celsius":
            day_temperature_label1.configure(text="Current Temperature: " + celsius_day_temperatures[0])
            night_temperature_label1.configure(text="Night Temperature: " + celsius_night_temperatures[0])

            day_temperature_label2.configure(text="Day Temperature: " + celsius_day_temperatures[1])
            night_temperature_label2.configure(text="Night Temperature: " + celsius_night_temperatures[1])

            day_temperature_label3.configure(text="Day Temperature: " + celsius_day_temperatures[2])
            night_temperature_label3.configure(text="Night Temperature: " + celsius_night_temperatures[2])

        elif chosen_degree.get() == "Fahrenheit":
            day_temperature_label1.configure(text="Day Temperature: " + fahrenheit_day_temperatures[0])
            night_temperature_label1.configure(text="Night Temperature: " + fahrenheit_night_temperatures[0])

            day_temperature_label2.configure(text="Day Temperature: " + fahrenheit_day_temperatures[1])
            night_temperature_label2.configure(text="Night Temperature: " + fahrenheit_night_temperatures[1])

            day_temperature_label3.configure(text="Day Temperature: " + fahrenheit_day_temperatures[2])
            night_temperature_label3.configure(text="Night Temperature: " + fahrenheit_night_temperatures[2])

        day_wind_label1.configure(text="Current Wind: " + day_winds[0])
        night_wind_label1.configure(text="Night Wind: " + night_winds[0])

        day_wind_label2.configure(text="Day Wind: " + day_winds[1])
        night_wind_label2.configure(text="Night Wind: " + night_winds[1])

        day_wind_label3.configure(text="Day Wind: " + day_winds[2])
        night_wind_label3.configure(text="Night Wind: " + night_winds[2])


        try:
            day_icon_label1.configure(image=None)
            night_icon_label1.configure(image=None)
            day_icon_label2.configure(image=None)
            night_icon_label2.configure(image=None)
            day_icon_label3.configure(image=None)
            night_icon_label3.configure(image=None)

            day_image1 = ctk.CTkImage(Image.open("icons/" + day_logos[0]), size=(50, 50))
            day_icon_label1.configure(image=day_image1)

            night_image1 = ctk.CTkImage(Image.open("icons/" + night_logos[0]), size=(50, 50))
            night_icon_label1.configure(image=night_image1)


            day_image2 = ctk.CTkImage(Image.open("icons/" + day_logos[1]), size=(50, 50))
            day_icon_label2.configure(image=day_image2)


            night_image2 = ctk.CTkImage(Image.open("icons/" + night_logos[1]), size=(50, 50))
            night_icon_label2.configure(image=night_image2)


            day_image3 = ctk.CTkImage(Image.open("icons/" + day_logos[2]), size=(50, 50))
            day_icon_label3.configure(image=day_image3)


            night_image3 = ctk.CTkImage(Image.open("icons/" + night_logos[2]), size=(50, 50))
            night_icon_label3.configure(image=night_image3)
        except Exception as e:
            city_label.configure(text="An error occurred while fetching logos:")
            print("An error occurred while fetching logos:", str(e))

    except Exception as e:
        city_label.configure(text="An error occurred while fetching information:")
        print("An error occurred while fetching information:", str(e))



city_options = [
    "Izmir",
    "Ankara",
    "Istanbul",
    "Antalya",
    "Denizli"
]

chosen_city = ctk.StringVar()

chosen_city.set(default_city)

chosen_degree = ctk.StringVar()

chosen_degree.set(default_temperature_unit)


city_optionMenu = ctk.CTkOptionMenu(mainFrame, values=city_options, variable=chosen_city)
city_optionMenu.grid(column=1)

city_label = ctk.CTkLabel(mainFrame, text="")
city_label.grid(column=1)

date_label1 = ctk.CTkLabel(mainFrame, text="")
date_label1.grid(row=2,column=0,pady=10, padx=20)

day_icon_label1 = ctk.CTkLabel(mainFrame, text="")
day_icon_label1.grid(row=3, column=0, pady=10, padx=20)

day_temperature_label1 = ctk.CTkLabel(mainFrame, text="")
day_temperature_label1.grid(row=4,column=0,pady=10, padx=20)

day_wind_label1 = ctk.CTkLabel(mainFrame, text="")
day_wind_label1.grid(row=5,column=0,pady=10, padx=20)

night_icon_label1 = ctk.CTkLabel(mainFrame, text="")
night_icon_label1.grid(row=6, column=0, pady=10, padx=20)

night_temperature_label1 = ctk.CTkLabel(mainFrame, text="")
night_temperature_label1.grid(row=7,column=0,pady=10, padx=20)

night_wind_label1 = ctk.CTkLabel(mainFrame, text="")
night_wind_label1.grid(row=8,column=0,pady=10, padx=20)

date_label2 = ctk.CTkLabel(mainFrame, text="")

date_label2.grid(row=2,column=1,pady=10, padx=20)

day_icon_label2 = ctk.CTkLabel(mainFrame, text="")
day_icon_label2.grid(row=3,column=1,pady=10, padx=20)

day_temperature_label2 = ctk.CTkLabel(mainFrame, text="")
day_temperature_label2.grid(row=4,column=1,pady=10, padx=20)

day_wind_label2 = ctk.CTkLabel(mainFrame, text="")
day_wind_label2.grid(row=5,column=1,pady=10, padx=20)

night_icon_label2 = ctk.CTkLabel(mainFrame, text="")
night_icon_label2.grid(row=6,column=1,pady=10, padx=20)

night_temperature_label2 = ctk.CTkLabel(mainFrame, text="")
night_temperature_label2.grid(row=7,column=1,pady=10, padx=20)

night_wind_label2 = ctk.CTkLabel(mainFrame, text="")
night_wind_label2.grid(row=8,column=1,pady=10, padx=20)

date_label3 = ctk.CTkLabel(mainFrame, text="")
date_label3.grid(row=2,column=3,pady=10, padx=20)

day_icon_label3 = ctk.CTkLabel(mainFrame, text="")
day_icon_label3.grid(row=3,column=3,pady=10, padx=20)

day_temperature_label3 = ctk.CTkLabel(mainFrame, text="")
day_temperature_label3.grid(row=4,column=3,pady=10, padx=20)

day_wind_label3 = ctk.CTkLabel(mainFrame, text="")
day_wind_label3.grid(row=5,column=3,pady=10, padx=20)

night_icon_label3 = ctk.CTkLabel(mainFrame, text="")
night_icon_label3.grid(row=6,column=3,pady=10, padx=20)

night_temperature_label3 = ctk.CTkLabel(mainFrame, text="")
night_temperature_label3.grid(row=7,column=3,pady=10, padx=20)

night_wind_label3 = ctk.CTkLabel(mainFrame, text="")
night_wind_label3.grid(row=8,column=3,pady=10, padx=20)


degree_optionMenu = ctk.CTkOptionMenu(mainFrame, values=["Celsius", "Fahrenheit"], variable=chosen_degree)
degree_optionMenu.grid(column=1)

button = ctk.CTkButton(mainFrame, text="Get Information", command=show)
button.grid(column=1, pady=5)

def on_closing():
    save_settings()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)


app.mainloop()
