# Flask HTTP Middleware
<!-- [![Downloads](https://static.pepy.tech/personalized-badge/fastapi-simple-crud?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/fastapi-simple-crud) -->

## Repository
- [ ] [GITHUB](https://github.com/Danangjoyoo/flask-http-middleware)

## Installation
```
pip install flask-http-middleware
```

## Description
Flask HTTP Middleware with starlette's (FastAPI) BaseHTTPMiddleware style. Manage your middleware directly from `request` to `response` easily

## Changelogs
- v0.0
    - First Upload

## How to use ?

### Example: adding a response header
```
import time
from flask import Flask
from flask_http_middleware import MiddlewareManager, BaseHTTPMiddleware

app = Flask(__name__)

class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self):
        super().__init__()
    
    def dispatch(self, request, call_next):
        t0 = time.time()
        response = call_next(request)
        response_time = time.time()-t0
        response.headers.add("response_time", response_time)
        return response

app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(MetricsMiddleware)

@app.get("/health")
async def health():
    return {"message":"I'm healthy"}

if __name__ == "__main__":
    app.run()
```
- Note: you can put your `MetricsMiddleware` class in different file

Above example is equals with `app.before_request` and `app.after_request` decorated function.

```
@app.before_request
def start_metrics():
    g.t0 = time.time()

@app.after_request
def stop_metrics(response):
    response_time = time.time()-g.t0
    response.headers.add("response_time", response_time)
    return response
```

---

### Example: Authentication
```
import time
from flask import Flask, jsonify
from flask_http_middleware import MiddlewareManager, BaseHTTPMiddleware

app = Flask(__name__)

class AccessMiddleware(BaseHTTPMiddleware):
    def __init__(self):
        super().__init__()
    
    def dispatch(self, request, call_next):
        if request.headers.get("token") == "secret":
            return call_next(request)
        else:
            return jsonify({"message":"invalid token"})

app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(AccessMiddleware)

@app.get("/health")
async def health():
    return {"message":"I'm healthy"}

if __name__ == "__main__":
    app.run()
```

---

### Example: add some routers security
```
import time
from flask import Flask, jsonify
from flask_http_middleware import MiddlewareManager, BaseHTTPMiddleware

app = Flask(__name__)

class SecureRoutersMiddleware(BaseHTTPMiddleware):
    def __init__(self, secured_routers = []):
        super().__init__()
        self.secured_routers = secured_routers
    
    def dispatch(self, request, call_next):
        if request.path in self.secured_routers:
            if request.headers.get("token") == "secret":
                return call_next(request)
            else:
                return jsonify({"message":"invalid token"})
        else:
            return call_next(request)

secured_routers = ["/check_secured"]

app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(SecureRoutersMiddleware, secured_routers=secured_routers)

@app.get("/health")
async def health():
    return {"message":"I'm healthy"}

@app.get("/check_secured")
async def health():
    return {"message":"Security bypassed"}

if __name__ == "__main__":
    app.run()
```

---

### Example: add error handling
```
import time
from flask import Flask, jsonify
from flask_http_middleware import MiddlewareManager, BaseHTTPMiddleware

app = Flask(__name__)

class AccessMiddleware(BaseHTTPMiddleware):
    def __init__(self):
        super().__init__()
    
    def dispatch(self, request, call_next):
        if request.headers.get("token") == "secret":
            return call_next(request)
        else:
            raise Exception("Authentication Failed)
    
    def error_handler(self, error):
        return jsonify({"error": str(error)})

app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(AccessMiddleware)

@app.get("/health")
async def health():
    return {"message":"I'm healthy"}

if __name__ == "__main__":
    app.run()
```