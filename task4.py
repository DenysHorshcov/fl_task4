
import re
import os

INPUT_FILE = "data.txt"
OUTPUT_FILE = "results.txt"
DELIM = r"""\s*[;:\?]\s*"""

PATTERN = re.compile(rf"""
    ^\s*
    (?P<invoice>[A-Za-z0-9]{{10}})                      
    {DELIM}
    (?P<qty>(?:0|[1-9]\d*)\.\d{{3}})                   
    {DELIM}
    (?P<name>[A-Za-z0-9_''\-]{{1,22}})                 
    {DELIM}
    (?P<cost>[+\-]?(?:\d+(?:\.\d+)?|\.\d+))            
    {DELIM}
    (?P<price>(?:0|[1-9]\d*)\.\d{{3}})                 
    {DELIM}
    (?P<pos>[1-9]\d*)                                  
    \s*$
""", re.VERBOSE)

def validate_line(line_to_check):
    match_result = PATTERN.fullmatch(line_to_check)
    if not match_result:
        return False
    else:
        return True 

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, INPUT_FILE)
    output_file_path = os.path.join(script_dir, OUTPUT_FILE)

    if not os.path.exists(input_file_path):
        print(f"[ERROR] Файл '{INPUT_FILE}' не знайдено.")
        print("Створи поруч із .py файл data.txt з рядками для перевірки.")
        return

    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            all_lines = input_file.readlines()
            lines_to_process = []
            for line in all_lines:
                stripped_line = line.strip()
                if stripped_line:  
                    lines_to_process.append(stripped_line)
    except Exception as e:
        print(f"[ERROR] Помилка читання файлу: {e}")
        return

    if len(lines_to_process) == 0:
        print("[INFO] Файл порожній.")
        return

    validation_results = []
    valid_lines_count = 0

    for line_number, current_line in enumerate(lines_to_process, 1):
        is_valid = validate_line(current_line)
        if is_valid:
            validation_results.append(f"[OK]  Рядок {line_number}: валідний")
            valid_lines_count = valid_lines_count + 1  
        else:
            validation_results.append(f"[ERR] Рядок {line_number}: не відповідає формату")

    try:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"Результати перевірки файлу '{INPUT_FILE}':\n")
            output_file.write("=" * 50 + "\n")
            
            for result in validation_results:
                output_file.write(result + "\n")
            
            output_file.write("=" * 50 + "\n")
            total_lines = len(lines_to_process)
            output_file.write(f"✅ Валідних рядків: {valid_lines_count} / {total_lines}\n")
    except Exception as e:
        print(f"[ERROR] Помилка запису файлу: {e}")
        return

    print(f"[INFO] Перевірку завершено. Результат збережено у '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()