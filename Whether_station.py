from abc import ABC, abstractmethod
from typing import List
import random

# ==========================
# Паттерн Наблюдатель
# ==========================
class Observer(ABC):
    @abstractmethod
    def update(self, data: dict):
        pass

class WeatherStation:
    def __init__(self, station_name: str):
        self.station_name = station_name
        self.sensors = []  # Датчики станции
        self.observers: List[Observer] = []  # Наблюдатели
        self.data_log = []  # История данных

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_observers(self, data):
        for observer in self.observers:
            observer.update(data)

    def collect_data(self):
        """Собираем данные с датчиков и уведомляем наблюдателей."""
        data = {}
        for sensor in self.sensors:
            data[sensor.get_type()] = sensor.get_data()
        self.data_log.append(data)  # Сохраняем данные в историю станции
        print(f"[INFO] Data from {self.station_name}: {data}")
        self.notify_observers(data)

    def get_data_log(self):
        """Возвращает историю собранных данных."""
        return self.data_log

# ==========================
# Паттерн Фабрика
# ==========================
class Sensor(ABC):
    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

class TemperatureSensor(Sensor):
    def get_data(self):
        return random.randint(10, 35)

    def get_type(self):
        return "Temperature"

class HumiditySensor(Sensor):
    def get_data(self):
        return random.randint(20, 60)

    def get_type(self):
        return "Humidity"

class PressureSensor(Sensor):
    def get_data(self):
        return random.randint(710, 780)

    def get_type(self):
        return "Pressure"

class WindSpeedSensor(Sensor):
    def get_data(self):
        return random.randint(0, 10)

    def get_type(self):
        return "WindSpeed"
    

class SensorFactory:
    @staticmethod
    def create_sensor(sensor_type: str) -> Sensor:
        if sensor_type == "Temperature" or sensor_type == "T":
            return TemperatureSensor()
        elif sensor_type == "Humidity" or sensor_type == "H":
            return HumiditySensor()
        elif sensor_type == "Pressure" or sensor_type == "P":
            return PressureSensor()
        elif sensor_type == "WindSpeed" or sensor_type == "WS":
            return WindSpeedSensor()
        else:
            raise ValueError(f"Не известный тип сенсора: {sensor_type}")

# ==========================
# Паттерн Компоновщик
# ==========================
class WeatherManager(Observer):
    def __init__(self):
        self.stations: List[WeatherStation] = []
        self.data_log = []

    def add_station(self, station: WeatherStation):
        self.stations.append(station)
        station.add_observer(self)

    def update(self, data: dict):
        """Получение данных от станций."""
        self.data_log.append(data)
        print(f"[WeatherManager] New data received: {data}")

    def save_to_file(self, filename: str):
        """Сохранение данных в файл."""
        with open(filename, "w") as file:
            for record in self.data_log:
                file.write(str(record) + "\n")
        print(f"[WeatherManager] Data saved to {filename}")

    def create_station_interactively(self):
        """Интерактивное создание станции и добавление датчиков."""
        station_name = input("Введите название станции: ")
        station = WeatherStation(station_name)

        while True:
            print("Доступные датчики: Temperature(T), Humidity(H), Pressure(P), WindSpeed(WS)")
            sensor_type = input("Введите тип датчика для добавления (или 'stop' для завершения): ").strip()
            if sensor_type.lower() == 'stop':
                break
            try:
                sensor = SensorFactory.create_sensor(sensor_type)
                station.add_sensor(sensor)
                print(f"[INFO] Датчик {sensor_type} добавлен на станцию {station_name}.")
            except ValueError as e:
                print(e)

        self.add_station(station)
        print(f"[INFO] Станция {station_name} создана и зарегистрирована.")

    def print_station_data(self):
        """Выводит данные всех станций."""
        for station in self.stations:
            print(f"\n[INFO] Data log for station {station.station_name}:")
            for record in station.get_data_log():
                print(record)

# ==========================
# Основной код
# ==========================
if __name__ == "__main__":
    # Создаем диспетчер
    manager = WeatherManager()

    while True:
        print("\nМеню:")
        print("1. Создать новую станцию")
        print("2. Собрать данные со всех станций")
        print("3. Сохранить данные в файл")
        print("4. Показать данные всех станций")
        print("5. Выйти")

        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            manager.create_station_interactively()
        elif choice == "2":
            for station in manager.stations:
                station.collect_data()
        elif choice == "3":
            filename = input("Введите имя файла для сохранения: ").strip()
            manager.save_to_file(filename)
        elif choice == "4":
            manager.print_station_data()
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор, попробуйте снова.")
