Django Rest Framework CRUD API

1. Django Installation

```python
pip install Django==3.2.7
```

2. Django Rest Framework Installation

```python
pip install djangorestframework
```

3. Start Django Project

```python
django-admin startproject CRUDAPI
```

```python
cd CRUDAPI
```

```python
python manage.py startapp todoList
```

4. Registet TodoList app

```python
INSTALLED_APPS = [
    'todoList.apps.TodolistConfig',
]
```

5. Register Django Rest Framework

```python
INSTALLED_APPS = [
    'rest_framework',
]
```

6. Models

```python
python manage.py migrate
```

7. Start out application

```python
python manage.py runserver
```

8. Create superuser

```python
python manage.py createsuperuser
```

9. Run application again

```python
python manage.py runserver
```

10. Include URL for our app

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("todoList.urls"))
]
```

11. Update the url file

```python
from django.urls import path
from .views import index

urlpatterns = [
    path("", index, name = "index")
]
```

12. User registration Serializer

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
```

in views.py add the following

```python
from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
```

13. Simple JWT login

```python
pip install djangorestframework-simplejwt
```

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

```python
INSTALLED_APPS = [
    'rest_framework_simplejwt',
]
```

```python

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
```

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES' : ('rest_framework.permissions.IsAuthenticated',)
    ,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

```

14. Model Creation

```python
class Todo(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=400, null=False)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.utcnow)

    def __str__(self) -> str:
        return self.name
```


15. Model Serialization

```python
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"
```

16. Final ``url.py`` file from CRUDAPI app

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("todoList.urls")),
    path('admin/', admin.site.urls),
    path('api-auth/', include("rest_framework.urls")),
]
```

17. Final ``url.py`` from todoList app

```python
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserCreate, TodosListCreateView, TodosRetrieveUpdateDestroyAPIView


urlpatterns = [
    path("registration/", UserCreate.as_view()),
    path('', TodosListCreateView.as_view()),
    path('todos/<int:pk>/', TodosRetrieveUpdateDestroyAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

18. Final file from ``views.py`` from todoList

```python
from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Todo
from .serializers import TodoSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class TodosListCreateView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class TodosRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
```