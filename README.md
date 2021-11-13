# WEB EVALUATION SUITE
<hr>
This Repository contains the Web Evaluation Suite used to retrieve analytics from websites as part of the coursework of SSD.
<hr>

## PROJECT OVERVIEW :

## REQUIREMENTS :

## SYSTEM DIAGRAM :

## E-R MODEL/CLASSES (DJANGO ORM) :
TABLES:

* Users and SuperUser(admin) default present
    1. email - will be needed for email sending
* Event:
    1. id - PRIMARY KEY(Auto generated)
    2. name - String
    3. date - date
    4. starttime - time
    5. endtime - time
    6. status - completed - true not completed - false
    7. token - default null (generate through email)
* URL :
    1. id - PK
    2. url 
* Eval :
    1. id - auto generated
    2. eventid - FK
    3. url id:
## Main Structure :
* Main user creation/Admin login page: `GET`
    * User create :`POST`   -> redirect to main page
    * Login Admin : `POST`  -> redirect to admin dashboard
* Admin Dashboard : `GET`
    * Events create submenu : `GET`
    * Events calendar submenu : `GET`
    * Events modify submenu
    * Events delete submenu
    * Send email submenu(generate otp)


## Rest Endpoints for now:

1. `/accounts/` : `GET` request -> fetch admin 
2. `/accounts/login` : login user {not required}
3. `/accounts/create`: create user
4. `/accounts/admin` : login admin and redirect to dashboard
5. `/observer/`: Admin dashboard [Use Bootsrap Nav bar and footer and make a fake dashboard for now with navigation to events and email menu]
6. `/observer/event/create` : Take input to create an event entry
7. `/observer/event/modify` : Modify an existing event
8. `/observer/event/remove` : Remove the event
9. `/observer/event/display` : Display calendar
10. `/observer/event/email` : Generate otp token for test and email to user
11. `/eval/login` : authenticate otp token [Extension]
12. `/eval/entry` : Entry into db of mouseclick/heatmap [Extension]
13. `/eval/tests` : Select tests and view results [Extension]


Modify as per convinience