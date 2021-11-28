# WEB EVALUATION SUITE
<hr>
This Repository contains the Web Evaluation Suite used to retrieve analytics from websites as part of the coursework of SSD.
<hr>

## PROJECT OVERVIEW :
The main goal of our tool is to evaluate the usability of a test website by generating heatmaps. 
Heatmap is essentially placed on top of an existing website so that developers/admins can view which areas are frequently accessed in a website so that they can use this information to improve their website.

### E-R MODEL/CLASSES (SQLALCHEMY ORM) :
TABLES:
* Users
    1. id - PK
    2. username - String(unique)
    3. email - will be needed for email sending
    4. firstname - String
    5. lastname - String
    6. password - String
    7. isadmin - Boolean
* Event:
    1. id - PRIMARY KEY(Auto generated)
    2. name - String
    3. start - time
    4. end - time
    5. status - COMPLETED - true NOTCOMPLETED - false
    6. url
* coordinates :
    1. id - event id
    2. x - xth pos
    3. y - yth pos
### Main Structure (Pages):
* Main user creation/Admin login page: `GET`
    * User create :`POST`   -> redirect to main page
    * Login Admin : `POST`  -> redirect to admin dashboard
* Admin Dashboard : `GET`
    * TEST(Eval) RESULTS
    * Events create submenu : `POST`
    * Events calendar submenu : `GET`
    * Events modify submenu : `PUT`
    * Events delete submenu : `DELETE`
    * Send email submenu(generate otp): `POST`
### Structure (Extension):
* Admin/User login page:
    * Admin Login:
        * Enter event id -> View Heatmap
    * User OTP login -> load url -> Mouse click capture
### Rest Endpoints for now:

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
### Javascript tasks :
1. Reading the mouse click location and sending it to `/eval/entry`
2. Fetching the mouse click data from db and display it in heatmap `/eval/tests`

## Whiteboard link : 
https://wbd.ms/share/v2/aHR0cHM6Ly93aGl0ZWJvYXJkLm1pY3Jvc29mdC5jb20vYXBpL3YxLjAvd2hpdGVib2FyZHMvcmVkZWVtLzcyNzVmYWJiMjU0MjQwMjY5OTNiZjJkM2VlZGI2ZTRhXzAzMWEzYmJjLWNmN2MtNGUyYi05NmVjLTg2NzU1NTU0MGExY19iYTcxY2IwMy01MmJkLTQyYjctODU1MS1hMTc3N2ExYjlmMjA=

### Useful git commands:[only update readme on master -> no other files]
1. Creating a new branch: `git branch <BRANCH_NAME>`
2. Moving to the branch : `git checkout <BRANCH_NAME>` Shortcut in one command : `git checkout -b <BRANCH_NAME>`
3. Staging the changes: `git add --all`
4. Commiting the changes: `git commit -m "message" ` :Write 2-3 lines about your work in the message
5. Creating remote branch: `git push -u origin <BRANCH_NAME>` (do it only once after that use git push)
6. Pushing to remote branch : `git push`
7. Update your current branch with changes from master : `git rebase master` (This will bring all the commits from master into your branch)[Just during push use --force in your branch]
8. Taking a particular commit from one branch to another : `git cherry-pick <commit-hash>`
