from engine import WeatherDiary
import matplotlib.pyplot as plt


def print_menu():
    """Вывод главного меню"""
    print("\n" + "=" * 50)
    print("  WEATHER DIARY - Дневник погоды")
    print("=" * 50)
    print("1. Показать все записи")
    print("2. Добавить запись")
    print("3. Удалить запись")
    print("4. Фильтр по дате")
    print("5. Фильтр по температуре")
    print("6. Показать график температуры")
    print("7. Статистика")
    print("8. Выход")
    print("=" * 50)


def print_entries(entries):
    """Вывод списка записей"""
    if not entries:
        print("\n️  Записей не найдено")
        return
    
    print("\n" + "-" * 70)
    print(f"{'№':<5} {'Дата':<12} {'Темп.':<8} {'Описание':<20} {'Осадки':<10}")
    print("-" * 70)
    
    for i, entry in enumerate(entries):
        print(f"{i:<5} {entry.date:<12} {entry.temperature:<8} "
              f"{entry.description:<20} {entry.precipitation}мм")
    
    print("-" * 70)
    print(f"Всего записей: {len(entries)}")


def show_all_entries(diary):
    """Показать все записи"""
    entries = diary.get_all_entries()
    print_entries(entries)


def add_entry(diary):
    """Добавить новую запись"""
    print("\n--- Добавление записи о погоде ---")
    
    date_str = input("Введите дату (YYYY-MM-DD): ").strip()
    
    temp = input("Введите температуру (°C): ").strip()
    
    description = input("Введите описание (солнечно/дождь/облачно): ").strip()
    
    precipitation = input("Введите количество осадков (мм): ").strip()
    
    print("\nТип погоды:")
    print("1. Обычная")
    print("2. Солнечная")
    print("3. Дождливая")
    print("4. Облачная")
    weather_type_choice = input("Выберите тип (1-4): ").strip()
    
    type_map = {"1": "base", "2": "sunny", "3": "rainy", "4": "cloudy"}
    weather_type = type_map.get(weather_type_choice, "base")
    
    kwargs = {}
    if weather_type == "sunny":
        kwargs["uv_index"] = input("UV-индекс: ").strip() or None
    elif weather_type == "rainy":
        kwargs["rain_intensity"] = input("Интенсивность дождя (слабый/средний/сильный): ").strip() or None
    elif weather_type == "cloudy":
        kwargs["cloudiness"] = input("Облачность (%): ").strip() or None
    
    try:
        idx = diary.add_entry(date_str, temp, description, precipitation, 
                              weather_type, **kwargs)
        print(f"\n Запись #{idx} успешно добавлена!")
    except ValueError as e:
        print(f"\n Ошибка: {e}")


def delete_entry(diary):
    """Удалить запись"""
    try:
        idx = int(input("\nВведите номер записи для удаления: ").strip())
        diary.delete_entry(idx)
        print(f" Запись #{idx} удалена")
    except ValueError as e:
        print(f" Ошибка: {e}")
    except Exception as e:
        print(f" Ошибка: {e}")


def filter_by_date(diary):
    """Фильтр по дате"""
    target_date = input("\nВведите дату для поиска (YYYY-MM-DD): ").strip()
    entries = diary.filter_by_date(target_date)
    print(f"\n Записи за {target_date}:")
    print_entries(entries)


def filter_by_temperature(diary):
    """Фильтр по температуре"""
    print("\n--- Фильтр по температуре ---")
    min_temp = input("Минимальная температура (или Enter для пропуска): ").strip()
    max_temp = input("Максимальная температура (или Enter для пропуска): ").strip()
    
    min_t = float(min_temp) if min_temp else None
    max_t = float(max_temp) if max_temp else None
    
    entries = diary.filter_by_temperature(min_t, max_t)
    print(f"\n  Записи с температурой от {min_t} до {max_t}:")
    print_entries(entries)


def show_chart(diary):
    """Показать график температуры"""
    dates, temps = diary.get_temperatures_for_chart()
    
    if not dates:
        print("\n  Нет данных для построения графика")
        return
    
    plt.figure(figsize=(10, 6))
    plt.plot(dates, temps, marker='o', linestyle='-', color='b', linewidth=2)
    plt.xlabel('Дата')
    plt.ylabel('Температура (°C)')
    plt.title('График температуры по дням')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    print("\n График построен!")


def show_statistics(diary):
    """Показать статистику."""
    stats = diary.get_statistics()
    
    if not stats:
        print("\n  Нет данных для статистики")
        return
    
    print("\n Статистика:")
    print(f"  Количество записей: {stats['count']}")
    print(f"  Минимальная температура: {stats['min_temp']}°C")
    print(f"  Максимальная температура: {stats['max_temp']}°C")
    print(f"  Средняя температура: {stats['avg_temp']:.1f}°C")


def main():
    """Главная функция"""
    print("\n Добро пожаловать в Weather Diary!")
    
    diary = WeatherDiary()
    
    while True:
        print_menu()
        choice = input("Выберите пункт меню (1-8): ").strip()
        
        if choice == "1":
            show_all_entries(diary)
        elif choice == "2":
            add_entry(diary)
        elif choice == "3":
            delete_entry(diary)
        elif choice == "4":
            filter_by_date(diary)
        elif choice == "5":
            filter_by_temperature(diary)
        elif choice == "6":
            show_chart(diary)
        elif choice == "7":
            show_statistics(diary)
        elif choice == "8":
            print("\n До свидания!")
            break
        else:
            print("\n Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
    