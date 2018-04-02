from Algorithms import ALGORITHMS

#This is the welcome message for when a user starts the skill without a specific intent.
WELCOME_MESSAGE = ("Welcome to the Big O notation! What would you like to know?")

#This is the message a user will hear when they ask Alexa for help in your skill.
HELP_MESSAGE = ("Help help help!")

#This is the message a user will hear when the session is ended.
SESSION_ENDED_MESSAGE = ("Bye bye")

# --------------- entry point -----------------

def lambda_handler(event, context):
    """ App entry point  """

    if event['request']['type'] == "LaunchRequest":
        return on_launch()
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'])

# -------------- events  ---------------------------------

def on_launch():
    return response(response_plain_text(SESSION_ENDED_MESSAGE, False))

def on_intent(request, session):
    return do_help()

def on_session_ended(request):
    return response(response_plain_text(HELP_MESSAGE, True))

# -------------- functions ---------------------------------

def do_help():
    return response(response_plain_text(HELP_MESSAGE, False))

# --------------- speech response handlers -----------------

def response(speech_response, attributes={}):
    """ create a simple json response """

    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speech_response
    }

def response_plain_text(message, endsession):
    """ create a simple json plain text response  """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': message
        },
        'shouldEndSession': endsession
    }
