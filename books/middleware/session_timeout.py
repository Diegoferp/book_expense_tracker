from datetime import datetime, timedelta
from django.utils.timezone import now
from django.contrib.auth import logout
from django.shortcuts import redirect


class InactivityTimeoutMiddleware:
    """Middleware to log out users after inactivity."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            timeout_seconds = 300  # 30 seconds for testing

            # Get the last activity timestamp from the session
            last_activity_str = request.session.get('last_activity')
            if last_activity_str:
                # Convert the string back to a datetime object
                last_activity = datetime.fromisoformat(last_activity_str)

                # Calculate elapsed time
                elapsed_time = (now() - last_activity).total_seconds()
                if elapsed_time > timeout_seconds:
                    # Log out the user and redirect to login page
                    logout(request)
                    return redirect('login')

            # Store the current timestamp as a string in ISO format
            request.session['last_activity'] = now().isoformat()

        response = self.get_response(request)
        return response
