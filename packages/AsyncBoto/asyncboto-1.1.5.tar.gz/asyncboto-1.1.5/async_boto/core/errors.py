class ClientError(Exception):
    "Raised when an API does not return a statuscode < 300"
    pass


class ErrorFactory:
    @staticmethod
    def create_exception(name, message, api_response):
        return type(
            name,
            (ClientError,),
            {
                "__init__": lambda self, msg=message: super(
                    self.__class__, self
                ).__init__(msg),
                "message": message,
                "error_type": name,
                "response": api_response,
            },
        )

    @staticmethod
    def raise_error_from_json(api_response: dict):
        error_type = api_response.get("__type", "GenericException").split("#")[-1]
        message = api_response.get("message", api_response)

        exc = ErrorFactory.create_exception(error_type, message, api_response)
        exc_obj = exc(message)
        raise exc_obj
