from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from chatbot_session_flow.models import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import requests
import json
import os
from types import MethodType
from django.views.decorators.csrf import csrf_exempt
from distutils.util import strtobool


# Create your views here.

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token , created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@csrf_exempt
@api_view(['POST'])
def sendWhatsappMessageViaNgumzo(request):
    run_dynamic_methods("sendWhatsappMessage",
        session="session", phoneNumber="phoneNumber", message="message")
    return Response({"response" : res})

@api_view(['POST'])
def messageCallback(request):
    print(request.data)
    validateOptionMessage(request)
    return Response({"response" : "success"})

def getSessionStepper(request):
    session = Session.objects.get(
        phoneNumber=request.json_data.get("from", ""),
    )
    stepper = Stepper.objects.filter(
        session=session, isCurrent=True).first()
    return session, stepper

def createSaveData(session, page: Page, message:str):
    print("Creating Saved Data -> " + message)
    try:
        if page.pageType == "collect":
            collectedData = CollectedData(
                page = page,
                session = session,
                key = page.fieldName,
                value = message)
            collectedData.save()
    except Exception as e:
        print("Exception -> {}".format(e))

def call_dymanic_method(session, page: Page, message:str):
    print("Call Dynamic method -> " + message)
    if page.task is not None:
        perform_dynamic_action(session, page, message)

def getSessionVariables(session):
    try:
        collectedData = CollectedData.objects.filter(
            session = session
        )
        data = {}
        for cData in collectedData:
            data[cData.key] = cData.value
        return data
    except:
        return { }

def validateOptionMessage(request):
    session, stepper = getSessionStepper(request)
    if stepper:
        currentPage = stepper.page
        message = request.json_data.get("message", "")
        createSaveData(session, stepper.page.prev, message)
        run_dynamic_methods(stepper.page.prev, session=session,
            page=stepper.page.prev, message=message)
        if message:
            print("Message Sent : {}".format(message))
            try:
                messageOption = int(message.strip())
                if messageOption:
                    print("Message Option : {}".format(str(messageOption)))
                    mOption = PageOption.objects.get(
                        numberOnScreen=messageOption, page=currentPage)
                    if mOption:
                        print("mOption : Found")
                        stepperCreated = Stepper(
                            session=session,
                            isCurrent=True,
                            page=mOption.next_page
                        )
                        stepper.isCurrent = False
                        stepper.save()
                        stepperCreated.save()
                        sendTheMessage(request)
                    else:
                        # Message Option passed is missing send error screen
                        print("mOption : !Found")
                        pass
                else:
                    print("Message Option : !Found")
            except Exception as e:
                # Pass method here for continuation value is string or word or sentence
                print("Error ->  : {}".format(e))
                sendTheMessage(request)
    else:
        # Go to next page info is insignificant ie Hi, hello etc
        sendTheMessage(request)


def sendTheMessage(request):
    print(str(request.json_data))
    session, stepper = getSessionStepper(request)
    if stepper:
        currentPage = stepper.page
        sendMessage(request, session, stepper, currentPage)
    else:
        page = Page.objects.filter().first()
        stepperCreated = Stepper(
            session=session,
            isCurrent=True,
            page=page
        )
        stepperCreated.save()
        sendMessage(request, session, stepperCreated, page)

def validatePrevious(request, session, stepperCreated, page):
    prevPage = page
    if prevPage:
        pageType = page.pageType
        if pageType == "options":
            message = request.json_data.get("message", "")
            pageOption = PageOption.objects.filter(
                page=prevPage, numberOnScreen=int(message)).first()
            stepperCreated.page = pageOption.next_page
            sendMessage(request, session, stepperCreated, page)
    else:
        sendMessage(request, session, stepperCreated, page)
    sendMessage(request, session, stepperCreated, page)


def sendMessage(request, session: Session, stepper: Stepper, currentPage: Page):
    if not session or not currentPage:
        print("Invalid session or page")
        return

    message = f"Sending message for {currentPage.title}"
    print(message)
    pageType = currentPage.pageType

    sendOptionMessages(request,
        session, stepper, currentPage)
    # Simulate sending message
    print(f"Session {session.id}: {message}")
    moveToNextPage(request, session, currentPage, stepper)

def moveToNextPage(request, session, currentPage, stepper):
    # Move to the next step if available
    if currentPage.next_page:
        print(f"Moving from {currentPage.title} to {currentPage.next_page.title}")
        passTheBaton(request, session, currentPage, stepper)  # Assuming you have a function to move forward
    else:
        # raise Exception, should be closed.
        print("End of stepper reached.")


def sendOptionMessages(request, session: Session, stepper: Stepper, currentPage: Page):
    message = currentPage.message + "\n" + getMessageToSendForOptions(currentPage)
    print("message : {}".format(message))
    useNgumzo = os.environ.get("USE_NGUMZO_APIS")
    useNgumzo = bool(strtobool(useNgumzo))
    sendWhatsappMessageViaNgumzo(session,
        session.phoneNumber, message, useNgumzo)
    # moveToNextPage(session, currentPage, stepper)


def getMessageToSendForOptions(page):
    pageOptions = PageOption.objects.filter(page=page)
    messageOptions = "\n\n"
    if pageOptions is not None and len(pageOptions) > 0:
        for i in range(len(pageOptions)):
            pageOption = pageOptions[i]
            if pageOption is not None:
                messageOptions += "{}). {} \n".format(
                    pageOption.numberOnScreen, pageOption.label)
    else:
        print("Def Jaaaaaammmm ====> ")
    return messageOptions



def passTheBaton(request, session: Session, currentPage: Page, stepper:Stepper):
    stepper.isCurrent = False
    stepper.save()
    nextPage = currentPage.next_page
    stepperCreated = Stepper(
        session=session,
        isCurrent=True,
        page=nextPage
    )
    stepperCreated.save()

    print(f"Transitioned from {currentPage} to {currentPage.next_page}")

    if nextPage.pageType == "continuation":
        print(f"Transitioned from {currentPage} to {currentPage.next_page} a continuation page")
        sendTheMessage(request)


def sendWhatsappMessageViaNgumzo(session, phoneNumber, message, useNgumzo):
    res = {}
    if useNgumzo:
        url = "https://ngumzo.com/v1/send-message"

        payload = json.dumps({
            "sender": "254716554593",
            "recipient": phoneNumber,
            "message": message
        })
        headers = {
            'Content-Type': 'application/json',
            'api-key': os.environ.get('NGUMZO_API_KEY')
        }

        # response = requests.request("POST",
        #     url, headers=headers, data=payload)
        print(message.format_map(getSessionVariables(session)))
        # res = response.text
        # print(res)
        res = {}
    else:
        run_dynamic_methods("sendWhatsappMessage",
            session=session, phoneNumber=phoneNumber, message=message)
    return Response({"response" : res})

def run_dynamic_methods(method_name, *args, **kwargs):
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
                print(f"Attribute '{method_name}' exists but is not callable.")
        else:
            print(f"No method named '{method_name}' found in module '{module_path}'.")
    except Exception as e:
        print(f"Error in run_dynamic_methods: {e}")