#This is the welcome message for when a user starts the skill without a specific intent.
WELCOME_MESSAGE = ("Welcome to the Big O notation!"
                    " With this skill, you can learn time and space complexity of common sorting algorithms."
                    " What would you like to know?")

#This is the message a user will hear when they ask Alexa for help in your skill.
HELP_MESSAGE = ("With this skill, you can learn time and space complexity of common sorting algorithms."
                " You can ask about time complexity of quicksort, mergesort, and other sorting algorithms."
                " What would you like to know?")

#This is the message a user will hear when the session is ended.
SESSION_ENDED_MESSAGE = ("Come back next time you would like to know more about big O notation. Bye bye!")

# This is the message a user will hear when there is no intent match.
ELSE_MESSAGE = ("I'm sorry, I don't know that...")

# --------------- algorithms data

class Algorithm:
    def __init__(self, name, bestTimeComplexity, averageTimeComplexity, worstTimeComplexity, spaceComplexity):
        self.name = name
        self.bestTimeComplexity = bestTimeComplexity
        self.averageTimeComplexity = averageTimeComplexity
        self.worstTimeComplexity = worstTimeComplexity
        self.spaceComplexity = spaceComplexity

ALGORITHMS = {}
ALGORITHMS['quicksort'] = Algorithm("Quicksort", "n log(n)", "n log(n)", "n^2", "log(n)")
ALGORITHMS['mergesort'] = Algorithm("Mergesort", "n log(n)", "n log(n)", "n log(n)", "n")
ALGORITHMS['timsort'] = Algorithm("Timsort", "n", "n log(n)", "n log(n)", "n")
ALGORITHMS['heapsort'] = Algorithm("Heapsort", "n log(n)", "n log(n)", "n log(n)", "1")
ALGORITHMS['bubble sort'] = Algorithm("Bubble Sort", "n", "n^2", "n^2", "1")
ALGORITHMS['insertion sort'] = Algorithm("Insertion Sort", "n", "n^2", "n^2", "1")
ALGORITHMS['selection sort'] = Algorithm("Selection Sort", "n^2", "n^2", "n^2", "1")
ALGORITHMS['tree sort'] = Algorithm("Tree Sort", "n log(n)", "n log(n)", "n^2", "n")
ALGORITHMS['bucket sort'] = Algorithm("Bucket Sort", "n+k", "n+k", "n^2", "n")
ALGORITHMS['radix sort'] = Algorithm("Radix Sort", "n*k", "n*k", "n*k", "n+k")
ALGORITHMS['counting sort'] = Algorithm("Counting Sort", "n+k", "n+k", "n+k", "k")
ALGORITHMS['cubesort'] = Algorithm("Cubesort", "n", "n log(n)", "n log(n)", "n")

# --------------- entry point

def lambda_handler(event, context):
    """ App entry point  """

    if event['request']['type'] == "LaunchRequest":
        return on_launch()
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'])

# -------------- events

def on_launch():
    return response(response_plain_text(WELCOME_MESSAGE, False))

def on_intent(request, session):
    intent_name = request['intent']['name']
    print("on_intent: " + intent_name)

    try:
        if intent_name == "WorstTimeComplexity":
            return say_worst_time_complexity(request)
        elif intent_name == "BestTimeComplexity":
            return say_best_time_complexity(request)
        elif intent_name == "AverageTimeComplexity":
            return say_average_time_complexity(request)
        elif intent_name == "SpaceComplexity":
            return say_space_complexity(request)
        elif intent_name == "AMAZON.HelpIntent":
            return do_help()
        elif intent_name == "AMAZON.StopIntent":
            return do_stop()
        elif intent_name == "AMAZON.CancelIntent":
            return do_stop()
        else:
            return do_global_else()
    except Exception:
        print("Exception happened during intent processing.")

    return do_global_else()

def on_session_ended(request):
    return response(response_plain_text(SESSION_ENDED_MESSAGE, True))

# -------------- functions

def do_help():
    return response(response_plain_text(HELP_MESSAGE, False))

def do_stop():
    return response(response_plain_text(SESSION_ENDED_MESSAGE, True))

def say_worst_time_complexity(request):
    a = get_sorting_algorithm(request)
    m = "The worst time complexity of {0} is {1}".format(a.name, a.worstTimeComplexity)
    return response(response_plain_text(m, True))

def say_best_time_complexity(request):
    a = get_sorting_algorithm(request)
    m = "The best time complexity of {0} is {1}".format(a.name, a.bestTimeComplexity)
    return response(response_plain_text(m, True))

def say_average_time_complexity(request):
    a = get_sorting_algorithm(request)
    m = "The average time complexity of {0} is {1}".format(a.name, a.averageTimeComplexity)
    return response(response_plain_text(m, True))

def say_space_complexity(request):
    a = get_sorting_algorithm(request)
    m = "The space complexity of {0} is {1}".format(a.name, a.spaceComplexity)
    return response(response_plain_text(m, True))

def do_global_else():
    return response(response_plain_text(ELSE_MESSAGE, True))

def get_sorting_algorithm(request):
    slot = request['intent']['slots']['SortingAlgorithm']['value']
    a = ALGORITHMS[slot.lower()]
    return a

# --------------- speech response handlers

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
