import polars as pl

def save_vacancies(vacancies_data):
    df = pl.DataFrame(vacancies_data)
    df.write_database(
        table_name="vacancies",
        connection="sqlite:///vacancies.db",
        if_table_exists="replace"
    )
    print(f" Сохранено {len(df)} вакансий")