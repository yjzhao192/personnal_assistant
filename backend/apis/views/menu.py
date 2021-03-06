import os
import yaml
import json

from django.http import JsonResponse
from django.views import View

from backend import settings
from authorization.models import User
from apis.models import App

import utils.response
from utils.auth import already_authorized, get_user
from utils.response import CommonResponseMixin, ReturnCode


def init_app_data():
    data_file = os.path.join(settings.BASE_DIR, 'app.yaml')
    with open(data_file, 'r', encoding='utf-8') as f:
        apps = yaml.load(f)
        return apps

def get_menu(request):
    # global_app_data = init_app_data()
    # published_apps = global_app_data['published']
    # return JsonResponse(data=published_apps, safe=False, status=200)
    print('get menu')
    query_set = App.objects.all()
    all_app = []
    for app in query_set:
        all_app.append(app.to_dict())
    print(all_app)
    response = utils.response.wrap_json_response(data=all_app)
    print(response)
    return JsonResponse(data=response, safe=False)


class UserMenu(View, CommonResponseMixin):
    def get(self, request):
        # 如果没登录，返回未鉴权
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(response, safe=False)
        # 否则返回用户定制的menu
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)
        menu_list = user.menu.all()

        user_menu = []
        for app in menu_list:
            user_menu.append(app.to_dict())
        response = self.wrap_json_response(data=user_menu, code=ReturnCode.SUCCESS)
        return JsonResponse(response, safe=False)

    def post(self, request):
        # 如果没登录，返回未鉴权
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(response, safe=False)
        user = get_user(request)
        post_menu = json.loads(request.body.decode('utf-8'))
        post_menu = post_menu.get('data')
        focus_menu = []
        print(post_menu)
        for item in post_menu:
            print(item)
            item = App.objects.get(appid=item.get('appid'))
            print(item)
            focus_menu.append(item)
        print(focus_menu)
        user.menu.set(focus_menu)
        user.save()
        response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS)
        return JsonResponse(response, safe=False)