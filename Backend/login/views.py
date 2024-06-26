from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import Token
from .serializer import UserSerializer
from Backend.crudDB import CrudDB
import psycopg2


# Create your views here.
# Register endpoint
@api_view(['POST'])
def register(request):
    """
    This view handles the registration of a new user

    It expects a POST request with 'username' and 'password' in the request data.
    If the username or password is missing, it returns a 400 error.
    If the username already exists in the database it returns a 409 error.
    If the registration is successful, it returns a 200 status.

    :param request: The request object.
    :return: A response object with the status of the operation.
    """

    # Create a new instance of the CrudDB class
    db = CrudDB()

    # Try to get the username and password from the request
    ci = request.data.get('ci')
    username = request.data.get('username')
    password = request.data.get('password')

    # If the username or password is not in the request, return a 400 error
    if username is None or password is None or ci is None:
        return Response({'error': 'Please provide a ci, username and password'}, status.HTTP_400_BAD_REQUEST)

    # Call the register_user method of the CrudDB instance with the username and password
    response: Response = db.register_user(ci=ci, username=username, password=password)

    return response


# Login endpoint
@api_view(['POST'])
def login(request):
    """
    This view handles the login of a user.

    It expects a POST request with 'username' and 'password' in the request data.
    Responses:
    If the username or password is missing, it returns a 400 error.
    If the username does not exist in the database it returns a 409 error.
    If the password does not match the stored password for the user, it returns a 400 error.
    If the login is successful, it returns a 200 status.

    :param request: The request object
    :return: A response object with the status of the operation.
    """

    # Create a new instance of the CrudDB class
    db = CrudDB()

    # Try to get the username and password from the request
    username = request.data.get('username')
    password = request.data.get('password')

    # If the username or password is not in the request, return a 400 error
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status.HTTP_400_BAD_REQUEST)

    # Call the log_in_user method of the CrudDB instance with the username and password
    response: Response = db.log_in_user(username=username, password=password)

    return response


@api_view(['POST'])
def validate_token(request):
    user = request.data.get('user')
    auth_token = request.data.get('auth_token')

    print(user)
    print(auth_token)

    if not user or not auth_token:
        return Response({'status': 'denied'}, status.HTTP_401_UNAUTHORIZED)
    print('llegamo a la base')
    db = CrudDB()
    return db.validate_token(user, auth_token)







