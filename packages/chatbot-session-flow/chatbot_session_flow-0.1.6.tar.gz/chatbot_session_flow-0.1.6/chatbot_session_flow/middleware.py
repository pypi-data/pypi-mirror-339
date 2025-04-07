
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from chatbot_session_flow.models import *
import json
import logging

logger = logging.getLogger(__name__)

class WhatsappSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Handles incoming requests and processes JSON body if applicable."""
        print(f"Request: {request.method} {request.path}")

        # Skip middleware for Django admin URLs
        if request.path.startswith('/admin/'):
            return None  # Allow Django Admin to process normally

        try:
            if request.content_type == "application/json":
                request.json_data = json.loads(request.body)
            else:
                request.json_data = request.POST  # Handle form data
            self.cleanUpData(request)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body.")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error in process_request: {e}", exc_info=True)

        return None  # Continue processing

    def process_response(self, request, response):
        """Logs response status for debugging."""
        print(f"Response: {response.status_code} for {request.path}")
        return response

    def cleanUpData(self, request):
        """Extracts required fields and dynamically dispatches to task handler."""
        try:
            module_path = os.environ.get("DYNAMIC_METHOD_VIEWS")  # e.g., 'chatbot_session_flow.views.dynamic_tasks'
            if not module_path:
                raise ImportError("DYNAMIC_METHOD_VIEWS env variable is not set.")

            views = importlib.import_module(module_path)

            # Try to dynamically call a method based on self.task
            if hasattr(views, "formatRequest"):
                self.run_dynamic_methods("formatRequest")
                data = {
                    "phoneNumber": request.json_data.get("from", ""),
                    "userName": request.json_data.get("name", ""),
                    "message": request.json_data.get("message", ""),
                    "device": request.json_data.get("device", "")
                }
                self.validateSession(request, data)
            else:
                logger.warning(f"No method named formatRequest found in {module_path}. Falling back to default.")

                # Fallback path: extract request data manually
                data = {
                    "phoneNumber": request.json_data.get("from", ""),
                    "userName": request.json_data.get("name", ""),
                    "message": request.json_data.get("message", ""),
                    "device": request.json_data.get("device", "")
                }
                self.validateSession(request, data)

        except Session.DoesNotExist:
            logger.warning("Session not found for phoneNumber.")
        except Exception as e:
            logger.error(f"Error in cleanUpData: {e}", exc_info=True)

    def run_dynamic_methods(self, method_name, *args, **kwargs):
        """
        Dynamically imports a method from the module specified in the
        DYNAMIC_METHOD_VIEWS env variable and executes it with provided arguments.

        :param method_name: Name of the method to call from the dynamic module.
        :param args: Positional arguments to pass to the method.
        :param kwargs: Keyword arguments to pass to the method.
        """
        try:
            module_path = os.environ.get("DYNAMIC_METHOD_VIEWS")  # e.g., 'chatbot_session_flow.views.dynamic_tasks'
            if not module_path:
                raise ImportError("DYNAMIC_METHOD_VIEWS env variable is not set.")

            views = importlib.import_module(module_path)

            if hasattr(views, method_name):
                task_method = getattr(views, method_name)
                if callable(task_method):
                    return task_method(*args, **kwargs)
                else:
                    logger.error(f"Attribute '{method_name}' exists but is not callable.")
            else:
                logger.warning(f"No method named '{method_name}' found in module '{module_path}'.")
        except Exception as e:
            logger.error(f"Error in run_dynamic_methods: {e}", exc_info=True)

    def validateSession(self, request, data):
        """Checks if a session exists and is valid."""
        try:
            phoneNumber = data.get("phoneNumber", "")
            session = Session.objects.filter(
                phoneNumber=phoneNumber).first()  # Fix: Use .filter().first()

            if session and session.is_session_expired():
                print(f"Session expired for {phoneNumber}. Creating a new session.")
                session.delete()
                self.createNewSession(phoneNumber)
                return request
            elif session:
                print(f"Valid session found for {phoneNumber}.")
                self.validateProfileExists(request, data)
                return request
            else:
                print(f"No session found for {phoneNumber}. Creating a new session.")
                self.validateProfileExists(request, data)  # Handle case where no session exists
                self.createNewSession(phoneNumber)
                return request
        except Exception as e:
            logger.error(f"Error in validateSession: {e}", exc_info=True)

    def validateProfileExists(self, request, data):
        """Ensures a profile exists before proceeding."""
        phoneNumber = data.get("phoneNumber", "")
        username = data.get("userName", "")

        profile, created = Profile.objects.get_or_create(
            phoneNumber=phoneNumber, defaults={"username": username})

        if created:
            print(f"New profile created for {phoneNumber}.")
            return request
        else:
            print(f"Profile exists for {phoneNumber}.")
            return request

    def createNewSession(self, phoneNumber):
        """Creates a new session for the user."""
        profile = Profile.objects.filter(phoneNumber=phoneNumber).first()
        if not profile:
            print(f"Cannot create session. No profile found for {phoneNumber}.")
            return None  # Don't create a session without a profile

        session = Session.objects.create(
            isValidSession=True,
            phoneNumber=phoneNumber,
            user=profile
            # Fix: Ensure session links to profile
        )
        print(session.id)
        print(f"New session created for {phoneNumber}.")
        return session
