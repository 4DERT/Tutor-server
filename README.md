# Tutor app server

# Enpoints
#### / or /announcements
GET, return all announcments

You can filter announcements by adding GET parameters like:
```
?subject=matematyka
```
You can add multiple filters joing them using '&':
```
?subject=informatyka&price_from=10
```

All avaible filters:
 - price_from
 - price_to
 - subject
 - degree_course
 - semester
 - is_negotiable
 - date_posted_from
 - date_posted_to

Date format is: YYYY-mm-dd

You can also sort by price or date using:
```
?price_sort=asc
```
```
?date_sort=desc
```

#### /sign_up
POST method
```json
{
    "username": "pijoter",
    "email": "pjoter12@demo.com",
    "password": "qwerty",
    "name": "Piotr",
    "surname": "Kowalski",
    "phone": "213742069"
}
```

### /login
POST method

user can be either an email or username
```json
{
    "user": "pjoter12@demo.com",
    "password": "qwerty"
}
```

### /logout
GET method


#### /new_announcement
POST method
```json
{
  "title": "Ucze jak robić równania różniczkowe",
  "content": "fajny opis",
  "price": 120,
  "is_negotiable": false,
  "degree_course": "informatyka",
  "subject": "matematyka",
  "semester": 4
}
```

#### /announcements/*id*
GET, PUT, DELETE methods

You can edit announcement using PUT method (the same json as in [new_announcement](#new_announcement))

### /my_account  
GET, PUT, DELETE method

Returns logged user info.

To edit account use PUT method with following json:
```json
{
    "description": "Fajny. młody, ciekawy a co najważniejsze przystojny chłopak",
    "email": "4DERT@demo.com",
    "name": "Jarosław",
    "phone": "213742071",
    "surname": "Jarząbkowski",
    "semester": 4,
    "degree_course": "informatyka"
}
```

### /my_account/avatar
GET, PUT, DELETE methods

This endpoint returns base64 encoded image (png or jpg)
To send avatar use PUT method (couse default is NULL) and use form-data with key named 'file'.
Avatar must be either PNG or JPEG, max size 512 x 512 px

### /user/*username*
GET method

Returns info about given user


### /user/*username*/review
POST, PUT, DELETE methods
```json
{
  "rate": 5,
  "review": "Fajny korepetytor"
}
```

### /user/*username*/avatar
GET methods
Returns base64 encoded image (png or jpg)

### /subjects
GET method

Returns all subjects

### /degree_courses
GET, POST method

Returns all degree_courses

To add degree courses use POST with following JOSN:
```json
{
  "degree_course": "informatyka"
}
```
This method is only available for admin

### /degree_courses/*degree_course*
GET, PUT, DELETE method

GET - returns more detailed degree course data

PUT, DELETE - this methods are only available for admin, PUT uses the same JSON as [degree_courses](#degree_courses)

### /new_subject
POST method
```json
{
  "subject": "matematyka",
  "degree_course": "informatyka",
  "semester": 1
}
```
This method is only available for admin

# Application settings
You can configure an app secret key and admin usernames in `.env` file:
```.env
SECRET_KEY="KEY"
ADMINS=4DERT,pablo
```

# To do
 - [x] user sesions and log in
 - [x] password hash
 - [x] announcements filtering
 - [x] loged user info endpoint
 - [x] other users info endpoint
 - [x] find better validation system, try...catch is bleh
 - [x] find way to store user avatars in the db
 - [x] announcements sorting
 - [x] add ratings and reviews about users
 - [x] store SECRET_KEY in .env
 - [x] announcements editing
 - [x] announcements deleting
 - [x] reviews editing
 - [x] reviews deleting
 - [x] account editing
 - [x] account deleting
 - [ ] subjects editing
 - [ ] subjects deleting
 - [x] degree course editing
 - [x] degree course deleting
 - [ ] add endpoint to change password
 - [ ] and more...
