import json, re, bcrypt, jwt

from django.views         import View
from django.http          import JsonResponse

from .models              import User, Class

from my_settings          import SECRET_KEY, ALGORITHM
from decorators           import login_decorator, admin_only

class SignupView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            phone           = data['phone']
            password        = data['password']
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

            if User.objects.filter(phone=phone).exists():
                return JsonResponse({"MESSAGE": "PHONE_ALREADY_EXIST"}, status=400)

            if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password):
                return JsonResponse({"MESSAGE": "INVALID_FORMAT"}, status=400)

            User.objects.create(
                phone        =   phone,
                password     =   hashed_password.decode('UTF-8'),
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

class SigninView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)      
            phone    = data['phone']
            password = data['password']        

            if not User.objects.filter(phone = phone).exists():
                return JsonResponse({'MESSAGE':'INVALID_VALUE'}, status = 401)

            user = User.objects.get(phone=phone)

            if bcrypt.checkpw(password.encode('utf-8'),user.password.encode('utf-8')):
                
                token = jwt.encode({'user_id':User.objects.get(phone=phone).id, "role": user.role}, SECRET_KEY, algorithm=ALGORITHM)
            
                return JsonResponse({'TOKEN': token, "phone":phone, "role": user.role}, status = 200)

            return JsonResponse({'MESSAGE':'INVALID_USER'}, status = 401)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class ClassView(View):
    @admin_only
    def post(self, request):
        try:
            data       = json.loads(request.body)
            name       = data['name']

            if Class.objects.filter(name = name).exists():
                return JsonReponse({'MESSAGE': 'SAME_NAME_EXIST'}, status = 401)

            Class.objects.create(
                    name       = name,
                    location   = data['location'],
                    class_type = data['class_type'],
                    price      = data.get('price') if data.get('price') is not None else 1,
                    capacity   = data.get('capacity') if data.get('capacity') is not None else 20,
                    date       = data['date'],
                    start_at   = data['start_at'],
                    end_at     = data['end_at']
                )
            
            return JsonResponse({'MESSAGE': 'CLASS_CREATED'}, status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)