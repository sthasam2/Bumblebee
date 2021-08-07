# Changelogs

## v.0.3.2.2: Profile Serializer modifications, Bug fixes

1. Modified profile serializers to display connection counts
2. Bug Fixes

## v.0.3.2.1: Bug Fixes

1.  Bug Fixes

## v.0.3.2: Removed Password Required for profile methods, Bug Fixes

1. Removed Password Required for profile methods
2. Bug Fixes

## v.0.3.1.1: Bug Fixes

1.  Bug Fixes

## v.0.3.1: Added Crosssite origin access, Bug Fixes

1. Added Crosssite origin access
2. Bug Fixes

## v.0.3: Integration of ML model, Bug Fixes

1. Integrated Machine learning model (Logreg, NaiBay) as well as the popular TextBlob
2. Bug Fixes

## v.0.2.2: Bug Fixes

1. Bug Fixes

## v.0.2.1: Bug Fixes, template View

1. Added HTML template view for Email verification
2. Bug Fixes

## v.0.2: Added Notification System, Bug Fixes, Additions, Modifications

1. Added:
   1. Notification system logic and end points
   2. Added Sensitivity Analysis app (Not completed)
   3. Added Communities Analysis app (Not completed)
   4. Added some exceptions
2. Modified:
   1.  Database Models for multiple models
   2. Modified Serializers
   3. Modified settings
3. Bug Fixes on various parts
4. Code Beautification and sorting
5. Tests: All endpoints tested

## v.0.1.10: Added Feed System, Bug fixes, Additions

1. Added Feed system API Views
2. Added persona field to Profile model for inbuilt character avatar
3. Fixed User Serializer and other bugs
4. Added DRF Pagination
5. Adjustments for connectoins. Now users cant follow/mute/block ownself.
6. Changed some endpoints.

## v.0.1.9.1: Configured ElephantSQL, Removed some dependencies

1. Configured ElephantSQl
2. Removed drf-yasg, django-heroku

## v.0.1.9: Added Connection System

1. Added Follow, Mute, Block system API Views
2. Bug Fixes, Modifications
3. Beta: Not Tested

## v.0.1.8: Added Comment System

1. Added Comment system API Views
2. Bug Fixes, Modifications
3. Beta: Not Tested

## v.0.1.7: Added Buzz, Rebuzz System

1. Added Buzz, Rebuzz system API Views
2. Bug Fixes, Modifications
3. Beta: Rebuzz (Not Tested)

## v.0.1.6: Modifications, Bug Fixes, additions

1. Modifications, Bug Fixes for User, Profile
2. Added Requirements.txt
3. Added templates for heroku, elephant (Not customized)

## v.0.1.5.1: Added Dotenv configuration, changed some logic

## v.0.1.5: Added Profile API views, logic

1. Added Django REST API for  Profile Views

   a. Profile Retrieve: Detail GET (Different for owners, public and private), Summary GET
   b. Profile Update: Update PATCH, Update Images POST, Change Private POST

2. Added some utlity functions, serializers

3. Bug Fixes, Some settings additions, Structure changes

NOTE: Documentation of API not done

## v.0.1.4: Added User API views, logic

1. Added Django REST API for  User Views

   a. User Detail GET
   b. User Update: Update PATCH, Change Password PATCH, Activate POST, Deactivate PATCH
   c. User Delete: Delete account DELETE

2. Modified user urls

NOTE: Documentation of API not done

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
