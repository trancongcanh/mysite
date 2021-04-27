from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth


class AutoLogout(object):
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """
        return None

    def process_exception(self, request, exception):
        """
        Called when a view raises an exception.
        """
        return None

    def process_template_response(self, request, response):
        """
        Called just after the view has finished executing.
        """
        return response
    def process_request(self, request):
        if not request.user.is_authenticated() :
            #Can't log out if not logged in
            return

        try:
            if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                del request.session['member_id']
                del request.session['last_touch']
                return
        except KeyError:
            pass

        request.session['last_touch'] = datetime.now()