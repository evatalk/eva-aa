from random import choice
from controllers.eva_functions import EvaController


class MessageFlowHandler(object):

    @classmethod
    def get_response(cls, request, wit_response):
        """        
        From the intention contained in the user's
        message and the response to that intention
        chosen by the EVA controller, we will send
        the appropriate message to the user.
        """
        intent = cls._get_intent(wit_response)

        return cls._choose_intent_response(request, intent)

    @classmethod
    def _get_intent(cls, wit_response):
        """
        From the response of the request made to the WIT,
        we will discover the intention contained in the
        user's message.
        """
        try:
            # Que feio!
            intent = wit_response['entities']['intent'][0]['value']
        except KeyError:
            intent = "default"

        return intent

    @classmethod
    def _choose_intent_response(cls, request, intent):
        """
        After discovery the user's intention, we will send
        it to the EVA controller, so that can be chosen
        which treatment should be performed.
        """
        eva_response_controller = EvaController(intent, request)

        return eva_response_controller.response()
