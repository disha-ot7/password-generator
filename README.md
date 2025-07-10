Advanced Password Generator :
A FastAPI-based microservice that generates, analyzes, and checks passwords against real-world data breaches using the Have I Been Pwned API. Built with security and flexibility in mind.
🚀 Features
✅ Generate strong random passwords
✅ Customize length, digits, symbols, uppercase/lowercase
✅ Analyze strength using zxcvbn
✅ Check if the password is pwned (leaked) using HIBP
✅ Built with FastAPI + Swagger UI
✅ Easy to deploy as a microservice

Query Parameters:
| Name        | Type    | Default | Description                |
| ----------- | ------- | ------- | -------------------------- |
| `length`    | integer | 16      | Password length (8–64)     |
| `digits`    | bool    | true    | Include digits             |
| `symbols`   | bool    | true    | Include special characters |
| `uppercase` | bool    | true    | Include uppercase letters  |
| `lowercase` | bool    | true    | Include lowercase letters  |
Example:
GET /generate?length=20&symbols=false
📤 Response:
{
  "password": "T6nDxN4zQdM2c7gR8YfK",
  "strength": 4,
  "pwned": false,
  "pwned_count": 0
}
🧪 POST /analyze
Analyze and check a given password.
📥 Body:
{
  "password": "password123"
}
📤 Response:
{
  "password": "password123",
  "strength": 0,
  "pwned": true,
  "pwned_count": 6141973
}




