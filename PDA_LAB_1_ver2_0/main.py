import json
import os
import pandas as pd
import traceback  # Для вывода ошибок
from sql_db import engine
from main2 import parse_vacancies
from save_to_db import save_vacancies

JSON_PATH = "vacancies_backup.json"


try:
    if os.path.exists(JSON_PATH):
        print("Файл JSON найден")
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            vacancies = json.load(f)

        if len(vacancies) == 0:
            print("JSON пуст. Запускаем парсер")
            vacancies = parse_vacancies()

            print("Сохраняем новые данные в JSON")
            with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=2)
        else:
            print(f"Загружено из JSON: {len(vacancies)} вакансий")
    else:
        print("JSON не найден. Запускаем парсер (main2.py)")
        vacancies = parse_vacancies()

        print("Сохраняем в JSON")
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    if vacancies:
        save_vacancies(vacancies)
        print("Данные успешно переданы в БД")
    else:
        print("Данных нет, в БД ничего не сохраняем")


    queries = {
        "Топ-10 компаний": "SELECT employer, COUNT(*) as count FROM vacancies GROUP BY employer ORDER BY count DESC LIMIT 10",
        "По опыту": "SELECT experience, COUNT(*) as count FROM vacancies GROUP BY experience",
        "Распределение по формату работы": "SELECT workformat, COUNT(*) as count FROM vacancies GROUP BY workformat ORDER BY count DESC",
        "Топ-10 городов": "SELECT address, COUNT(*) as count FROM vacancies GROUP BY address ORDER BY count DESC LIMIT 10",
        "Без зарплаты": "SELECT employer, name FROM vacancies WHERE salary = 'None' LIMIT 15"
    }

    for name, query in queries.items():
        print(f"\n--- {name} ---")
        result = pd.read_sql(query, engine)
        print(result.to_string(index=False))

except Exception as e:
    print(f"Текст ошибки: {e}")
    traceback.print_exc()