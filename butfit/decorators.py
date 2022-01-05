import jwt

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings            import SECRET_KEY, ALGORITHM
from butfitapp.models                import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token         = request.headers.get("Authorization", None)
            user          = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            request.user  = User.objects.get(id = user['id'])

            return func(self, request, *args, **kwargs)

        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "DECODE_ERROR"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    return wrapper

def admin_only(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            pay_load     = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            role         = pay_load['role']
            user         = User.objects.get(id=pay_load['user_id'])
            request.user = user
            
            if role == 'admin':
                return func(self, request, *args, **kwargs)
            else:
                return JsonResponse({'message': 'UNAUTHORIZED'}, status=401)

        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    return wrapper

