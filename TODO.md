
# TO ADD

- [ ] show progress in relation to others as a gamification strategy
- [ ] allow easily running the services locally 
- [ ] export and import questions, classes, users, etc.
- [ ] make questions independent self-contained packages so that they are not dependent of the system. Users should be able of downloading questions, uploading in other virtual learning envs and, running autojudge independently in the context of the question. Why: if the system is discontinued, users should not lose the questions because preparing them is highly time-consuming.
- [ ] non-binary grades based on the number of tests passed. Allow setting weights to the tests.
- [ ] grades based on code quality or implementation of requirements (classes, functions, structs, etc.)
- [ ] model *types of problems* so that we can provide a system for users easily creating questions of these types.

# Backlog

- [ ] apply strip on all lines used as input in tests.
- [ ] run evaluation of submissions in parallel
- [ ] In autojudge, add CLI commands to allow re-evaluating a single question, course, student, and submission.
- [ ] In autojudge, re-evaluate only the most recent submission of each student
- [ ] As a student, view or download the submitted file.
- [ ] Delete submissions? 
- [ ] write a script to setup the test environment with some default users and questions
- [ ] Use a better logging system to avoid the need of manually controlling verbosity.
- [ ] Add types of errors when printing the result of tests in autojudge script.
- [ ] teachers should be able of adding tests in questions to check if 
        files were submitted or generated by the program and if their content  is correct.
- [ ] teachers should be able of easily writting custom evaluation scripts.
- [ ] teachers should be able of seeing students performance
- [ ] in the teacher and admin interface, present system health information (docker is running, etc.)
- [ ] Use question's creation flow in the other models.
- [ ] Drag and drop questions between sections.
- [ ] Attach files to the question description.
- [ ] Drag and drop sections to change order.
- [ ] limit memory and CPU using python subprocess when not using docker (see https://docs.python.org/3/library/resource.html))
- [ ] Import and export questions from/to BOCA.
- [ ] refactor the directory checks and processings in autojudge due to the use of docker
- [ ] Import users from file (similar to BOCA).
- [ ] Add checks for login, permissions, and groups in all views
- [ ] refactor autojudge
- [ ] Use JS in the question editor to prevent annoying page jumps.
- [ ] When user is not allowed to perform an action, it is currently redirected to the main page (courses). Redirect to the error page instead.
- [ ] Better e-mail check.
- [ ] Teachers - edit or submit new docker images to run programs.
- [ ] Process input and output tests when submitted and not when running tests.
- [ ] Write unit tests

# Known Bugs 

- [ ] Autofocus on file submission in question-detail

- [ ] In most forms, when the user (1) click in delete, (2) cancel the delete, and (3) 
click the "back" hyperlink in the form page, it returns to the delete page. This is 
a bit challenging to make right because the user can arrive in the form page from 
different pages.



