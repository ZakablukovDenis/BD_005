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
                VALUES(%s, %s, %s)"""
    cursor.execute(command, (cl_name, cl_lastname, cl_mail))


def add_phone(phone_number, id_client):
    phone_add = f"""INSERT INTO phones (phone, client_id) 
                    VALUES(%s, %s)"""
    cursor.execute(phone_add, (phone_number, id_client))


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


def edit_client(id_client, **kwargs):

    tuple_fields_values = tuple(zip(kwargs.keys(), kwargs.values()))
    comprehension_fields_values = [f"{x[0]} = '{x[1]}'" for x in tuple_fields_values]
    fields_values = ', '.join(comprehension_fields_values)

    change = f"""UPDATE clients 
                 SET 
                        {fields_values}
                 WHERE 
                        id = %s;"""
    cursor.execute(change, (id_client,))


def search_client(**kwargs):
    tuple_fields_values = tuple(zip(kwargs.keys(), kwargs.values()))
    comprehension_fields_values = [f"{x[0]} = '{x[1]}'" for x in tuple_fields_values]
    fields_values = ' and '.join(comprehension_fields_values)
    cursor.execute(f"""
        SELECT named, surname, email, phone
        FROM Clients c JOIN Phones p ON p.client_id = c.id
        WHERE {fields_values}
        """)

    return f"[INFO]: found successful: {cursor.fetchall()}"


def delete_phone(id_client, phone_number):  # +++
    """УДАЛЕНИЕ НОМЕРА ТЕЛЕФОНА КЛИЕНТА"""
    del_number = """DELETE FROM Phones WHERE client_id=%s AND phone=%s"""
    cursor.execute(del_number, (id_client, phone_number))


def delete_client(id_client):
    """ УДАЛЕНИЕ ИНФОРМАЦИИ О КЛИЕНТЕ """
    del_phone = """DELETE FROM Phones WHERE client_id=%s"""
    cursor.execute(del_phone, (id_client,))
    del_client = """DELETE FROM Clients WHERE id=%s"""
    cursor.execute(del_client, (id_client,))


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
        # add_client('Dave', 'Batista', 'dave_batista@gooogle.com')
        # add_phone(89634565263, 3)
        print(search_client(named='Edvard'))
        # edit_client(3, named='Edvard', email="Edv_Norton@gmail.com")
        # delete_phone(1, 89634565263)
        # delete_client(1)
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
