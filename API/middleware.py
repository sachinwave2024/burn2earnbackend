# API/middleware.py

class CorsDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("CORS middleware processing request")
        response = self.get_response(request)
        print("CORS middleware processed response")
        return response
