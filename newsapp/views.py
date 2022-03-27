import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewsStories, Authors
from django.views.decorators.http import require_http_methods

category_list = ['tech', 'pol', 'art', 'trivia']
region_list = ['uk', 'w', 'eu']


@csrf_exempt
def user_register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
    is_exist = True
    try:
        user = Authors.objects.get(username=username, password=password)
    except Authors.DoesNotExist:
        is_exist = False

    if is_exist:
        return build_response('The user already exists', 401)

    Authors(username=username, password=password).save()
    return build_response('Register successfully!', 200)


@csrf_exempt
def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        user = Authors.objects.get(username=username, password=password)
    except Authors.DoesNotExist:
        return build_response('user not exist', 401)
    if password == user.password:
        rep = build_response('login successfully, have fun!', 200)
        rep.set_cookie('login', True)
        rep.set_cookie('uname', username)
        return rep
    else:
        return build_response('UserName or Password not Right!', 405)


@csrf_exempt
def user_logout(request):
    check_login(request)

    rep = build_response("--- Successfully logged off", 200)
    rep.delete_cookie('login')
    rep.delete_cookie('uname')
    return rep


@csrf_exempt
def post_story(request):
    check_login(request)
    if request.method != 'POST':
        return HttpResponse(status=405, content_type='text/plain')

    try:
        authname = Authors.objects.get(username=request.COOKIES.get('uname'))
    except Authors.DoesNotExist:
        return build_response("--- You haven't logged in yet", 400)

    story = json.loads(request.body)

    # check category and region
    if story['category'] not in category_list and story['region'] not in region_list:
        return build_response("--- Invalid region or category", 503)

    story = NewsStories(headline=story['headline'], category=story['category'], author=authname,
                        details=story['details'], region=story['region'])
    story.save()
    return build_response("--- POST successful", 201)


@csrf_exempt
def get_story(request):
    req_data = json.loads(request.body)  # a piece of story
    stories = NewsStories.objects.all()  # all stories
    stoty_list = []
    check_login(request)

    print(req_data)
    if req_data.get("key", None):
        stories = stories.filter(key=req_data['key'])

    if req_data.get("category", None):
        stories = stories.filter(category=req_data['category'])

    if req_data.get("region", None):
        stories = stories.filter(region=req_data['region'])

    if req_data.get("date", None):
        construct_date = datetime.datetime.strptime(req_data.get('story_date'), "%d/%m/%Y").strftime("%Y-%m-%d")
        stories = stories.filter(date=construct_date)

    # print(stories)
    for story in stories:
        story_json_info = {'key': str(story.key), 'headline': story.headline, 'story_cat': story.category,
                           'story_region': story.region, 'author': story.author.username, 'story_date': str(story.date),
                           'story_details': story.details}
        stoty_list.append(story_json_info)

    if len(stoty_list) == 0:
        return build_response("--- No any story", status=404)
    rep = json.dumps({'stories': stoty_list})
    return HttpResponse(content=rep, content_type="application/json", status=200)


@csrf_exempt
@require_http_methods(["POST"])
def del_story(request):
    check_login(request)
    json_data = json.loads(request.body)

    have_story = NewsStories.objects.filter(pk=json_data.get('story_key')).exists()
    if not have_story:
        return HttpResponse("Story not exist :(", status=503, content_type='text/plain')

    NewsStories.objects.filter(pk=json_data.get('story_key')).delete()
    return build_response("Story deleted", status=201)


def build_response(msg: str, status: int):
    data = {
        "msg": msg
    }
    return JsonResponse(data, status=status)


def check_login(request):
    """
    login status check
    """
    if not request.COOKIES.get('login'):
        return build_response("--- You haven't logged in yet", 400)
