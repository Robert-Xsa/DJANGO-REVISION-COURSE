---
subtitle: A practical explanation of Django's major elements, how they
  work together, and how to use them in real projects
title: The Complete Django Guide
---

# The Complete Django Guide

A practical learning reference for developers who want to understand
Django and write code manually.

**Practical example:** A School Management System with student
registration and CRUD operations.

## 1. What is Django?

Django is a Python web framework used to build secure, maintainable,
database-driven websites and applications. It includes tools for URL
routing, database access, forms, authentication, administration,
security and testing.

Examples include school, hospital, inventory, e-commerce, apartment
management and financial systems, as well as REST APIs.

### Django's MVT architecture

Django commonly follows the Model--View--Template (MVT) pattern:

  -----------------------------------------------------------------------
  Part                    Responsibility          School-system example
  ----------------------- ----------------------- -----------------------
  Model                   Defines data structure  A Student table with
                          and database            name, student ID and
                          relationships.          age.

  View                    Processes requests,     Retrieves students or
                          applies logic and       saves a registration
                          prepares a response.    form.

  Template                Displays information to An HTML page showing
                          the user.               the student list.
  -----------------------------------------------------------------------

Typical request flow: **Browser request → URL pattern → view →
model/database as needed → template → HTTP response.** A view can also
return JSON or a redirect instead of rendering a template.

## 2. Create a Django project and application

``` bash
python3 -m venv myenv
source myenv/bin/activate
pip install django

django-admin startproject school_system
cd school_system
python manage.py startapp students
```

A **project** is the complete website and its configuration. An
**application** is a component that handles a particular area of
functionality. A school project might contain `students`, `teachers`,
`attendance`, `examinations` and `fees` apps.

Register the app in `school_system/settings.py`:

``` python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'students',
]
```

## 3. Understanding the project files

  -----------------------------------------------------------------------
  File or folder                      Purpose
  ----------------------------------- -----------------------------------
  `manage.py`                         Runs Django management commands.

  `settings.py`                       Configures apps, database,
                                      templates, middleware, static files
                                      and security.

  Project `urls.py`                   Main URL routing configuration.

  `asgi.py`                           ASGI application entry point.

  `wsgi.py`                           WSGI application entry point.

  `models.py`                         Defines database models.

  `views.py`                          Contains request-handling and
                                      application logic.

  `admin.py`                          Registers and customizes models in
                                      Django admin.

  `apps.py`                           Application configuration.

  `tests.py`                          Automated tests.

  `migrations/`                       Database schema change history.
  -----------------------------------------------------------------------

A growing project may also contain app-specific `templates/`,
`forms.py`, `urls.py`, static assets, uploaded media, tests and
configuration files.

## 4. `manage.py`

`manage.py` is the command-line entry point for operating a Django
project.

  --------------------------------------------------------------------------
  Command                                What it does
  -------------------------------------- -----------------------------------
  `python manage.py runserver`           Starts the local development
                                         server.

  `python manage.py startapp students`   Creates an application.

  `python manage.py makemigrations`      Creates migration files from model
                                         changes.

  `python manage.py migrate`             Applies migrations to the database.

  `python manage.py createsuperuser`     Creates an administrator account.

  `python manage.py shell`               Opens an interactive Django Python
                                         shell.

  `python manage.py test`                Runs automated tests.
  --------------------------------------------------------------------------

## 5. `settings.py`

`settings.py` controls how the project behaves. It contains
configuration for installed applications, database connections,
templates, middleware, static files, media files, language, time zone
and security.

### Database configuration: SQLite example

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

SQLite is convenient for learning and small deployments. PostgreSQL is
commonly preferred for larger production applications.

### Project-level templates

``` python
TEMPLATES = [
    {
        # Other generated settings remain here.
        'DIRS': [BASE_DIR / 'templates'],
        # ...
    },
]
```

The project-level `templates` directory is useful for shared pages such
as `base.html`, `login.html` and `dashboard.html`. App-specific
templates can live inside each app.

### Static and media files

``` python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Static files are assets supplied with the application, such as CSS,
JavaScript, logos and icons. Media files are uploaded by users, such as
photographs, certificates and documents. Production media storage should
be configured deliberately.

### Production security settings

-   Set `DEBUG = False`.
-   Configure `ALLOWED_HOSTS`.
-   Keep `SECRET_KEY` and database credentials outside source code using
    environment variables.
-   Use HTTPS.
-   Configure secure cookies and trusted origins appropriately.

## 6. `models.py`: database structure

A model is a Python class that Django maps to a database table. Model
fields define the columns and their data types.

``` python
from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=30, unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.first_name
```

### Common model fields

  Field               Typical use
  ------------------- -------------------------------------------------
  `CharField`         Short text, names, codes and labels.
  `TextField`         Long descriptions or addresses.
  `IntegerField`      Whole numbers.
  `DecimalField`      Precise decimal values such as prices and fees.
  `FloatField`        Floating-point measurements where suitable.
  `BooleanField`      True/false values.
  `DateField`         A calendar date.
  `DateTimeField`     Date and time.
  `EmailField`        Email address with email-format validation.
  `ImageField`        Uploaded image; requires Pillow.
  `FileField`         Uploaded files.
  `ForeignKey`        Many records related to one parent record.
  `OneToOneField`     One-to-one relationship.
  `ManyToManyField`   Many records related to many other records.

### Model relationships

``` python
class SchoolClass(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT
    )
```

Many students can belong to one `SchoolClass`.
`on_delete=models.PROTECT` prevents deleting a class while students
still refer to it. Other choices include `CASCADE`, `SET_NULL` (with
`null=True`) and `SET_DEFAULT`, depending on business rules.

Use `unique=True` for values that must not repeat. Use `null` and
`blank` thoughtfully: `null` controls database storage, while `blank`
controls validation. Add model validation and database constraints for
important business rules.

## 7. Migrations

Migrations are versioned instructions for changing the database schema
to match your models.

``` bash
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` generates migration files. `migrate` applies them. When
you add a field, change a field type or create a model, inspect the
generated migration and then apply it. Commit migration files to version
control.

## 8. `urls.py`: URL routing

URL patterns connect web addresses to views. The main project `urls.py`
can include URL configurations from individual apps.

``` python
# school_system/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
]
```

Create `students/urls.py`:

``` python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.student_create, name='student_create'),
    path('<int:id>/edit/', views.student_update, name='student_update'),
    path('<int:id>/delete/', views.student_delete, name='student_delete'),
]
```

The `<int:id>` converter captures an integer from the URL and passes it
to the view. Use named URLs in templates and redirects instead of
hardcoding paths.

## 9. `views.py`: application logic

A view receives an `HttpRequest` and returns an `HttpResponse`. It may
retrieve records, validate input, check permissions, save data, render a
template or redirect the user.

``` python
from django.shortcuts import render
from .models import Student

def student_list(request):
    students = Student.objects.all()
    return render(
        request,
        'students/list.html',
        {'students': students}
    )
```

`Student.objects.all()` retrieves the records. `render()` loads the
template and supplies a context dictionary. A view can also return
`JsonResponse`, `HttpResponse` or `redirect()`.

## 10. Templates: HTML and Django Template Language

Templates are HTML files with Django Template Language (DTL) expressions
and tags. A common app template location is
`students/templates/students/list.html`.

``` html
<h1>Registered Students</h1>

<a href="{% url 'student_create' %}">Add Student</a>

<table>
  <tr><th>Name</th><th>Student ID</th></tr>
  {% for student in students %}
    <tr>
      <td>{{ student.first_name }}</td>
      <td>{{ student.student_id }}</td>
    </tr>
  {% empty %}
    <tr><td colspan="2">No students registered.</td></tr>
  {% endfor %}
</table>
```

### Common template syntax

  Syntax                           Meaning
  -------------------------------- ----------------------------------------
  `{{ variable }}`                 Displays a value.
  `{% for item in items %}`        Loops through a collection.
  `{% if condition %}`             Conditional rendering.
  `{% url 'name' %}`               Resolves a named URL.
  `{% csrf_token %}`               Adds a CSRF token to a form.
  `{% extends 'base.html' %}`      Inherits a parent template.
  `{% block content %}`            Defines a replaceable template block.
  `{% include 'partial.html' %}`   Includes another template fragment.
  `{% load static %}`              Loads the static template tag library.

### Template inheritance

``` html
<!-- templates/base.html -->
<!doctype html>
<html>
<head>
    <title>{% block title %}School{% endblock %}</title>
</head>
<body>
    <nav>School Management System</nav>
    <main>{% block content %}{% endblock %}</main>
</body>
</html>
```

``` html
<!-- students/templates/students/list.html -->
{% extends 'base.html' %}

{% block title %}Students{% endblock %}

{% block content %}
    <h1>Students</h1>
{% endblock %}
```

Template inheritance prevents repeating the same navigation, header and
footer on every page.

## 11. `forms.py`: receiving and validating user input

Django has `forms.Form` for manually defined forms and `forms.ModelForm`
for forms based on a model. `ModelForm` is especially useful for CRUD
applications.

``` python
# students/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'student_id',
            'age',
            'gender',
        ]
```

`ModelForm` creates fields based on the model. The `fields` list
controls which model fields users may edit. Forms also support widgets,
labels, help text, custom `clean` methods and validators.

### Create view and template

``` python
# students/views.py
from django.shortcuts import render, redirect
from .forms import StudentForm

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(
        request,
        'students/create.html',
        {'form': form}
    )
```

``` html
<!-- students/templates/students/create.html -->
<h1>Register Student</h1>
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save Student</button>
</form>
```

-   **GET** displays an empty form.
-   **POST** submits data.
-   `is_valid()` runs validation.
-   `save()` writes the record.
-   `redirect()` sends the browser to another page.

Always include CSRF protection in internal POST forms.

## 12. `admin.py`: built-in administration

Django admin provides a generated interface for trusted staff to manage
registered models.

``` python
# students/admin.py
from django.contrib import admin
from .models import Student

admin.site.register(Student)
```

Create an administrator and start the server:

``` bash
python manage.py createsuperuser
python manage.py runserver
```

Open `/admin/` in your browser and sign in. You can add, edit and delete
records. For a more polished admin, use `ModelAdmin` to configure
`list_display`, `search_fields`, `list_filter` and `ordering`. The admin
is an internal management tool, not necessarily a replacement for the
application's own user interface.

## 13. Django ORM: database operations

ORM stands for Object-Relational Mapper. It lets Python code query and
update the database without manually writing SQL for common operations.

  ------------------------------------------------------------------------------------------------------------------------------------------------
  Task                                Example
  ----------------------------------- ------------------------------------------------------------------------------------------------------------
  Create                              `Student.objects.create(first_name='John', last_name='Peter', student_id='STU002', age=19, gender='Male')`

  Retrieve all                        `Student.objects.all()`

  Get one                             `Student.objects.get(id=1)`

  Filter                              `Student.objects.filter(gender='Male')`

  Search text                         `Student.objects.filter(first_name__icontains='john')`

  Update                              `student = Student.objects.get(id=1); student.age = 21; student.save()`

  Delete                              `student = Student.objects.get(id=1); student.delete()`

  Count                               `Student.objects.count()`
  ------------------------------------------------------------------------------------------------------------------------------------------------

`get()` raises `DoesNotExist` if no matching record exists and
`MultipleObjectsReturned` if more than one record matches. In web views,
`get_object_or_404(Student, pk=id)` is often a safer way to return a 404
page when a record is missing.

### Useful ORM tools

  -----------------------------------------------------------------------
  Tool                                Use
  ----------------------------------- -----------------------------------
  `Q` objects                         Build complex OR/AND query
                                      conditions.

  `F` expressions                     Refer to database field values in
                                      database-side updates.

  `aggregate()`                       Calculate totals, averages and
                                      other summary values.

  `annotate()`                        Add calculated values to each
                                      result.

  `select_related()`                  Fetch ForeignKey/OneToOne related
                                      objects efficiently.

  `prefetch_related()`                Efficiently fetch many-to-many and
                                      reverse relationships.

  `order_by()`                        Sort query results.

  `values()`                          Return dictionaries of selected
                                      fields.
  -----------------------------------------------------------------------

## 14. Complete CRUD: Create, Read, Update and Delete

CRUD is the foundation of many database applications.

  ----------------------------------------------------------------------------
  Operation               Purpose                 Typical Django approach
  ----------------------- ----------------------- ----------------------------
  Create                  Add a new record.       ModelForm + `form.save()`

  Read                    Display records.        QuerySet such as
                                                  `Model.objects.all()`

  Update                  Change an existing      ModelForm with
                          record.                 `instance=existing_object`

  Delete                  Remove a record.        Delete after an authorized
                                                  POST confirmation.
  ----------------------------------------------------------------------------

### Update view

``` python
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from .models import Student

def student_update(request, id):
    student = get_object_or_404(Student, pk=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'students/update.html',
        {'form': form}
    )
```

### Delete view

``` python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student

def student_delete(request, id):
    student = get_object_or_404(Student, pk=id)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    return render(
        request,
        'students/delete.html',
        {'student': student}
    )
```

``` html
<!-- students/templates/students/delete.html -->
<h2>Delete Student</h2>
<p>Are you sure you want to delete {{ student.first_name }}?</p>
<form method="POST">
    {% csrf_token %}
    <button type="submit">Confirm Delete</button>
</form>
```

Do not delete records through a GET request. Require POST confirmation,
and check that the logged-in user is authorized to delete that
particular record. Consider soft deletion or archival where records must
be retained.

## 15. Authentication, authorization and permissions

Authentication verifies who a user is. Authorization determines what the
user is allowed to do. Django includes user accounts, password hashing,
login/logout support, groups and permissions.

### Simplified login example

``` python
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('student_list')

    return render(request, 'login.html')
```

### Protect a view

``` python
from django.contrib.auth.decorators import login_required

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(
        request,
        'students/list.html',
        {'students': students}
    )
```

For a real login system, also provide clear error messages, logout,
password reset, rate limiting where appropriate, and permission checks.
Use Django's built-in authentication views or carefully implement the
complete flow rather than relying only on the simplified example above.

  Role            Possible responsibility
  --------------- ----------------------------------------
  Administrator   Manages the whole school system.
  Teacher         Manages permitted academic records.
  Accountant      Manages fees and payment records.
  Student         Views their own permitted information.

Use groups and model permissions, and enforce object-level access rules
in server-side code. Hiding a button in HTML is not security.

## 16. Middleware

Middleware is a request/response processing layer that runs around view
execution. Django includes middleware for security, sessions,
authentication, messages and CSRF protection.

``` python
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Request received")
        response = self.get_response(request)
        print("Response sent")
        return response
```

Register custom middleware in `MIDDLEWARE` in `settings.py`. Middleware
is useful for cross-cutting concerns such as request logging or shared
processing. Keep business rules in views or dedicated service functions
when possible.

## 17. Messages framework

The messages framework displays one-time notifications after an
operation.

``` python
from django.contrib import messages

messages.success(request, 'Student registered successfully!')
messages.error(request, 'The operation could not be completed.')
messages.warning(request, 'Please review the information.')
messages.info(request, 'Your report is being prepared.')
```

In a template:

``` html
{% if messages %}
  {% for message in messages %}
    <p>{{ message }}</p>
  {% endfor %}
{% endif %}
```

The default project template includes message middleware and context
processor. Keep the relevant generated settings enabled.

## 18. Static files and uploaded media

### Static files

``` html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}" alt="School logo">
```

A typical static directory contains `css/`, `js/` and `images/`. In
production, collect static files using `collectstatic` and serve them
through a suitable web server or static-file storage.

### Media uploads

``` python
# models.py
photo = models.ImageField(upload_to='student_photos/')

# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

``` html
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
```

In the view:

``` python
form = StudentForm(request.POST, request.FILES)
```

`ImageField` requires the Pillow package. For uploads, validate file
size and type, control who can access files, and use appropriate storage
and backup policies. In development, media can be served with Django URL
helpers; production should use a proper web server or object storage.

## 19. Sessions

Sessions let Django associate data with a user's browser across
requests. Django's session framework commonly uses a cookie containing a
session identifier while session data is stored server-side.

``` python
request.session['school_name'] = 'ABC School'

school = request.session.get('school_name')

del request.session['school_name']
```

Sessions are useful for temporary workflows, shopping carts and
user-specific state. Do not store passwords or sensitive secrets in
session values.

## 20. Signals

Signals allow code to respond to events such as a model being saved or
deleted. For example, a `post_save` receiver can react when a user
account is created.

``` python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    if created:
        print('New user registered!')
```

This is an illustration, not a complete profile-creation implementation.
Register signal handlers reliably, commonly from the app configuration's
`ready()` method. Avoid hiding complex business workflows in signals;
explicit service functions are often easier to understand and test.

## 21. Function-Based Views and Class-Based Views

Function-Based Views (FBVs) are Python functions that receive a request
and return a response. They are often easiest for beginners to
understand.

``` python
def student_list(request):
    students = Student.objects.all()
    return render(
        request,
        'students/list.html',
        {'students': students}
    )
```

Class-Based Views (CBVs) use classes and can reuse common behavior.
Django provides generic views for common patterns.

``` python
from django.views.generic import ListView
from .models import Student

class StudentListView(ListView):
    model = Student
    template_name = 'students/list.html'
    context_object_name = 'students'
```

URL configuration:

``` python
path('students/', StudentListView.as_view(), name='student_list')
```

  Generic view     Purpose
  ---------------- --------------------------------------
  `ListView`       Displays a collection of records.
  `DetailView`     Displays one record.
  `CreateView`     Creates a record.
  `UpdateView`     Updates a record.
  `DeleteView`     Deletes a record after confirmation.
  `TemplateView`   Renders a template.
  `RedirectView`   Redirects to another URL.

Learn FBVs first to understand request handling. Then learn CBVs to
reduce repetitive code. Both approaches are valid.

## 22. Django REST Framework (DRF)

Django REST Framework is a separate package for building REST APIs. APIs
allow a Django backend to exchange data with mobile apps, JavaScript
frontends and other systems. A common response format is JSON.

Example response:

``` json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Peter",
  "student_id": "STU002"
}
```

Simplified API view:

``` python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student

@api_view(['GET'])
def student_api(request):
    students = Student.objects.all()

    data = [
        {
            'id': student.id,
            'name': student.first_name,
            'student_id': student.student_id
        }
        for student in students
    ]

    return Response(data)
```

This simplified example manually builds response data. In real projects,
use serializers to validate input and convert model instances to and
from API representations. Add authentication, permissions, pagination,
filtering and versioning where appropriate.

## 23. Testing with `tests.py`

Automated tests verify that your code behaves as expected and help
prevent regressions when features change.

``` python
from django.test import TestCase
from .models import Student

class StudentTest(TestCase):
    def test_student_creation(self):
        student = Student.objects.create(
            first_name='Alex',
            last_name='Peter',
            student_id='STU003',
            age=20,
            gender='Male'
        )

        self.assertEqual(student.first_name, 'Alex')
```

Run tests:

``` bash
python manage.py test
```

Test models, forms, views, permissions, URLs and important business
rules. Tests should use test data and should not depend on production
records.

## 24. Other useful Django concepts

  -----------------------------------------------------------------------
  Concept                             Meaning and practical use
  ----------------------------------- -----------------------------------
  Validators                          Reusable checks for field values,
                                      such as a minimum age or valid
                                      input range.

  Custom managers                     Reusable model query methods, such
                                      as querying active students.

  Database constraints                Enforce rules at database level,
                                      such as unique combinations.

  Transactions                        Make multiple database changes
                                      succeed or fail as one unit; useful
                                      for payments.

  Pagination                          Split long result lists into pages.

  Caching                             Reuse frequently requested data to
                                      reduce processing.

  Management commands                 Create custom commands for imports,
                                      maintenance and scheduled jobs.

  Celery/background tasks             Run slow tasks outside the web
                                      request, such as sending bulk
                                      email.

  Logging                             Record application events and
                                      errors for diagnosis.
  -----------------------------------------------------------------------

## 25. Real project architecture

A school management system can be divided into applications according to
business responsibilities. Each app owns a coherent part of the system.

``` text
school_system/
    manage.py
    school_system/
        settings.py
        urls.py
        asgi.py
        wsgi.py
    students/
        migrations/
        templates/students/
        models.py
        views.py
        forms.py
        urls.py
        admin.py
        tests.py
    teachers/
    examinations/
    attendance/
    fees/
    templates/
        base.html
        login.html
        dashboard.html
    static/
        css/
        js/
        images/
    media/
    requirements.txt
```

This is an illustrative structure. Each application can have its own
models, views, forms, URLs, tests and templates. Keep shared templates
and shared utilities at project level where appropriate.

## 26. How all the elements work together

  -----------------------------------------------------------------------
  Step                    Element                 What happens
  ----------------------- ----------------------- -----------------------
  1                       Browser and URL         The browser requests a
                                                  page; Django matches a
                                                  URL pattern.

  2                       View                    The view receives the
                                                  request and runs
                                                  application logic.

  3                       Form                    If the user submitted
                                                  data, the form
                                                  validates it.

  4                       Model and ORM           The model describes the
                                                  data; ORM creates or
                                                  retrieves records.

  5                       Database                The database stores or
                                                  returns the
                                                  information.

  6                       View                    The view prepares
                                                  context or a redirect.

  7                       Template                The template renders
                                                  the page for the user.
  -----------------------------------------------------------------------

For a student registration request: the user opens the add-student URL,
the URL routes to the create view, the view displays a ModelForm, the
user submits it, the form validates the data, the model saves it through
the ORM, and the user is redirected to the student list.

## 27. Security essentials for real projects

  -----------------------------------------------------------------------
  Security measure                    Why it matters
  ----------------------------------- -----------------------------------
  CSRF protection                     Helps prevent forged form
                                      submissions from another site.

  Authentication                      Verifies the user's identity.

  Authorization                       Controls which actions and records
                                      a user may access.

  Password hashing                    Django stores password hashes
                                      rather than plain-text passwords.

  HTTPS                               Encrypts traffic between browser
                                      and server.

  SQL injection protection            Use Django ORM or safely
                                      parameterized SQL; do not
                                      concatenate untrusted SQL.

  XSS protection                      Keep template autoescaping enabled
                                      and handle untrusted HTML
                                      carefully.

  `DEBUG=False`                       Avoid exposing detailed debug pages
                                      in production.

  Environment variables               Keep secret keys and credentials
                                      out of source control.

  Backups and logging                 Support recovery, monitoring and
                                      incident investigation.
  -----------------------------------------------------------------------

Security is not a single setting. Apply least privilege, validate input,
check permissions on the server, update dependencies, protect uploaded
files and test access boundaries.

## 28. Deploying Django

A common VPS deployment uses Ubuntu, Django, Gunicorn, Nginx and
PostgreSQL.

  -----------------------------------------------------------------------
  Component                           Responsibility
  ----------------------------------- -----------------------------------
  Ubuntu Linux                        Server operating system.

  Python and Django                   Application runtime and framework.

  Gunicorn                            WSGI application server.

  Nginx                               Web server and reverse proxy; can
                                      serve static files.

  PostgreSQL                          Production relational database.

  Domain name                         Human-readable website address.

  SSL/TLS certificate                 Enables HTTPS.

  Static and media storage            Stores CSS, JavaScript, images and
                                      user uploads.
  -----------------------------------------------------------------------

Deployment checklist:

-   Use Git and GitHub for source control and deployment history.
-   Configure production settings and environment variables.
-   Run database migrations as part of a controlled deployment.
-   Collect and serve static files correctly.
-   Configure media storage and backups.
-   Set up logging, monitoring, firewall rules and regular updates.

## 29. Recommended learning roadmap

  -----------------------------------------------------------------------
  Phase                   Topics to learn         Practical outcome
  ----------------------- ----------------------- -----------------------
  1\. Fundamentals        Projects, apps,         A working student CRUD
                          settings, models,       application.
                          migrations, URLs,       
                          views, templates and    
                          forms.                  

  2\. Real applications   ORM, authentication,    A multi-user inventory
                          permissions, search,    or school application.
                          pagination, uploads and 
                          admin customization.    

  3\. Advanced Django     CBVs, signals,          A tested application
                          middleware, testing,    with an API.
                          query optimization and  
                          DRF.                    

  4\. Professional        PostgreSQL, Git, Linux, A production-ready
  development             Gunicorn, Nginx,        deployed application.
                          deployment, security    
                          and backups.            
  -----------------------------------------------------------------------

## 30. Five practical projects

  ------------------------------------------------------------------------
  Project                 Skills practiced        Suggested level
  ----------------------- ----------------------- ------------------------
  1\. Student             Models, forms, views,   Beginner
  Registration System     URLs, templates and     
                          CRUD.                   

  2\. Inventory           Relationships, search,  Beginner--Intermediate
  Management System       filtering, stock        
                          calculations and        
                          authentication.         

  3\. School Academic     Multiple apps,          Intermediate
  Records System          relationships,          
                          permissions and         
                          reports.                

  4\. Apartment           Users, tenants,         Intermediate
  Management System       properties, payments    
                          and database design.    

  5\. Django REST API     Serializers, API views, Advanced
                          authentication and      
                          mobile integration.     
  ------------------------------------------------------------------------

## 31. Official online learning resources

1.  **Django documentation:**
    <https://docs.djangoproject.com/en/stable/> --- authoritative
    reference and tutorials.
2.  **Django Girls tutorial:** <https://tutorial.djangogirls.org/> ---
    beginner-friendly guided project.
3.  **MDN Django guide:**
    <https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django>
    --- server-side web development concepts and Django introduction.

## 32. Final advice: learn by building

Do not try to memorize every Django feature at once. First understand
how models, views, URLs, forms, templates and the ORM cooperate.
Practise writing each file yourself and explain what each line does.

**Suggested first exercise:** Start with an empty project and build a
complete Student CRUD system. Add one feature at a time: list students,
register a student, edit a student, delete a student, add search, then
add login and permissions.

When you can build that application without copying a finished solution,
you will have a strong foundation for larger systems such as school
academic records platforms, inventory systems and apartment management
applications.

------------------------------------------------------------------------

*End of guide. Use the official Django documentation alongside practical
coding exercises.*
