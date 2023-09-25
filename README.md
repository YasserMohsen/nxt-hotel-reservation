# Hotel Reservation System

Hotel Reservation app is a backend system for hotel room reservations

## Requirements

Python >= 3.8
pip

## Setup
1. Create a virtual environment:

    ```
    python -m venv venv
    ```

2. Activate the virtual environment:
   
    Windows:
    ```
    .\venv\Scripts\activate
    ```
    
    Linux:
    ```
    source venv/bin/activate
    ```

3. Clone the repository:

    ```shell
    git clone https://github.com/YasserMohsen/nxt-hotel-reservation.git
    ```

4. Navigate to the project directory:

    ```
    cd nxt-hotel-reservation
    ```

5. Install the project dependencies:

    ```
    pip install -r requirements/local.txt
    ```

6. Configure the environment variables by copying `.env.template` to `.env` and change whatever variables you need


7. Perform database migrations:
    ```
    python manage.py migrate
    ```

8. Create the needed groups (roles: Admin, Front Desk Agent, Guest):
    ```
    python manage.py populate_groups
    ```

9. Create a new user. Be aware that we are not relying on `is_superuser` and `is_staff` for the user's permissions, but you can initially create a user using:
    ```
    python manage.py createsuperuser
    ```
    regarding `role.id`, you can type `1` for Admin role, `2` for Front Desk Agent role, or `3` for Guest role

10. (Optional) Create some dummy RomeType and Room objects:
    ```
    python manage.py create_rooms
    ```

11. Run the application using:
    ```
    python manage.py 127.0.0.1:8000
    ```

12. Access the API documentation using one of the below:
    ```
    http://127.0.0.1:8000/api/v1/schema
    http://127.0.0.1:8000/api/v1/schema/redoc
    http://127.0.0.1:8000/api/v1/schema/swagger-ui
    ```
13. To use any request (except registration), you have to login using `http://127.0.0.1:8000/api/v1/token/` with `username` and `password`, then get the `access` token and add it with your request headers as `Authorization: Bearer {access}`. Later on, when the token expires, you can re-login or rely on the `refresh` token and send it to `http://127.0.0.1:8000/api/v1/token/refresh/` to get a new `access` token.


## Used Schema

You can find it as ERD called `NXT_Hotel_Reservation_ERD.svg`.

#### Summary
- Built-in Django User model has been extended to another CustomUser model to be used instead. This give us the felxibility in the future to add any needed fields.
- Each Reservation object has relation with a user object and a Room object, each Room has a RoomType

## Decisions
- Application is separated to two modules (apps): users and rooms. Reservations are handled within rooms app.
- RBAC is handled by creating a relation (FK) between CustomUser model and the buildt-in Django Group model. Users permission classes are handled in a sepearated module and used in views.
- JWT is used for authentication
- Each RoomType has multiple rooms and the reservation is handled in order not to conflict with reserved dates.
- No one can reserve a room in the past.

## Permissions

#### Users
- Any one (unauthenticated) can register as a Guest role, while adding users with other roles needs Admin Role
- Admin users can do all the actions on users.
- Agent users can list existing users and retrieve specific user data.
- Guest user can retrieve his own informations only

#### Room Types
- Admin users can do all the actions
- Agent users and Guest users can list all room types and retrieve details of a single type
- Unauthorized users can do nothing

#### Rooms
- Admin users can do all the actions
- Agent users can list all rooms and retrieve details of a single room
- Guest user can do see or do nothing about the rooms

#### Reservations
- Guest users can reserve a room by selecting a RoomType, and an available Room is assigned to his reservation in the background if exists
- Guest users can see their reservations
- Agent users can do all the actions with the reservations
- Updating a reservation can be done separately on dates or on the selected room.


## Testing
- Testing is applied almost on all the cases in rooms app, you can try executing them using `python manage.py test apps.rooms.tests`
- Testing is not applied yes on users app.

## Assumptions:
- using username for authentication instead of email
- no verification for user registration so far
- use sqlite3 for now for development
- no caching so far
- the user should have a role and only one role
- the guest has no permission to update his user info
- reservation cannot be updated by the guest,it should be deleted and re-created or he can request the edit from the agent
