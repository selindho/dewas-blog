# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from BlogApp.models import *
from datetime import datetime
from django.contrib.auth.models import User


def show_home(request):
    posts = BlogPost.getAll()

    if request.user.is_authenticated() and request.user.is_active():
        action = '/logout/'
        label = 'Logout'
    else:
        action = '/login/'
        label = 'Login'

    if 'valid' not in request.session or request.session['valid'] != 'True':
        request.session['valid'] = 'True'
        request.session['start'] = datetime.now()
        request.session['visited'] = '0'
        request.session['edited'] = '0'
        request.session['created'] = '0'
        request.session['deleted'] = '0'

    params = {'start': request.session['start'],
              'visited': request.session['visited'],
              'edited': request.session['edited'],
              'created': request.session['created'],
              'deleted': request.session['deleted']}

    return render_to_response("home_temp.html", {'action': action, 'label': label, 'posts': posts, 'stats': params},
                              context_instance=RequestContext(request))


def edit_blog(request, id):
    post = BlogPost.getById(id)

    if post is None:
        return HttpResponse("Not found!")

    elif request.method == "POST" and 'content' in request.POST:
        if request.POST['version'] == str(post.version):
            post.content = request.POST['content'].strip()
            post.title = request.POST['title']
            post.timestamp = datetime.now()
            post.version += 1
            post.save()

            request.session['edited'] = int(request.session['edited']) + 1

            return HttpResponseRedirect("/myblog/")

        else:
            return render_to_response('version_error.html', {'id': post.id,
                                                             'serverversion': post.version,
                                                             'servertitle': post.title,
                                                             'servercontent': post.content,
                                                             'clientversion': request.POST['version'],
                                                             'clienttitle': request.POST['title'],
                                                             'clientcontent': request.POST['content']},
                                      context_instance=RequestContext(request))

    else:
        return render_to_response('edit_blog_temp.html', {'title': post.title, 'content': post.content, 'id': post.id,
                                                          'version': post.version},
                                  context_instance=RequestContext(request))


def show_blog(request, id):
    post = BlogPost.getById(id)

    if post is None:
        return HttpResponse("No such post found!")

    else:
        request.session['visited'] = int(request.session['visited']) + 1
        return render_to_response('show_blog_temp.html', {'title': post.title, 'timestamp': post.timestamp,
                                  'content': post.content}, context_instance=RequestContext(request))


def add_blog(request):
    post = BlogPost(title='Untitled Post', content='', timestamp=datetime.now())
    post.save()
    request.session['created'] = int(request.session['created']) + 1
    return render_to_response('message.html', {'message': 'Blog added successfully!', 'redirect': '/myblog/'},
                              context_instance=RequestContext(request))


def delete_blog(request, id):
    post = BlogPost.getById(id)

    if post is None:
        return HttpResponse("No such post found!")

    else:
        post.delete()
        request.session['deleted'] = int(request.session['deleted']) + 1
        return render_to_response('message.html', {'message': 'Successfully deleted blog!', 'redirect': '/myblog/'},
                                  context_instance=RequestContext(request))


def reset_stats(request):
    request.session['valid'] = 'False'

    return HttpResponseRedirect('/myblog/')


def create_user(request):
    if request.method == 'POST' and 'user' in request.POST and 'password' in request.POST:
        try:
            user = User.objects.create_user(username=request.POST['user'], password=request.POST['password'], email=None)
            return render_to_response('message.html', {'message': 'User created!', 'redirect': '/myblog/'},
                                      context_instance=RequestContext(request))
        except:
            return render_to_response('message.html', {'message': 'User exists!', 'redirect': '/createuser/'},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('create_user.html', {'title': 'Create User'},
                                  context_instance=RequestContext(request))