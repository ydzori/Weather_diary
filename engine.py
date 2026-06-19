import json
import os
from datetime import datetime, date


DATA_FILE = "weather_data.json"


# ===== МОДЕЛЬ ДАННЫХ (ООП) =====

class WeatherEntry:
    """Базовый класс записи о погоде."""
    
    def __init__(self, date_str, temperature, description, precipitation):
        self._date = date_str
        self._temperature = temperature
        self._description = description
        self._precipitation = precipitation
    
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = value
    
    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        self._temperature = value
    
    @property
    def description(self):
        return self._description
    
    @property
    def precipitation(self):
        return self._precipitation
    
    def to_dict(self):
        return {
            "date": self._date,
            "temperature": self._temperature,
            "description": self._description,
            "precipitation": self._precipitation,
            "type": "base"
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["date"],
            data["temperature"],
            data["description"],
            data["precipitation"]
        )
    
    def __str__(self):
        return f"{self._date} | {self._temperature}°C | {self._description} | Осадки: {self._precipitation}мм"


class SunnyWeather(WeatherEntry):
    """Солнечная погода (наследование)."""
    
    def __init__(self, date_str, temperature, description, precipitation):
        super().__init__(date_str, temperature, description, precipitation)
        self._uv_index = None
    
    @property
    def uv_index(self):
        return self._uv_index
    
    @uv_index.setter
    def uv_index(self, value):
        self._uv_index = value
    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "sunny"
        data["uv_index"] = self._uv_index
        return data
    
    @classmethod
    def from_dict(cls, data):
        entry = cls(
            data["date"],
            data["temperature"],
            data["description"],
            data["precipitation"]
        )
        entry._uv_index = data.get("uv_index")
        return entry


class RainyWeather(WeatherEntry):
    """Дождливая погода (наследование)."""
    
    def __init__(self, date_str, temperature, description, precipitation):
        super().__init__(date_str, temperature, description, precipitation)
        self._rain_intensity = None
    
    @property
    def rain_intensity(self):
        return self._rain_intensity
    
    @rain_intensity.setter
    def rain_intensity(self, value):
        self._rain_intensity = value
    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "rainy"
        data["rain_intensity"] = self._rain_intensity
        return data
    
    @classmethod
    def from_dict(cls, data):
        entry = cls(
            data["date"],
            data["temperature"],
            data["description"],
            data["precipitation"]
        )
        entry._rain_intensity = data.get("rain_intensity")
        return entry


class CloudyWeather(WeatherEntry):
    """Облачная погода (наследование)."""
    
    def __init__(self, date_str, temperature, description, precipitation):
        super().__init__(date_str, temperature, description, precipitation)
        self._cloudiness = None
    
    @property
    def cloudiness(self):
        return self._cloudiness
    
    @cloudiness.setter
    def cloudiness(self, value):
        self._cloudiness = value
    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "cloudy"
        data["cloudiness"] = self._cloudiness
        return data
    
    @classmethod
    def from_dict(cls, data):
        entry = cls(
            data["date"],
            data["temperature"],
            data["description"],
            data["precipitation"]
        )
        entry._cloudiness = data.get("cloudiness")
        return entry


# ===== МЕНЕДЖЕР ДАННЫХ =====

class WeatherDiary:
    """Менеджер записей о погоде."""
    
    def __init__(self):
        self._entries = []
        self._load()
    
    def _load(self):
        """Загрузка данных из JSON."""
        if not os.path.exists(DATA_FILE):
            self._entries = []
            return
        
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self._entries = []
            for entry_data in data.get("entries", []):
                entry_type = entry_data.get("type", "base")
                
                if entry_type == "sunny":
                    self._entries.append(SunnyWeather.from_dict(entry_data))
                elif entry_type == "rainy":
                    self._entries.append(RainyWeather.from_dict(entry_data))
                elif entry_type == "cloudy":
                    self._entries.append(CloudyWeather.from_dict(entry_data))
                else:
                    self._entries.append(WeatherEntry.from_dict(entry_data))
        except (json.JSONDecodeError, IOError):
            self._entries = []
    
    def _save(self):
        """Сохранение данных в JSON."""
        data = {
            "entries": [entry.to_dict() for entry in self._entries]
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def validate_date(self, date_str):
        """Проверка корректности даты."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def validate_temperature(self, temp):
        """Проверка корректности температуры."""
        try:
            t = float(temp)
            if t < -100 or t > 100:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    def add_entry(self, date_str, temperature, description, precipitation, 
                  weather_type="base", **kwargs):
        """Добавление новой записи."""
        if not self.validate_date(date_str):
            raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD")
        
        if not self.validate_temperature(temperature):
            raise ValueError("Температура должна быть числом от -100 до 100")
        
        try:
            precip = float(precipitation)
            if precip < 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Осадки должны быть неотрицательным числом")
        
        if weather_type == "sunny":
            entry = SunnyWeather(date_str, float(temperature), description, precip)
            entry.uv_index = kwargs.get("uv_index")
        elif weather_type == "rainy":
            entry = RainyWeather(date_str, float(temperature), description, precip)
            entry.rain_intensity = kwargs.get("rain_intensity")
        elif weather_type == "cloudy":
            entry = CloudyWeather(date_str, float(temperature), description, precip)
            entry.cloudiness = kwargs.get("cloudiness")
        else:
            entry = WeatherEntry(date_str, float(temperature), description, precip)
        
        self._entries.append(entry)
        self._save()
        return len(self._entries) - 1
    
    def delete_entry(self, index):
        """Удаление записи по индексу."""
        if index < 0 or index >= len(self._entries):
            raise ValueError(f"Запись с индексом {index} не найдена")
        self._entries.pop(index)
        self._save()
    
    def get_all_entries(self):
        """Получить все записи."""
        return self._entries
    
    def filter_by_date(self, target_date):
        """Фильтрация по дате."""
        return [e for e in self._entries if e.date == target_date]
    
    def filter_by_temperature(self, min_temp=None, max_temp=None):
        """Фильтрация по температуре."""
        result = self._entries
        if min_temp is not None:
            result = [e for e in result if e.temperature >= min_temp]
        if max_temp is not None:
            result = [e for e in result if e.temperature <= max_temp]
        return result
    
    def get_temperatures_for_chart(self):
        """Получить данные для графика."""
        dates = [e.date for e in self._entries]
        temps = [e.temperature for e in self._entries]
        return dates, temps
    
    def get_statistics(self):
        """Получить статистику."""
        if not self._entries:
            return None
        
        temps = [e.temperature for e in self._entries]
        return {
            "count": len(self._entries),
            "min_temp": min(temps),
            "max_temp": max(temps),
            "avg_temp": sum(temps) / len(temps)
        }
    