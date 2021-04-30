# Changelogs

## v.0.1.3: Added User API views, logic

1. Added Django REST API for  

   a. Logout
   b. Email Verification: Sending emails POST, confirming verifications GET
   c. Resetting Password: Sending emails GET, confirming verification POST

2. Renamed API documentation endpoints using drf-yafg  

   a. api/docs/redoc
   b. api/docs/swagger

## v.0.1.2: Added Apps, Models, API, Increased Dependencies

1. Apps: Added apps chats, comments, core. Modified users.  
2. Users: Added exceptions, urls, utils, and apis  
3. Added Django REST API for  

   a. Register
   b. Login (JWT Authentication using djangorestframework_simplejwt)

4. Added API documentation endpoints using drf-yafg  

   a. api/redoc-docs
   b. api/swagger-docs

5. Added some dependencies
6. Added `definitions.py` for commonly used definitions i.e. setting values
7. Added some linux scripts for speedy workflow

## v.0.1.1: Added Apps, Database modelling

1. Added apps: buzzes, notifications
2. Database schema made via models
3. Minor file changes

NOTE: INCOMPLETE PHASE

## v.0.1.0: Initial Repository

1. Django backend template
2. Configured Postgres
3. Customized User model
