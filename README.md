<div align="center">
<h1>Django Deployment Guide</h1>
</div>

# Context

- [Context](#context)
  - [Preparation](#preparation)
  - [Deployment](#deployment)
    - [Cpanel Deployment](#cpanel-deployment)
    - [Render Deployment](#render-deployment)
    - [Host locally view globally](#host-locally-view-globally)
  - [Extra](#extra)
    - [Django uploaded content (File/Image) Deletion](#django-uploaded-content-fileimage-deletion)
    - [Django uploaded content (File/Image) Rename](#django-uploaded-content-fileimage-rename)
    - [Sign-in/Sign-up Access Control using Custom Decorator](#sign-insign-up-access-control-using-custom-decorator)

## Preparation

- Add those in `requirements.txt`

  ```txt
  Django==6.0.5
  gunicorn==26.0.0
  pillow==12.2.0
  whitenoise==6.12.0
  django-cleanup==9.0.0
  crispy-bootstrap5==2026.3
  ```

- In `settings.py` file modify as below

  ```py
  DEBUG = False
  ALLOWED_HOSTS = ["*"] # change this to domain website
  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'whitenoise.runserver_nostatic', # This must be added before 'django.contrib.staticfiles'
      'django.contrib.staticfiles',

      # for cleanup deleted files
      'django_cleanup.apps.CleanupConfig',

      # bootstrap5
      "crispy_forms",
      "crispy_bootstrap5",

      # my apps
      'imageApp',
    ]

  MIDDLEWARE = [
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'whitenoise.middleware.WhiteNoiseMiddleware', # This must be added here after SecurityMiddleware & SessionMiddleware
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',
  ]
  # Add those at the end
  # static
  STATIC_URL = 'static/'
  STATIC_ROOT = BASE_DIR / 'staticfiles/'

  STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

  # media
  MEDIA_URL = '/media/'
  MEDIA_ROOT = BASE_DIR / 'media/'

  # auth model
  AUTH_USER_MODEL='imageApp.CustomUserModel'

  # login redirect
  LOGIN_URL='signin'

  # bootstrap5
  CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
  CRISPY_TEMPLATE_PACK = "bootstrap5"
  ```

  - Here we set the URL of the media so when we make a `ImageField` in model we will set the `upload_to` --> `upload_to='profile_image'` or any other preferred path name
  - To show the image we will use `{{i.profile_image.url}}`
- Now in modify `urls.py` file in project directory

  ```py
  from django.contrib import admin
  from django.conf import settings
  from django.conf.urls.static import static
  from django.views.static import serve
  from django.urls import path, include, re_path

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('',include('imageApp.urls'))
  ]
  if settings.DEBUG:
      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
      urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  ```

- Now use this command to collect all the static content
  - `python manage.py collectstatic`

---
[⬆️ Go to Context](#context)

## Deployment

### Cpanel Deployment

- In `Cpanel` create a python application
- Select python version >= 3.10 (for django version 5)
- Add `Application root`
- Select domain in `Application URL` and set the url
- Now click on `Create`
- Go to the `Application root` path
  - Edit `passenger_wsgi.py` add the below line and save it
    - `from imageProject.wsgi import application` # here imageProject is the project name
  - Upload project with `requirements.txt`
- Now again go to the python application and add `requirements.txt` in `Configuration files` (Save and run pip install)
- Now in `Execute python script` run this: `manage.py collectstatic`

---
[⬆️ Go to Context](#context)

### Render Deployment

- Go to [render](https://render.com/) and select web service from New tab
- Select GitHub repo of the project
- Now in project setting page write Project Name (unique)
- Select Region, Branch
- Set Build command `pip install -r requirements.txt`
- Set start command `gunicorn imageProject.wsgi:application`
  > here `jobProject` is the project name
- Choose Instance Type `Free` and start deploy.

---
[⬆️ Go to Context](#context)

### Host locally view globally

- Using [Serveo](https://serveo.net/)
  - `ssh -R 80:localhost:8000 serveo.net`
  - To use unique subdomain, need to generate a key
    - `ssh-keygen -t ed25519`
    - `ssh -R <unique subdomain>:80:<your local host>:<your local port> serveo.net`
    - Example: `ssh -R youruniquesubdomain:80:localhost:8000 serveo.net`
    - Add that domain in `ALLOWED_HOSTS` and include `CSRF_TRUSTED_ORIGINS = ['https://youruniquesubdomain.serveo.net']` in `settings.py`
  - Now a login prompt to `serveo` will be given; use google/github to login
  - Rerun `ssh -R youruniquesubdomain:80:localhost:8000 serveo.net`, now it will work

---
[⬆️ Go to Context](#context)

## Extra

### Django uploaded content (File/Image) Deletion

- Install `django-cleanup`
  - `pip install django-cleanup`
  - Documentation: [Django Cleanup](https://github.com/un1t/django-cleanup)
- Modify in `settings.py`'s `INSTALLED_APPS`

  ```py
  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'whitenoise.runserver_nostatic', # This must be added before 'django.contrib.staticfiles'
      'django.contrib.staticfiles',
      'imageApp',
      'django_cleanup.apps.CleanupConfig',
  ]
  ```

> Make sure to add it at the bottom

- Now first import the `cleanup` in `models.py`
  - `from django_cleanup import cleanup`
  - Add `@cleanup.select` before class defied

    ```py
    from django.db import models
    from django_cleanup import cleanup

    # Create your models here.
    @cleanup.select
    class UserModel(models.Model):
        name=models.CharField(max_length=100)
        profile_image=models.ImageField(upload_to='profile_image')
        def __str__(self):
            return self.name
    ```

> Note: To ignore a model we can add `@cleanup_ignore`

---
[⬆️ Go to Context](#context)

### Django uploaded content (File/Image) Rename

- Add this function in `models.py`

  ```py
  def user_directory_path(instance, filename):
      # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
      return f"user_{instance.name}_{filename}"
  ```

  - Here file will be saved as `user_{instance.name}_{file_name}`; e.g: `user_tansen_1.jpg`
- Now include this function in `upload_to`

  ```py
  class UserModel(models.Model):
      name=models.CharField(max_length=100)
      profile_image=models.ImageField(upload_to=user_directory_path)
      def __str__(self):
          return self.name
  ```

---
[⬆️ Go to Context](#context)

### Sign-in/Sign-up Access Control using Custom Decorator

- Create a custom function

  ```py
  from django.contrib import messages

  def logout_required(view_func):
      def wrapper(request, *args, **kwargs):
          if request.user.is_authenticated:
              messages.warning(request, "You are already logged in.")
              return redirect('dashboard')
          return view_func(request, *args, **kwargs)
      return wrapper
  ```

  - Here message is added to show the user that he is already logged in
  - Now add this `@logout_required`before `signin` and `singup` function

---
[⬆️ Go to Context](#context)
