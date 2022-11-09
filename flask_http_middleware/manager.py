import sys
import typing as t
from flask import Flask, g, request_started, request_finished, request
from werkzeug.wrappers import Request, Response

from .base import BaseHTTPMiddleware

class MiddlewareManager():
    def __init__(self, app: Flask):
        self.app = app
        self.middleware_stack = []
        self.stacked_dispatch = None

        @app.before_request
        def create_middleware_stack():
            g.middleware_stack = self.middleware_stack.copy()

    def add_middleware(self, middleware_class, **options):
        if BaseHTTPMiddleware.__subclasscheck__(middleware_class):
            self.middleware_stack.insert(0, middleware_class(**options))
        else:
            raise Exception("Error Middleware Class : not inherited from BaseHTTPMiddleware class")

    def process_request_and_get_response(self, request: Request) -> Response:
        if g.middleware_stack:
            try:
                mw = g.middleware_stack.pop()
                return mw._dispatch_with_handler(request, self.process_request_and_get_response)
            except Exception as e:
                return self.process_request_and_handle_exception(e)
            finally:
                g.middleware_stack.append(mw)
        rv = self.dispatch_request(request)
        return self.app.make_response(rv)

    def process_request_and_handle_exception(self, error) -> Response:
        rv = self.app.handle_user_exception(error)
        return self.app.make_response(rv)

    def __call__(self, environ, start_response):
        ctx = self.app.request_context(environ)
        error: t.Optional[BaseException] = None
        try:
            try:
                ctx.push()
                self.app.try_trigger_before_first_request_functions()
                try:
                    request_started.send(self)
                    rv = self.app.preprocess_request()
                    if rv is None:
                        response = self.process_request_and_get_response(request)
                except Exception as e:
                    response = self.process_request_and_handle_exception(e)
                try:
                    response = self.app.process_response(response)
                    request_finished.send(self, response=response)
                except Exception:
                    self.app.logger.exception(
                        "Request finalizing failed with an error while handling an error"
                    )
            except Exception as e:
                error = e
                response = self.app.handle_exception(e)
            except:
                error = sys.exc_info()[1]
                raise
            return response(environ, start_response)
        finally:
            if self.app.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)

    def preprocess_request(self, request):
        names = (None, *reversed(request.blueprints))
        for name in names:
            if name in self.app.url_value_preprocessors:
                for url_func in self.app.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)
        for name in names:
            if name in self.app.before_request_funcs:
                for before_func in self.app.before_request_funcs[name]:
                    try:
                        rv = self.app.ensure_sync(before_func)()
                    except:
                        rv = before_func()
                    if rv is not None:
                        return rv
        return None

    def dispatch_request(self, request):
        req = request
        if req.routing_exception is not None:
            self.app.raise_routing_exception(req)
        rule = req.url_rule
        if (
            getattr(rule, "provide_automatic_options", False)
            and req.method == "OPTIONS"
        ):
            return self.app.make_default_options_response()
        try:
            return self.app.ensure_sync(self.app.view_functions[rule.endpoint])(**req.view_args)
        except:
            return self.app.view_functions[rule.endpoint](**req.view_args)