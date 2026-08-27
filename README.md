# SpendWise Live - Django REST API

SpendWise Live is a full-stack expense tracking project built with Django and Django REST Framework. The backend replaces the earlier in-memory expense manager with a persistent database-backed API that supports authentication, per-user expenses, filtering, search, ordering, and pagination.

The SpendWise front end connects to this API using JavaScript `fetch()` requests.

## Project Features

- Django REST Framework API
- Persistent expense storage using SQLite
- Token authentication
- Session authentication for the browsable API
- Per-user expense isolation
- Create, read, update, and delete expenses
- Automatic expense ownership
- Category filtering
- Description search
- Expense ordering
- Pagination
- CORS support for front-end access
- Django administration interface
- Authentication failure handling

## Technology Used

- Python
- Django
- Django REST Framework
- django-filter
- django-cors-headers
- SQLite
- HTML
- CSS
- JavaScript
- Fetch API

## Project Structure

```text
SpendWise-Live-Django-REST-API/
│
├── expenses/
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
│
├── spendwise/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── __init__.py
│
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Expense Model

The application uses an `Expense` model containing the following fields:

```text
owner
amount
description
category
created_at
```

The model uses Django's built-in user system.

Each expense belongs to one authenticated user through a foreign key:

```python
owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='expenses'
)
```

The amount is stored using a decimal field so money values can be represented accurately.

The creation date is automatically recorded when an expense is saved.

## Expense Serializer

The `ExpenseSerializer` converts Expense model records to and from JSON.

The API exposes:

```text
id
amount
description
category
created_at
owner
```

The owner field is read-only:

```python
owner = serializers.ReadOnlyField(source='owner.username')
```

This prevents a client from choosing another user as the owner of an expense.

## Per-User Expense Security

Every expense request is scoped to the currently authenticated user.

The viewset uses:

```python
def get_queryset(self):
    return self.request.user.expenses.all()
```

This means:

```text
User A can only see User A's expenses.
User B can only see User B's expenses.
```

Expense ownership is also assigned on the server:

```python
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
```

The client never submits the owner ID.

This prevents users from creating expenses under another person's account.

## Authentication

SpendWise uses Django REST Framework token authentication.

The login endpoint is:

```text
POST /api/login/
```

A login request contains:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

A successful request returns a token.

Authenticated API requests send the token using the Authorization header:

```text
Authorization: Token YOUR_TOKEN
```

Every expense endpoint requires authentication.

A request without authentication was tested and returned:

```text
HTTP/1.1 401 Unauthorized
```

with:

```json
{
    "detail": "Authentication credentials were not provided."
}
```

An invalid token was also tested and returned:

```text
HTTP/1.1 401 Unauthorized
```

with:

```json
{
    "detail": "Invalid token."
}
```

The `/api/login/` endpoint was tested successfully and returned a valid authentication token.

## API Endpoints

### Login

```text
POST /api/login/
```

### List Expenses

```text
GET /api/expenses/
```

### Create Expense

```text
POST /api/expenses/
```

### Retrieve One Expense

```text
GET /api/expenses/<id>/
```

### Update Expense

```text
PUT /api/expenses/<id>/
```

or:

```text
PATCH /api/expenses/<id>/
```

### Delete Expense

```text
DELETE /api/expenses/<id>/
```

## Example Expense

A typical API response looks like:

```json
{
    "id": 1,
    "amount": "150.00",
    "description": "Weekly groceries",
    "category": "food",
    "created_at": "2026-08-27T04:45:58.751580Z",
    "owner": "robin"
}
```

The amount is returned as a string so decimal precision is preserved.

## Filtering

Expenses can be filtered by category using the `category` query parameter.

Example:

```text
/api/expenses/?category=food
```

Testing returned only expenses with:

```text
category = food
```

The tested food records included:

```text
Weekly groceries
Coffee before work
Lunch at work
Coffee beans
Snacks
```

The filter returned:

```text
count: 5
```

## Search

Expense descriptions can be searched using:

```text
/api/expenses/?search=coffee
```

Testing returned:

```text
Coffee beans
Coffee before work
```

The response contained:

```text
count: 2
```

Search is performed against the `description` field.

## Ordering

Expenses can be ordered using the `ordering` query parameter.

Highest amount first:

```text
/api/expenses/?ordering=-amount
```

The test returned amounts in descending order:

```text
200.00
150.00
120.00
70.00
60.00
45.00
35.00
25.00
22.00
15.00
```

Smallest amount first:

```text
/api/expenses/?ordering=amount
```

Expenses can also be ordered by creation date:

```text
/api/expenses/?ordering=created_at
```

or newest first:

```text
/api/expenses/?ordering=-created_at
```

Category ordering is also supported:

```text
/api/expenses/?ordering=category
```

The viewset supports:

```python
ordering_fields = ['amount', 'created_at', 'category']
```

## Pagination

The API uses page-number pagination with:

```text
PAGE_SIZE = 10
```

When more than ten expenses exist, list responses contain:

```json
{
    "count": 12,
    "next": "http://127.0.0.1:8000/api/expenses/?page=2",
    "previous": null,
    "results": []
}
```

The second page was successfully tested using:

```text
/api/expenses/?page=2
```

The test returned:

```text
count: 12
next: null
previous: http://127.0.0.1:8000/api/expenses/
```

The remaining two expenses appeared inside `results`.

Because pagination wraps the records inside the response object, the front end must read:

```javascript
data.results
```

instead of reading `data` directly.

## Two-User Privacy Test

Two separate user accounts were created to test per-user isolation.

The first user had an expense:

```text
Weekly groceries
Amount: 150.00
Category: food
```

The API showed:

```text
owner: robin
```

A second account named:

```text
testuser2
```

was created.

When logged in as `testuser2`, the first user's expense was not visible.

An expense belonging to `testuser2` was also created:

```text
Bus fare
Amount: 25.00
Category: transport
```

After switching back to the first user, the `Bus fare` expense was not visible.

This demonstrates that the API successfully isolates expense data by authenticated user.

## Django REST Framework Configuration

The project uses token and session authentication:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

## CORS Configuration

The project uses `django-cors-headers` so the SpendWise front end can communicate with the Django API.

CORS middleware is enabled in Django settings.

For local development:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

This is suitable for the local project environment.

In a production environment, access should normally be limited to specific trusted front-end origins.

## Front-End Integration

The SpendWise dashboard communicates with the backend using JavaScript `fetch()`.

### Login

The dashboard sends the username and password to:

```text
http://127.0.0.1:8000/api/login/
```

The returned token is stored and used for future API requests.

Example:

```javascript
async function login(username, password) {
    const response = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    const data = await response.json();
    localStorage.setItem("token", data.token);
}
```

### Load Expenses

```javascript
async function loadExpenses() {
    const token = localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:8000/api/expenses/",
        {
            headers: {
                "Authorization": "Token " + token
            }
        }
    );

    const data = await response.json();

    return data.results;
}
```

### Add Expense

```javascript
async function addExpense(amount, description, category) {
    const token = localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:8000/api/expenses/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Token " + token
            },
            body: JSON.stringify({
                amount: amount,
                description: description,
                category: category
            })
        }
    );

    return await response.json();
}
```

## Installation

Clone the repository:

```text
git clone <repository-url>
```

Enter the project folder:

```text
cd SpendWise-Live-Django-REST-API
```

Create a virtual environment:

```text
py -m venv venv
```

Activate the virtual environment on Windows PowerShell:

```text
.\venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, the execution policy can be changed temporarily for the current terminal:

```text
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

Install the required packages:

```text
pip install -r requirements.txt
```

Apply database migrations:

```text
python manage.py migrate
```

Create a Django administrator:

```text
python manage.py createsuperuser
```

Start the development server:

```text
python manage.py runserver
```

The server will run at:

```text
http://127.0.0.1:8000/
```

## Useful Development URLs

Django admin:

```text
http://127.0.0.1:8000/admin/
```

API root:

```text
http://127.0.0.1:8000/api/
```

Expense API:

```text
http://127.0.0.1:8000/api/expenses/
```

Token login:

```text
http://127.0.0.1:8000/api/login/
```

## Testing Completed

The following requirements were tested successfully:

- Django project configuration
- Expense database migrations
- Token authentication
- Successful `/api/login/`
- Missing authentication returns `401 Unauthorized`
- Invalid token returns `401 Unauthorized`
- Expense creation
- Per-user ownership
- Two-user expense isolation
- Category filtering
- Description search
- Amount ordering
- Creation-date ordering support
- Category ordering support
- Pagination
- Paginated `count`
- Paginated `next`
- Paginated `previous`
- Paginated `results`

## Requirements

The project dependencies are stored in:

```text
requirements.txt
```

The project uses:

```text
Django
djangorestframework
django-filter
django-cors-headers
```

## Security Notes

The API does not trust the client to specify expense ownership.

Ownership is determined from the authenticated request:

```python
serializer.save(owner=self.request.user)
```

The queryset is also restricted on the server:

```python
return self.request.user.expenses.all()
```

This means front-end manipulation cannot be used to request another user's expense list through the normal API endpoints.

Authentication is enforced globally through Django REST Framework.

## Final Project Requirements

This backend satisfies the SpendWise Live project requirements for:

- Expense model
- Expense serializer
- ModelViewSet
- DefaultRouter
- `/api/expenses/`
- `/api/login/`
- Token authentication
- Per-user querysets
- Automatic expense ownership
- Category filtering
- Search
- Ordering
- Pagination
- CORS configuration
- Front-end API integration support
- Two-user privacy testing
- Authentication error testing

## Conclusion

SpendWise Live converts the previous console-based expense manager into a persistent authenticated web API.

Django manages the database and user accounts, while Django REST Framework provides the JSON API, authentication, filtering, searching, ordering, and pagination.

Most importantly, expense ownership is enforced by the backend so each authenticated user only receives their own financial records.

The API is ready to be connected to the SpendWise front-end dashboard using JavaScript `fetch()` requests.