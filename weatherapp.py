import sys
import requests
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QPushButton,QLabel,QLineEdit
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter your city : ",self)
        self.city_input=QLineEdit(self)
        self.button = QPushButton("Get Weather", self)
        self.temp_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.description_label=QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WeatherApp")
        self.setGeometry(600,250,600,400)

        vbox=QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.button.setObjectName("button")
        self.temp_label.setObjectName("temp")
        self.emoji_label.setObjectName("emoji")
        self.city_input.setObjectName("input")

        self.setStyleSheet("""
        QLabel{font-weight:bold;
               font-family:calibri;
               padding:20px;
               font-size:40px
        }
        QLineEdit#input{
              font-size:40px;
              font-weight:bold;
        }

        QPushButton#button{font-weight:bold;
                   font-family:Arial;
                   font-size:40px;
                   border:3px solid;
                   border-radius:15px;
        }
        QLabel#temp{
               font-size:75px;
        }
        QLabel#emoji{
               font-size:100px;
               font-style:segoe UI emoji;
        }
        """)

        self.button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "fc24414a41359369152d448a3f148f7d"
        city = self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        response=requests.get(url)

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")


    def display_error(self,message):
        self.temp_label.setStyleSheet("font-size: 30px;")
        self.temp_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()


    def display_weather(self,data):
        self.temp_label.setStyleSheet("font-size: 75px;")
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        # temp_f = (temp_k * 9 / 5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temp_label.setText(f"{temp_c:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "⛈️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌁"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌬️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""



if __name__ == "__main__":
    app=QApplication(sys.argv)
    weather_app=WeatherApp()
    weather_app.show()
    sys.exit(app.exec())
