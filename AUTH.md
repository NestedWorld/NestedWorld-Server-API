Authentication flow
===================

## Login

`POST /v1/user/auth/login/simple`

Login a user with a email/password pair and the application token (used to identify the application with which the user is connected).

Params (Form body):
- `email`: User email (required)
- `password`: User password (required)
- `app_token`: Application token (given by the mighty admin) (required)
- `data`: Additional data associated with this session, as a JSON-encoded object (optional)

Output (JSON object):
- `token`: The session token!

## Requests

When you got the session token, you must pass it to *every* requests which require a session in the header field `Authorization` with the following format `Bearer <session token>`.

## Logout

`GET /v1/user/auth/logout`

Logout a user, in fact it just end the current session (and forbid any following requests with the session token)

> This request require a valid session, you must pass the session token as described in `Requests`
