"""
Модуль для предобработки JSON-файлов с вакансиями в CSV формат.
"""

import json
from pathlib import Path

import pandas as pd


def preprocess_json(input_file_path: Path, output_file_path: Path):
    """
    Читаем json файл и переводим в csv.

    Args:
        input_file_path: Путь до JSON файла
        output_file_path: Путь для сохранения CSV файла
    """
    try:
        # Проверка входного файла
        if not input_file_path.exists():
            raise FileNotFoundError(
                f"Входной файл не найден: {input_file_path}")
        if input_file_path.suffix.lower() != '.json':
            raise ValueError(
                f"Ожидается JSON-файл, получен: {input_file_path.suffix}")

        # Основная работа
        with open(input_file_path, "r", encoding='utf-8') as f:
            data = json.load(f)

        salaries = []
        for v in data["items"]:
            salary = v.get("salary")
            vacancy_name = v.get("name")
            if salary:
                salaries.append({
                    "city": "Москва" if v["area"]["id"] == "1" else v["area"]["name"],
                    "name": vacancy_name,
                    "salary_from": salary["from"],
                    "salary_to": salary["to"],
                    "employer": v["employer"]["name"]
                })

        df = pd.DataFrame(salaries)
        df.to_csv(output_file_path, index=False, encoding='utf-8')
        print(f"Данные успешно сохранены в: {output_file_path}")

    except json.JSONDecodeError as json_error:
        print(f"Ошибка парсинга JSON: {json_error}")
        raise
    except (FileNotFoundError, ValueError) as specific_error:
        print(f"Ошибка ввода: {specific_error}")
        raise
    except KeyError as key_error:
        print(f"Отсутствует ожидаемый ключ в данных: {key_error}")
        raise
    except OSError as os_error:
        print(f"Системная ошибка ввода/вывода: {os_error}")
        raise
    except Exception as unexpected_error:  # pylint: disable=broad-except
        print(f"Неожиданная ошибка: {unexpected_error}")
        raise


if __name__ == '__main__':
    project_root = Path(__file__).parent.parent
    processed = project_root / 'data' / 'processed'
    raw = project_root / 'data' / 'raw'

    fact_path = {
        'processedNn': processed / 'nnTeacher.csv',
        'processedMo': processed / 'moTeacher.csv',
        'rawNn': raw / 'nnTeacher.json',
        'rawMo': raw / 'moTeacher.json'
    }

    preprocess_json(fact_path['rawNn'], fact_path['processedNn'])
    preprocess_json(fact_path['rawMo'], fact_path['processedMo'])
