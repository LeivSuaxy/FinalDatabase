import psycopg2
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.timezone import now

from api.models import Producto
from api.serializer import ProductoSerializer
from .settings import DATABASES
from enum import Enum
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
import math
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.images import ImageFile
from PIL import Image
from io import BytesIO
from Backend import settings


# Aquí se declararán las clases y funciones que se encargarán
# de realizar consultas a la base de datos

class ResponseType(Enum):
    # Caso que la operacion se realizó con éxito
    SUCCESS = Response({'status': 'Success'}, status=status.HTTP_200_OK)

    # Caso en que haya dado algun error
    ERROR = Response({'status': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    # Caso que no se encuentre ningun elemento
    NOT_FOUND = Response({'status': 'Not_found'}, status=status.HTTP_404_NOT_FOUND)

    # Caso que exista ya un elemento
    EXIST = Response({'status': 'founded'}, status=status.HTTP_409_CONFLICT)

    # Caso en que exista un error interno en la base de datos
    DATABASE_ERROR = Response({'status': 'Error conectando con la base de datos'}, status=status.HTTP_400_BAD_REQUEST)

    # Caso de contraseña mal escrita
    PASSWORD_INCORRECT = Response({'status': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)


class CrudDB:
    def __init__(self):
        self.total_elements_stock = 0
        self.get_amount_elements_stock()

    # Las funciones se realizarán dependiendo de la tabla que se quiera consultar
    @staticmethod
    def connect_to_db():
        try:
            conn = psycopg2.connect(
                host=DATABASES['default']['HOST'],
                database=DATABASES['default']['NAME'],
                user=DATABASES['default']['USER'],
                password=DATABASES['default']['PASSWORD']
            )
        except psycopg2.Error as e:
            print(f'Ocurrio un error: {e}')
            return ResponseType.DATABASE_ERROR.value

        return conn

    # Function to register users
    def register_user(self, username: str, password: str) -> Response:
        """
        This method is used to register a new user in the database
        :param username: The username of the new user
        :param password: The password of the new user.
        :return:A status code indicating the result of the opeation.
                It returns 200 if the operation is successful,
                400 if there is an error,
                or 409 if the user already exists.
        """

        # Connect to the database
        connection = self.connect_to_db()

        # If the connection is unsuccessful, return an error code
        if connection == ResponseType.DATABASE_ERROR.value:
            return connection
        else:
            # Create a cursor object to execute SQL commands
            cursor = connection.cursor()

            # Execute a SQL command to check if a user with the provided username already exists in the database
            cursor.execute(f"SELECT 1 FROM auth_user WHERE username = '{username}'")

            # If the user exists, close the connection and return a code indicating that the user already exists
            user_exists = cursor.fetchone() is not None

            if not user_exists:
                # If the user does not exist, insert a new record into the auth_user table with the provided username
                # and hashed password, along with some default values for other fields.
                cursor.execute(f"""
                    INSERT INTO auth_user (password, is_superuser, username, first_name, last_name, email, is_staff,
                     is_active, date_joined) VALUES ('{password}', false, '{username}', '', '', '', false, true, now())
                """)

                # Commit the changes
                connection.commit()
                # Close the cursor and the connection
                cursor.close()
                connection.close()

                # Return a success code
                return ResponseType.SUCCESS.value
            else:
                # If the user exists, close the cursor and the connection and return a code indicating that the user
                # already exists
                cursor.close()
                connection.close()
                return ResponseType.EXIST.value

    # Function to log in users
    def log_in_user(self, username: str, password: str) -> Response:
        """
        This method is used to log in a user.


        :param username: The username of the user trying to log.
        :param password: The password provided by the user.
        :return: A status code indicating the result of the operation.
                It returns 200 if the operation is successful,
                400 if there is an error,
                or 404 if the user does not exist.
        """

        # Connect to the database
        connection = self.connect_to_db()

        # If the connection is unsuccessful, return an error code
        if connection == ResponseType.ERROR.value:
            return connection
        else:
            # Create a cursor object to execute SQL commands
            cursor = connection.cursor()

            # Execute a SQL command to check if a user with the provided username exists in the database
            cursor.execute(f"SELECT 1 FROM auth_user WHERE username = '{username}'")

            # If the user exists, close the connection and return a code indicating that the user already exists
            user_exists = cursor.fetchone() is not None

            if not user_exists:
                # If the user does not exist, close the cursor and the connection and return a code indicating that the
                # user does not exist
                cursor.close()
                connection.close()
                return ResponseType.NOT_FOUND.value
            else:
                # If the user exists, retrieve the hashed password of the user from the database
                cursor.execute(f"SELECT password FROM auth_user WHERE username = '{username}'")
                user_password = cursor.fetchone()[0]

                # Use Django's check_password function to compare the provided password with the stored hashed password
                if check_password(password, user_password):
                    # If the passwords match, close the cursor and the connection and return a success code
                    cursor.close()
                    connection.close()
                    return ResponseType.SUCCESS.value
                else:
                    # If the passwords do not match, close the cursor and the connection and return an error code
                    cursor.close()
                    connection.close()
                    return ResponseType.PASSWORD_INCORRECT.value

    # Function to get amount of elements from stock
    def get_amount_elements_stock(self) -> Response:

        # Connect to database
        connection = self.connect_to_db()

        if connection == ResponseType.ERROR.value:
            return connection
        else:
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM producto")

            self.total_elements_stock = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            return ResponseType.SUCCESS.value

    # Function to get elements from stock
    def get_elements_stock(self, pagination: int) -> Response:
        if pagination < 0:
            return ResponseType.ERROR.value

        pagination = pagination * 10

        self.get_amount_elements_stock()

        if pagination < self.total_elements_stock:
            query = ("SELECT id_producto, nombre, precio, descripcion, imagen, categoria, stock"
                     f" FROM producto LIMIT 10 OFFSET {pagination}")
            elements = Producto.objects.raw(query)

            print('imprimiento elementos')
            print(elements)

            if not elements:
                return ResponseType.NOT_FOUND.value
            else:
                serializer = ProductoSerializer(elements, many=True)
                print('imprimiendo serializer')
                print(serializer.data)
                return Response(serializer.data, status.HTTP_200_OK)
        else:
            return ResponseType.ERROR.value

    def __get_urls__(self, pagination) -> Response:
        total_page = math.ceil(self.total_elements_stock / 5)

        if 0 <= pagination <= total_page:
            if (pagination + 1) >= total_page:
                next_page = None
            else:
                next_page = f'http://localhost:8000/api/objects/?page={pagination + 1}'

            if (pagination - 1) < 0:
                previous_page = None
            else:
                previous_page = f'http://localhost:8000/api/objects/?page={pagination - 1}'

            urls = {
                'next': next_page,
                'previous': previous_page
            }

            return Response(data=urls, status=status.HTTP_200_OK)
        else:
            return ResponseType.ERROR.value

    def get_response_elements(self, pagination: int) -> Response:
        if pagination < 0:
            return ResponseType.ERROR.value

        elements = self.get_elements_stock(pagination)

        if elements == ResponseType.ERROR.value:
            return elements

        urls = self.__get_urls__(pagination)

        if urls == ResponseType.ERROR.value:
            return urls

        data = {
            'elements': elements.data,
            'urls': urls.data
        }

        return Response(data=data, status=status.HTTP_200_OK)

    # Storage CRUD
    def create_storage(self, name, location) -> Response:
        connection = self.connect_to_db()

        if connection == ResponseType.ERROR.value:
            return connection

        cursor = connection.cursor()

        check = self.__exist_storage__(name)

        if check == ResponseType.ERROR.value:
            cursor.close()
            connection.close()
            return Response({'error': 'Ya existe el nombre'}, status.HTTP_400_BAD_REQUEST)

        cursor.execute(f"INSERT INTO almacen (nombre, ubicacion) VALUES ('{name}', '{location}')")
        connection.commit()

        cursor.close()
        connection.close()
        print('Insertado en la base de datos!')

        return ResponseType.SUCCESS.value

    def __exist_storage__(self, name) -> Response:
        connection = self.connect_to_db()
        cursor = connection.cursor()

        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM almacen WHERE nombre='{name}')")

        exist_storage = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if not exist_storage:
            return ResponseType.SUCCESS.value
        else:
            return ResponseType.ERROR.value

    # Inventory CRUD
    def create_inventory(self, storage_name) -> Response:
        id_storage = self.__get_storage_id__(storage_name)

        if id_storage == ResponseType.ERROR.value or id_storage == ResponseType.NOT_FOUND.value:
            return id_storage

        id_storage = id_storage.data.get('id_value')

        print(id_storage)

        connection = self.connect_to_db()

        if connection == ResponseType.ERROR.value:
            return connection

        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO inventario (id_almacen) VALUES ('{id_storage}')")
        connection.commit()

        cursor.close()
        connection.close()

        return ResponseType.SUCCESS.value

    def __get_storage_id__(self, storage_name) -> Response:
        connection = self.connect_to_db()

        if connection == ResponseType.ERROR.value:
            return connection

        cursor = connection.cursor()

        cursor.execute(f"SELECT id_almacen FROM almacen WHERE nombre='{storage_name}'")

        id_storage = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if not id_storage:
            return ResponseType.NOT_FOUND.value
        else:
            return Response({'id_value': id_storage}, status.HTTP_200_OK)

    def get_inventories(self):
        pass

    # Product CRUD
    def insert_product(self, product_data):
        print('Entro al metodo')
        print(type(product_data))
        print(product_data)
        nombre = product_data['nombre']
        precio = product_data['precio']
        stock = product_data['stock']
        categoria = product_data['categoria']
        id_inventario = product_data['inventario']
        imagen = product_data['imagen']
        descripcion = product_data['descripcion']

        if not nombre or not precio or not stock or not categoria or not id_inventario:
            return Response({'error': 'Please provide all the required fields',
                             'mandatory_fields': 'nombre, precio, stock, categoria, inventario',
                             'optional_fields': 'descripcion, imagen'}, status=status.HTTP_400_BAD_REQUEST)

        # Processing data
        url_imagen = None
        print(type(imagen))
        if imagen is not None:
            img = Image.open(imagen)

            if img.width != 1024 and img.height != 1024:
                img = img.resize((1024, 1024))
                buffer = BytesIO()
                img.save(fp=buffer, format='PNG')
                path = default_storage.save('stock/' + imagen.name, ContentFile(buffer.getvalue()))
                url_imagen = os.path.join(path)
            else:
                path = default_storage.save('stock/' + imagen.name, ContentFile(imagen.read()))
                url_imagen = os.path.join(path)

        connection = self.connect_to_db()
        cursor = connection.cursor()

        cursor.execute(f"""
            INSERT INTO producto (nombre, precio, stock, categoria, id_inventario, descripcion, imagen, fecha_entrada)
            VALUES ('{nombre}', {precio}, {stock}, '{categoria}', {id_inventario}, '{descripcion}', '{url_imagen}', '{now()}')
        """)

        connection.commit()

        cursor.close()
        connection.close()

        return ResponseType.SUCCESS.value

    def get_product(self):
        pass

    def update_product(self):
        pass

    def delete_product(self):
        pass
