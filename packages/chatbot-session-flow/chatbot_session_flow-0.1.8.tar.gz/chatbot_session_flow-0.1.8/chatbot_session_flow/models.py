from django.db import models
from django.utils.timezone import now
import os
from datetime import timedelta
from types import MethodType
import importlib

# Abstract Base Model
class DynamicModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def execute_action(self, *args, **kwargs):
        """Default method - Can be overridden at runtime"""
        return "Default action executed"


# Profile Model
class Profile(models.Model):
    firstName = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=500, blank=True, null=True)
    middleName = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=40, blank=True, null=True)
    lastName = models.CharField(max_length=30, blank=True, null=True)
    phoneNumber = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return "{} {} {} ({}) - {}".format(
            self.firstName or "",
            self.middleName or "",
            self.lastName or "",
            self.username or "No Username",
            self.phoneNumber
        ).strip()


# Session Model
class Session(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile')
    phoneNumber = models.CharField(max_length=15, unique=True)
    last_logged_in = models.DateTimeField(auto_now=True)
    isValidSession = models.BooleanField(default=False)

    def __str__(self):
        return "{} : {}".format(self.phoneNumber or "", self.last_logged_in or "")

    def is_session_expired(self):
        """Checks if session is expired based on MAX_SESSION_TIME from environment"""
        MAX_SESSION_TIME = int(os.environ.get('MAX_SESSION_TIME', 60))  # Default to 60 mins
        return (now() - self.last_logged_in) > timedelta(minutes=MAX_SESSION_TIME) if self.last_logged_in else True


# Page Model
class Page(models.Model):
    PAGE_TYPE_CHOICES = [
        ('collect', 'collect'),
        ('continuation', 'continuation'),
        ('apiCall', 'apiCall'),
        ('computation', 'computation'),
        ('options', 'options'),
        ('text', 'text'),
    ]
    pageType = models.CharField(max_length=20, choices=PAGE_TYPE_CHOICES, default='collect')
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=1000, default="")
    fieldName = models.CharField(max_length=255, default="", blank=True, null=True)
    content = models.TextField()
    task = models.CharField(max_length=255, default="", blank=True, null=True)
    isToPerfomTask = models.BooleanField(default=False)
    prev = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="nextPage", blank=True, null=True)
    next_page = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="prev_page", blank=True, null=True)

    def __str__(self):
        return self.title

    def get_page_sequence(self):
        """Returns a list of page titles in order"""
        sequence, current = [], self
        while current:
            sequence.append(current.title)
            current = current.next_page  # Renamed from `next`
        return sequence

    def override_method(self, method_name, new_function):
        """
        Overrides a method dynamically.
        This does not persist in the database and is only valid in the current execution.
        """
        setattr(self, method_name, MethodType(new_function, self))

    def call_dynamic_method(self, method_name, new_function):
        """
        Overrides a method dynamically.
        This does not persist in the database and is only valid in the current execution.
        """
        views = importlib.import_module(os.environ.get("DYNAMIC_METHOD_VIEWS")) #"chatbot_session_flow.views"
        views.perform_dynamic_action(self.task)


# Page Option Model (Fixed Spelling)
class PageOption(models.Model):
    numberOnScreen = models.IntegerField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="options")
    label = models.CharField(max_length=255)  # Option text (e.g., "Yes", "No", "Maybe")
    next_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="incoming_options")

    def __str__(self):
        return f"{self.page.title} → {self.label} → {self.next_page.title}"


# Stepper Model
class Stepper(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="stepper")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='stepper')
    isCurrent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.page.title} → {self.isCurrent}"


# Collected Data Model
class CollectedData(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="collectedData")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='collectedData')
    key = models.CharField(max_length=255)  # The name of the key being collected
    value = models.CharField(max_length=255)  # The value passed by the user

    def __str__(self):
        return f"{self.page} → {self.key} → {self.value}"