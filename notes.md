### Backend

- Login route stores the user token and username in session using flask sessions
- Logout route invalidates the session

### Frontend

- Users can login and logout
- App version error message will be shown on login and logout routes
- After registeration, user will be routed to login
- After login, user will be routed to user route
- If user tries to go directly to user route, they will be routed to login if not authorized

### What could be improved if not limited by time

- Add moto field to user model
- Mimic the transcription process by adding a slight delay in saving and returning response
- Encrypt/decrypt the moto using bcrypt
- Make transcription route async to handle multiple requests at the same time
