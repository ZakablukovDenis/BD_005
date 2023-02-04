import psycopg2


def create_tables():
    create = """
                CREATE TABLE IF NOT EXISTS Clients
                (id SERIAL PRIMARY KEY,
                named VARCHAR(30) NOT NULL,
                surname VARCHAR(35) NOT NULL,
                email VARCHAR(35) NOT NULL);

                CREATE TABLE IF NOT EXISTS Phones
                (id SERIAL PRIMARY KEY,
                phone BIGINT,
                client_id INTEGER REFERENCES clients(id));
            """
    cursor.execute(create)


def add_client(cl_name, cl_lastname, cl_mail):
    command = f"""INSERT INTO clients(named, surname, email) 
                VALUES('{cl_name}', '{cl_lastname}', '{cl_mail}')"""
    cursor.execute(command)


def add_phone(phone_number, id_client):
    phone_add = f"""INSERT INTO phones (phone, client_id) 
                    VALUES({phone_number}, {id_client})"""
    cursor.execute(phone_add)


def get_params():
    command = {1: 'named', 2: 'surname', 3: 'email', 4: 'id'}
    while True:
        key = int(input(
            f"Выберите колонку \n"
            f"1 - Имя; \n"
            f"2 - Фамилия;\n"
            f"3 - Email;\n"
            f"4 - ID клиента\n"
            f": "))
        if key not in command.keys():
            print("Command not found")
        break
    value = input('Введите значение: ')
    return command[key], value


def change_client(id_client, colum, value):
    change = f"""UPDATE clients 
                 SET {colum} = '{value}'
                 WHERE id = {id_client};"""
    cursor.execute(change)


def search_client():
    param = get_params()
    change = f"""SELECT * FROM clients WHERE {param[0]} = '{param[1]}'"""
    cursor.execute(change)


def delete_phone(id_client, phone_number):
    """Удаление номера телефона клиента"""
    del_number = """DELETE FROM Phones WHERE client_id=%s AND phone=%s"""
    cursor.execute(del_number, (id_client, phone_number))


def delete_client(id_client):
    """ УДАЛЕНИЕ ИНФОРМАЦИИ О КЛИЕНТЕ """
    del_phone = """DELETE FROM Phones WHERE client_id=%s"""
    cursor.execute(del_phone, [id_client])

    del_client = """DELETE FROM Clients WHERE id=%s"""
    cursor.execute(del_client, [id_client])


if __name__ == '__main__':
    try:
        '''Подключение к БД'''
        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")
        '''Курсор для выполнения операций с БД>'''
        cursor = connection.cursor()

        '''Выполнение SQL-запроса для заполнения таблицы'''

        # create_tables()
        # add_client('Edvard', 'Norton', 'edv_norton@gugle.com')
        # add_phone(89634565263, 1)
        # search_client()
        # change_client(1, "named", "Edvard")
        # delete_phone(1, 89634565263)
        delete_client(1)
        # ============================
        print("SQL-запрос успешно выполнен")
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
