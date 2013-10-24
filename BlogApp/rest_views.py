from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from BlogApp.serializers import BlogPostSerializer
import base64
from django.contrib.auth import authenticate, login, logout


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# TODO: REST-API
# Sample JSON request:
#   {
#   "fields":
#   {
#   "title": "hello",
#   "content": "hello world!"
#   },
#   "model": "BlogPost"
#   }
@csrf_exempt
def blogs(request):
    # Authenticate user
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].partition(' ')
        clear_text = base64.b64decode(auth[2])
        split = str(clear_text, 'UTF-8').partition(':')
        user = authenticate(split[0], split[2])

    if user is not None and user.is_active:
        if request.method == 'POST':
            data = JSONParser().parse(request)
            print(data)
            serializer = BlogPostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return JSONResponse(serializer.data)
            else:
                return JSONResponse(serializer.errors, status=400)
    else:
        return HttpResponse(status=401)