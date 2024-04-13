from CreateDataBase import cur, conn


def get_data(table_name: str, res_column: str, asnw_column: str, answ_value: any) -> list | int | str:
    cur.execute(f'SELECT {res_column} FROM {table_name} WHERE {asnw_column} = {answ_value}')
    return cur.fetchall()


def set_data(table_name: str, res_column: str, res_value, asnw_column: str, answ_value) -> None:
    """
    Update data in the specified table with the given values based on certain conditions.

    Parameters:
    - table_name: str, the name of the table to update
    - res_column: str, the column to set the new value
    - res_value: any, the new value to set
    - asnw_column: str, the column to specify the condition
    - answ_value: any, the value to match in the condition

    Returns:
    None
    """
    cur.execute(f"UPDATE {table_name} SET {res_column} = ? WHERE {asnw_column} = ?", (res_value, answ_value))
    conn.commit()


def create_db_user(table_name: str, name: str, chatID: int) -> None:
    """
    Create a new user in the specified table if the user with the given chatID does not already exist.

    Parameters:
    - table_name: str, the name of the table to insert the user
    - name: str, the name of the user to insert
    - chatID: int, the chat ID of the user

    Returns:
    None
    """
    cur.execute(f"INSERT INTO {table_name} (name, chatID) VALUES (?, ?) ON CONFLICT DO NOTHING", (name, chatID))
    conn.commit()
