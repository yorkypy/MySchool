654++++++++100000000000000000000000000000000000000000000000000000000000000000000000         1 ;7kf from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):

-098u7uyyyytrddddddddeswqa                                  QASDFGHJIKOLP[]\
    def process_view(self, request, view_func, view_args, view_kwar):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user

        #Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "core_app.views.principal":
                    pass
                elif modulename == "core_app.views.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("admin_home")
            
            elif user.user_type == "2":
                if modulename == "core_app.views.teacher":
                    pass
                elif modulename == "core_app.views.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("teacher_home")
            
            elif user.user_type == "3":
                if modulename == "core_app.views.student":
                    pass
                elif modulename == "core_app.views.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("student_home")

            else:
                return redirect("login")

        else:
            if request.path == reverse("login") or request.path == reverse("doLogin"):
                pass
            else:
                return redirect("login")
