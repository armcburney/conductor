import json
import logging
from websocket_responses.response_to_object_mappings import object_mappings

logger = logging.getLogger("Response Factory")

class ResponseFactory():

    @classmethod
    def parse_response(cls, response):
        json_response = json.loads(response)

        command = json_response[0]

        response_type = object_mappings.get(command, None)

        if response_type is None:
            logger.warning('Ignoring response with command "{}"'.format(command))
            return None

        return response_type.process_response(json_response)
