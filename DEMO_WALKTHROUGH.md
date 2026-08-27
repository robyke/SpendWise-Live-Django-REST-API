# SpendWise Live - Demo Walkthrough

This walkthrough demonstrates the main Week 8 SpendWise Live requirements using the completed frontend and Django REST API.

## Project Links

### Backend Repository

https://github.com/robyke/SpendWise-Live-Django-REST-API

### Frontend Repository

https://github.com/robyke/spendwise-dashboard

---

## 1. Start the Django Backend

From the backend project folder:

```powershell
cd C:\Users\ROBIN\Downloads\SpendWise-Live-Django-REST-API
.\venv\Scripts\python.exe manage.py runserver
```

Expected local backend address:

```text
http://127.0.0.1:8000/
```

Expense API:

```text
http://127.0.0.1:8000/api/expenses/
```

Login endpoint:

```text
http://127.0.0.1:8000/api/login/
```

---

## 2. Start the Frontend

From the frontend project folder:

```powershell
cd C:\Users\ROBIN\Downloads\spendwise-dashboard
python -m http.server 5500
```

Open the dashboard in a browser:

```text
http://127.0.0.1:5500
```

The Django server must also remain running on port 8000.

---

## 3. Login Demonstration

SpendWise opens on a login screen.

Login with the first Django test account:

```text
Username: robin
Password: [private]
```

The frontend sends the credentials to:

```text
POST /api/login/
```

A successful login returns an authentication token.

Future requests include:

```text
Authorization: Token <token>
```

The password is not stored by the frontend.

### Test Result

The `/api/login/` endpoint was tested successfully and returned an authentication token.

### Screenshot Evidence

Add a screenshot here showing the login page.

```text
Screenshot 1 - SpendWise login page
```

Do not show the password or authentication token.

---

## 4. Load the Logged-In User's Expenses

After login, the frontend requests:

```text
GET /api/expenses/
```

The Django backend limits the queryset to the authenticated user:

```python
def get_queryset(self):
    return self.request.user.expenses.all()
```

This means the dashboard displays real expense data belonging only to the logged-in user.

Example expenses used during testing included:

```text
Weekly groceries - 150.00 - food
Coffee before work - 8.50 - food
Bus pass - 25.00 - transport
Internet bill - 60.00 - utilities
Lunch at work - 35.00 - food
Electricity - 120.00 - utilities
Parking - 15.00 - transport
Fuel - 45.00 - transport
Coffee beans - 22.00 - food
Pharmacy - 70.00 - health
Rent - 200.00 - housing
Snacks - 12.00 - food
```

### Screenshot Evidence

```text
Screenshot 2 - Robin dashboard showing live expenses
```

---

## 5. Add an Expense Without Reloading

Use the Add Expense form.

Example:

```text
Amount: 18.75
Description: Dashboard test expense
Category: Food
```

Click:

```text
Add Expense
```

The frontend sends:

```text
POST /api/expenses/
```

The client sends:

```json
{
  "amount": "18.75",
  "description": "Dashboard test expense",
  "category": "food"
}
```

The client does not choose an owner.

Django automatically assigns the logged-in user:

```python
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
```

The expense appears in the dashboard without manually refreshing the browser.

### Screenshot Evidence

```text
Screenshot 3 - Dashboard test expense visible immediately after creation
```

---

## 6. Category Filtering

Choose:

```text
Food
```

from the category filter.

The frontend sends:

```text
/api/expenses/?category=food
```

Backend testing confirmed that the result contained only food expenses.

The test returned:

```text
count: 5
```

Food expenses included:

```text
Weekly groceries
Coffee before work
Lunch at work
Coffee beans
Snacks
```

### Screenshot Evidence

```text
Screenshot 4 - Food category filter
```

---

## 7. Description Search

Enter:

```text
coffee
```

into the Search Description field.

The frontend sends:

```text
/api/expenses/?search=coffee
```

The backend test returned:

```text
Coffee beans
Coffee before work
```

Tested result:

```text
count: 2
```

### Screenshot Evidence

```text
Screenshot 5 - Coffee search results
```

---

## 8. Expense Ordering

Select:

```text
Highest amount
```

The frontend sends:

```text
/api/expenses/?ordering=-amount
```

Backend testing returned expenses in descending amount order.

Example result:

```text
200.00 - Rent
150.00 - Weekly groceries
120.00 - Electricity
70.00 - Pharmacy
60.00 - Internet bill
45.00 - Fuel
35.00 - Lunch at work
25.00 - Bus pass
22.00 - Coffee beans
15.00 - Parking
```

Other supported ordering options include:

```text
/api/expenses/?ordering=amount
/api/expenses/?ordering=-created_at
/api/expenses/?ordering=created_at
/api/expenses/?ordering=category
```

### Screenshot Evidence

```text
Screenshot 6 - Expenses ordered by highest amount
```

---

## 9. Per-User Data Isolation

Log out of Robin's account.

Then log in using the second test account:

```text
Username: testuser2
Password: [private]
```

A separate expense was created for this account:

```text
Bus fare
Amount: 25.00
Category: transport
```

When `testuser2` is logged in, Robin's expenses are not displayed.

When Robin is logged back in, the `Bus fare` expense belonging to `testuser2` is not displayed.

This demonstrates per-user data isolation.

The protection is enforced by the Django backend:

```python
def get_queryset(self):
    return self.request.user.expenses.all()
```

### Screenshot Evidence

```text
Screenshot 7 - testuser2 showing a different expense list
```

---

## 10. Missing Authentication Test

The API was tested without an authentication token.

Command:

```powershell
curl.exe -i http://127.0.0.1:8000/api/expenses/
```

Result:

```text
HTTP/1.1 401 Unauthorized
```

Response:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

This confirms that unauthenticated users cannot access the expense API.

---

## 11. Invalid Token Test

The API was also tested using an invalid token.

Command:

```powershell
curl.exe -i -H "Authorization: Token definitely-invalid-token" http://127.0.0.1:8000/api/expenses/
```

Result:

```text
HTTP/1.1 401 Unauthorized
```

Response:

```json
{
  "detail": "Invalid token."
}
```

This confirms that an invalid token cannot be used to access expense data.

### Screenshot Evidence

```text
Screenshot 8 - 401 Unauthorized terminal evidence
```

Do not expose a real authentication token in the screenshot.

---

## 12. Pagination Test

The API uses page-number pagination.

Configured page size:

```text
10
```

The following endpoint was tested:

```text
/api/expenses/?page=2
```

The response included:

```json
{
  "count": 12,
  "next": null,
  "previous": "http://127.0.0.1:8000/api/expenses/",
  "results": [
    {
      "amount": "8.50",
      "description": "Coffee before work",
      "category": "food",
      "owner": "robin"
    },
    {
      "amount": "150.00",
      "description": "Weekly groceries",
      "category": "food",
      "owner": "robin"
    }
  ]
}
```

This confirms that pagination provides:

```text
count
next
previous
results
```

The frontend reads records from:

```javascript
data.results
```

and follows additional pages when necessary.

### Screenshot Evidence

```text
Screenshot 9 - Pagination response
```

---

## 13. Expense Model

The Django Expense model contains the required fields:

```text
owner
amount
description
category
created_at
```

The owner is connected to Django's built-in User model.

Example:

```python
owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='expenses'
)
```

The amount uses a decimal field:

```python
amount = models.DecimalField(
    max_digits=10,
    decimal_places=2
)
```

The creation date is automatically stored:

```python
created_at = models.DateTimeField(
    auto_now_add=True
)
```

---

## 14. Expense Serializer

The serializer exposes:

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
owner = serializers.ReadOnlyField(
    source='owner.username'
)
```

This prevents the frontend from submitting another user's username as the expense owner.

---

## 15. ViewSet and Router

The API uses a Django REST Framework `ModelViewSet`.

The viewset supports:

```text
GET
POST
PUT
PATCH
DELETE
```

The router exposes expenses under:

```text
/api/expenses/
```

Individual expense records are available at:

```text
/api/expenses/<id>/
```

---

## 16. Filtering, Search, and Ordering Configuration

The backend viewset includes:

```python
filterset_fields = ['category']
search_fields = ['description']
ordering_fields = ['amount', 'created_at', 'category']
ordering = ['-created_at']
```

This provides server-side filtering, search, and ordering rather than performing those operations only in the browser.

---

## 17. Authentication Configuration

Django REST Framework is configured to require authentication.

The project includes:

```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
]
```

and:

```python
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
]
```

This protects the expense endpoints.

---

## 18. CORS Configuration

The project uses:

```text
django-cors-headers
```

CORS middleware allows the frontend running on port 5500 to communicate with Django running on port 8000.

For the local development project:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

For a production application, trusted origins should normally be restricted.

---

## 19. Django System Check

The backend was verified using:

```powershell
python manage.py check
```

Result:

```text
System check identified no issues (0 silenced).
```

### Screenshot Evidence

```text
Screenshot 10 - Django system check success
```

---

## 20. Required Backend Files

The backend repository contains:

```text
manage.py
requirements.txt
README.md
expenses/models.py
expenses/serializers.py
expenses/views.py
expenses/urls.py
expenses/migrations/0001_initial.py
spendwise/settings.py
spendwise/urls.py
```

---

## 21. Python Requirements

The backend requirements include:

```text
asgiref==3.12.1
Django==6.1
django-cors-headers==4.9.0
django-filter==26.1
djangorestframework==3.18.0
sqlparse==0.6.0
tzdata==2026.3
```

---

## 22. Requirements Demonstrated

SpendWise Live demonstrates:

- Django Expense model
- Expense serializer
- ModelViewSet
- DefaultRouter
- `/api/expenses/`
- `/api/login/`
- Token authentication
- Protected API endpoints
- Per-user expense ownership
- Server-side owner assignment
- User data isolation
- Category filtering
- Description search
- Expense ordering
- Pagination
- CORS
- JavaScript `fetch()`
- Live database data
- Adding expenses without page reload
- Deleting expenses
- Login and logout
- Two-user testing
- Missing-token `401 Unauthorized`
- Invalid-token `401 Unauthorized`

---

# Suggested Non-Video Demo Screenshot Order

For a complete written walkthrough, capture screenshots in this order:

1. SpendWise login screen
2. Robin dashboard showing live expenses
3. New expense added without refreshing
4. Food filter results
5. Coffee search results
6. Highest-amount ordering
7. testuser2 showing separate data
8. Terminal showing `401 Unauthorized`
9. Pagination response
10. `python manage.py check` showing no issues

Do not include passwords or real authentication tokens in screenshots.

---

# Submission Links

## Backend

```text
https://github.com/robyke/SpendWise-Live-Django-REST-API
```

## Frontend

```text
https://github.com/robyke/spendwise-dashboard
```

---

# Conclusion

SpendWise Live connects a responsive JavaScript dashboard to a Django REST API.

Users authenticate using token authentication and can create, view, filter, search, order, and delete their own expenses.

The backend enforces ownership so users cannot access another user's expense records.

The project also demonstrates pagination, authentication protection, CORS configuration, database persistence, and live frontend-to-backend communication.