import typing as t
from abc import ABC, abstractmethod
from flask import Request, Response

class BaseHTTPMiddleware(ABC):
    """
    BaseHTTPMiddleware

    A base class to create an HTTP Middleware by using dispatch function.
    Inherit this class to make it
    """
    @abstractmethod
    def __init__(self):
        """
        You have to add `__init__` function into your classes.
        Error will raised if you dont have this function
        """
        pass
    
    @abstractmethod
    def dispatch(self, request: Request, call_next: callable) -> Response:
        """
        You have to override this function in your custom middleware class.
        Error will raised if you dont have this function
        
        The templates are :
        ```
        def dispatch(self, request, call_next):
            ## put your pre-process/before-request here
            response = call_next(request)
            ## put your post-process/after-request here
            return response
        ```

        - you can add your `pre-process/before-request` or `post-process/after-request`
          inside the dispatch function
        - you could:
            - modify the `response`
            - return custom `response`
            - raise the `exception`
        """
        pass

    def error_handler(self, error: t.Any):
        """
        Override this function if you want to add error handling in your middleware.
        if not, any exception will be raised
        """
        raise error

    def _dispatch_with_handler(self, request, call_next):
        try:
            return self.dispatch(request, call_next)
        except Exception as e:
            return self.error_handler(e)