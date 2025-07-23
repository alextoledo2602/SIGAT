class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"\nRequest: {request.method} {request.path}")
        print(f"Headers: {dict(request.headers)}")
        print(f"Cookies: {request.COOKIES}\n")
        
        response = self.get_response(request)
        
        print(f"Response: {response.status_code}")
        print(f"Response Headers: {dict(response.items())}\n")
        
        return response