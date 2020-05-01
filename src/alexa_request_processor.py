import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from data_manager import DataManager

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "Welcome to the Transit Time skill, ask when the next bus is coming!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Transit Time", speech_text)).set_should_end_session(
        False).response

@sb.request_handler(can_handle_func=is_intent_name("GetBusStopTimeIntent"))
def get_bus_stop_time_intent_handler(handler_input):
    """Handler for Get bus stop time Intent."""
    # type: (HandlerInput) -> Response
    slots = handler_input.request_envelope.request.intent.slots

    # setting formatted bus name
    bus_slot = slots["busName"]
    bus_name = bus_slot.value.replace(" ", "").upper()
    
    bus_name = f"MTABC_{bus_name}"
    stop_name = slots["stopName"].value

    logger.info(f"INFO: Bus name: {bus_name}, Stop name: {stop_name}")
    bus_route = DataManager.get_bus_route(bus_name, stop_name, True)
    speech_text = str(bus_route)

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Bus Stop Time", speech_text)).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "You can ask when the next bus is coming!"

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Transit Time", speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Stopping."

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Transit Time", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The Transit Time skill can't help you with that.  "
        "You can ask when the next bus is coming!")
    reprompt = "You can ask when the next bus is arriving!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()