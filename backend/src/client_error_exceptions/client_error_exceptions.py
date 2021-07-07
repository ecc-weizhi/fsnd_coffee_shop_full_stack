class ClientErrorException(Exception):
    def get_status_code(self): return self._STATUS_CODE


class BadRequest(ClientErrorException):
    _MESSAGE = "Problems parsing JSON"
    _STATUS_CODE = 400

    def get_message(self): return BadRequest._MESSAGE


class NotFound(ClientErrorException):
    _STATUS_CODE = 404

    def __init__(self, entity, entity_id):
        self.entity = entity
        self.entity_id = entity_id

    def get_message(self):
        return f"{self.entity} with id {self.entity_id} not found"


class UnprocessableEntity(ClientErrorException):
    _STATUS_CODE = 422

    def __init__(self, message="Error processing request"):
        self.message = message

    def get_message(self):
        return self.message

    @staticmethod
    def missing_fields(fields):
        """
        Instantiate a new UnprocessableEntity object with missing fields error message
        :param fields: list of fields that are missing from request body
        :return: a new UnprocessableEntity object with missing fields error message
        """
        return UnprocessableEntity(f"Required field(s) missing from request body: {fields}")