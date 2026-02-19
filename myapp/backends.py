from myapp.models import Users


class EmailBackend:
    def authenticate(self, request, email=None, password=None):
        try:
            user = Users.objects.get(email=email)
            if user.check_password(password):
                return user
        except Users.DoesNotExist:
            return None 
        return None
    
    def get_user(self, request, user_id):
        try:
            user = Users.objects.get(id=user_id)
            if not user:
                return None
            return user 
        except Users.DoesNotExist:
            return None