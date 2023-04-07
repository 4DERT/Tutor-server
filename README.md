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

#### /new_announcement
POST method
```json
{
  "title": "Chemia do matury",
  "content": "Szbko i skutecznie naucze cię chemii do matury.",
  "price": 32,
  "is_negotiable": true,
  "announcer_username": "pijoter",
  "subject": "chemia",
  "location": "podkarpackie"
}
```
