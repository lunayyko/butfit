import json, bcrypt, jwt, binascii, os

from django.http           import JsonResponse
from drf_yasg              import openapi
from drf_yasg.utils        import swagger_auto_schema
from rest_framework.views  import APIView
# from rest_framework.views  import CreateAPIView

from core.decorators       import login_required, admin_only
from my_settings           import SECRET_KEY, ALGORITHM, ADMIN_TOKEN
from .models               import User
from .serializers          import UserSerializer

class SignupView(APIView):
    @swagger_auto_schema (
        request_body = UserSerializer, 
        responses    = {
            "201": "SUCCESS",
            "400": "BAD_REQUEST" 
        },
        operation_id          = "회원가입",
        operation_description = "핸드폰 번호와 비밀번호(영문, 숫자, 특수기호를 1개씩 포함해야합니다)를 입력하여 가입할 수 있습니다"
    )
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
                password     =   hashed_password.decode('UTF-8')
            )
            
            access_token = jwt.encode({'user': user.phone, 'role': user.role}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'MESSAGE': 'SUCCESS', 'access_token': access_token}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class SigninView(APIView):
    @swagger_auto_schema (
        request_body = UserSerializer,
        responses    = {
            "200": "SUCCESS",
            "400": "BAD_REQUEST"
        },
        operation_id          = "로그인",
        operation_description = "전화번호와 비밀번호 입력이 필요합니다."
    )
    def post(self, request):
        try: 
            data       = json.loads(request.body)
            phone      = data['phone']
            password   = data['password']

            if not User.objects.filter(phone = phone).exists():
                    return JsonResponse({'MESSAGE':'NOT_VALID_USER'}, status = 401)

            if bcrypt.checkpw(password.encode('utf-8'),User.objects.get(phone=phone).password.encode('utf-8')):
                token = jwt.encode({'user_id': user.id, 'role': user.role}, SECRET_KEY, ALGORITHM)
            
                return JsonResponse({'token': token, "phone": phone}, status = 200)

            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

# class ClassView(CreateAPIView):
#     @swagger_auto_schema (
#         request_body = ClassSerializer,
#         responses    = {
#             "200": "SUCCESS",
#             "400": "BAD_REQUEST"
#         },
#         operation_id          = "수업 생성",
#         operation_description = "수업이름, 장소, 가격(크레딧), 수업날짜, 시작시간, 종료시간을 입력합니다"
#     )
#     @admin_only
#     def post(self, request):
#         try: 
#             data       = json.loads(request.body)
#             name       = data['name']
#             location   = data['location']
#             class_type = data['class_type']
#             price      = data['price']
#             capacity   = data['capacity']
#             date       = data['date']
#             start_at   = data['start_at']
#             end_at     = data['end_at'] 

#             if not User.objects.filter(phone = phone).exists():
#                     return JsonResponse({'MESSAGE':'NOT_VALID_USER'}, status = 401)

#             if bcrypt.checkpw(password.encode('utf-8'),User.objects.get(phone=phone).password.encode('utf-8')):
#                 token = jwt.encode({'user_id': user.id, 'role': user.role}, SECRET_KEY, ALGORITHM)
            
#                 return JsonResponse({'token': token, "phone": phone}, status = 200)

#             return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

#         except KeyError:
#             return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)