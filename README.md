# Tutor app server

# Enpoints
#### /
GET, return all announcments

#### /locations
GET avaible locations

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
  "title": "Chemia do matury",
  "content": "Szbko i skutecznie naucze cię chemii do matury.",
  "price": 32,
  "is_negotiable": true,
  "subject": "chemia",
  "location": "podkarpackie"
}
```

### /my_account
GET method

Returns loged user info

### /user/*username*
GET method

Returns info about given user

## To do
 - [x] user sesions and log in
 - [x] password hash
 - [ ] announcements filtering
 - [x] loged user info endpoint
 - [x] other users info endpoint
 - [ ] find better validation system, try...catch is bleh
 - [ ] and more...