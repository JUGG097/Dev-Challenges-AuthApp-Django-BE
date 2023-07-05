# Authentication App Django Backend Project (The backend for the Auth App Website deployed [here](https://authapp-adeoluwa.netlify.app/))

This project was developed using `Python` v "^3.9", it runs `Django` v "^4.0.4", `Sentry-sdk` v "^1.5.11", and `Djangorestframework` v "^3.13.1" libraries.

The Auth App Website was deployed with `Netlify` link [here](https://authapp-adeoluwa.netlify.app/).

Figma design was provided by [devChallenges.io](https://devchallenges.io/).

You can clone the project and customise it at your end.

## API Documentation
*http://127.0.0.1:8000/check Endpoint (server health check)*

- METHOD: 'GET'

- SUCCESS RESPONSE (200): {'success': true}

- ERROR RESPONSE (4**, 5**): {'success': false, 'message': '***********'}


*http://127.0.0.1:8000/api/v1/auth/signup Endpoint*

- METHOD: 'POST'

- REQUEST BODY: {
  "email": "JohnDoe@gmail.com",
  "password": "ty12243fghhh",
  "provider": "LOCAL",
  }

- SUCCESS RESPONSE (200): {
  'success': true,
  'authToken': '**********',
  'refreshToken': '**********',
  'data': {}
  }

- ERROR RESPONSE (4**, 5**): {'***********'}

*http://127.0.0.1:8000/api/v1/auth/login Endpoint*

- METHOD: 'POST'

- REQUEST BODY: {
  "email": "JohnDoe@gmail.com",
  "password": "ty12243fghhh",
  "provider": "LOCAL",
  }

- SUCCESS RESPONSE (200): {
  'success': true,
  'authToken': '**********',
  'refreshToken': '**********',
  'data': {}
  }

- ERROR RESPONSE (4**, 5**): {'***********'}

*http://127.0.0.1:8000/api/v1/auth/refreshToken Endpoint*

- METHOD: 'POST'

- REQUEST BODY: {
  "refreshToken": "awerra233",
  }

- SUCCESS RESPONSE (200): {
  'success': true,
  'authToken': '**********',
  'refreshToken': '**********',
  'data': {}
  }

- ERROR RESPONSE (4**, 5**): {'***********'}

*http://127.0.0.1:8000/api/v1/user/profile Endpoint (Protected)*

- METHOD: 'GET'

- AUTHORIZATION: 'Bearer <access_token>'

- SUCCESS RESPONSE (200): {'success': true, 'data': {}}

- ERROR RESPONSE (4**, 5**): {'success': false, 'message': '***********'}

*http://127.0.0.1:8000/api/v1/user/editProfile Endpoint (Protected)*

- METHOD: 'PUT'

- AUTHORIZATION: 'Bearer <access_token>'

- REQUEST BODY: {
  "name": "JohnDoe@gmail.com",
  "bio": "ty12243fghhh",
  "image": "*****",
  "phoneNumber": 23244242,
  }

- SUCCESS RESPONSE (200): {'success': true,  'data': {}}

- ERROR RESPONSE (4**, 5**): {'success': false, 'message': '***********'}
