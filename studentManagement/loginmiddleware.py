# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.utils.deprecation import MiddlewareMixin


# class LoginCheckMiddleware(MiddlewareMixin):
#     def process_view(self,request,view_func,view_args,view_kwargs):
#         modulename=view_func.__module__
#         user=request.user
#         allowed_urls = [
#             reverse('log_out_user'),  # Add logout here
#         ]
        
        
#         if user.is_authenticated:
#             if user.user_type == "1":
#                 if modulename == 'studentManagement.HODViews':
#                     pass
#                 elif modulename == 'studentManagement.Views':
#                     return None
#                 else:
#                     return HttpResponseRedirect(reverse('admin_home'))
                
#             elif user.user_type == "2":
#                 if modulename == 'studentManagement.staffViews':
#                     return None
#                 elif modulename == 'studentManagement.Views':
#                     return None
#                 else:
#                     return HttpResponseRedirect(reverse('staff_home'))
                
#             elif user.user_type == "3":
#                 if modulename == 'studentManagement.studentViews':
#                     return None
#                 elif modulename == 'studentManagement.Views':
#                     return None
#                 else:
#                     return HttpResponseRedirect(reverse('student_home'))
#             else:
#                 return HttpResponseRedirect(reverse("show_login"))
                
            


#         else:
#             # if request.path == reverse('show_login') or request.path == reverse("doLogin"):
#             #     return None
#             if request.path in allowed_urls:
#                 return None
#             else:
#                 return HttpResponseRedirect(reverse('show_login'))