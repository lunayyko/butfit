import json, re, bcrypt, jwt, decimal
from datetime             import datetime
from decimal              import Decimal

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models              import User, Class, Credit, Booking, BookingLog

from my_settings          import SECRET_KEY, ALGORITHM
from core.decorators      import login_decorator, admin_only

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

class CreateClassView(View):
    @admin_only
    def post(self, request):
        try:
            data  = json.loads(request.body)
            name  = data['name']

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

class BuyCreditView(View):
    @login_decorator
    def post(self, request):
        try:
            data  = json.loads(request.body)

            Credit.objects.create(
                user_id    = request.user.id,
                credit     = data['number_of_credit'],
                expire_in  = data['expire_in']
            )
            return JsonResponse({'MESSAGE': 'CREDIT_BOUGHT'}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

class BookView(View):
    @login_decorator
    def post(self, request, class_id):
        try:
            if Booking.objects.filter(class_id_id = class_id).exists():
                return JsonResponse({'MESSAGE':'ALREADY_BOOKED'}, status = 401)
            class_v = Class.objects.get(id= class_id)

            if not Credit.objects.filter(user_id = request.user.id).exists():
                return JsonResponse({'MESSAGE':'NO_CREDIT'}, status = 401)

            if Credit.objects.get(user_id = request.user.id).credit - class_v.price < 0:
                return JsonResponse({'MESSAGE':'NOT_ENOUGH_CREDIT'}, status = 401)
            
            Credit.objects.update(
                credit = Credit.objects.get(user_id = request.user.id).credit - class_v.price
            )

            Booking.objects.create(
                user_id     = request.user.id,
                class_id_id = class_id
            )

            BookingLog.objects.create(
                user_id     = request.user.id,
                class_id_id = class_id,
                action      = "booked"
            )

            return JsonResponse({'MESSAGE': 'CLASS_BOOKED'}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
        except ObjectDoesNotExist:
            return JsonResponse({"message" : "NOT_EXIST"}, status=400)

    @login_decorator
    def delete(self, request, class_id):
        try:
            if not Booking.objects.filter(class_id_id = class_id).exists():
                return JsonResponse({'MESSAGE':'BOOKING_NOT_EXIST'}, status = 404)
            user    = User.objects.get(id=request.user.id)
            booking = Booking.objects.get(class_id_id = class_id)
            class_v = Class.objects.get(id= class_id)
            refund_credit = 0

            print("days left until class :", class_v.date - datetime.now().date())

            if (class_v.date - datetime.now().date()).days < 1 :
                return JsonResponse({'MESSAGE': 'DENIED'}, status = 200)
            elif (class_v.date - datetime.now().date()).days < 2 :
                refund_credit = class_v.price * 0.5
            else:
                refund_credit = class_v.price

            Credit.objects.filter(user_id=user.id).update(
                credit = Credit.objects.get(user_id=user.id).credit + Decimal(refund_credit)
            )

            booking.delete()

            BookingLog.objects.create(
                user_id     = request.user.id,
                class_id_id = class_id,
                action      = "canceled"
            )

            return JsonResponse({'MESSAGE': 'BOOKING_CANCELLED'}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
        except ObjectDoesNotExist:
            return JsonResponse({"message" : "NOT_EXIST"}, status=400)

class LogView(View):
    @login_decorator
    def get(self, request): 
        try:
            if not BookingLog.objects.filter(user_id = request.user.id).exists():
                return JsonResponse({'BOOKINGS': 'NOT_EXIST'}, status = 200)

            user    = User.objects.get(id=request.user.id)
            logs    = BookingLog.objects.filter(user_id=request.user.id)

            results = [{
                    "user"        : user.phone,
                    "date"        : log.created_at,
                    "class"       : Class.objects.get(id=log.class_id_id).name,
                    "action"      : log.action,
                    "price"       : Class.objects.get(id=log.class_id_id).price
                } for log in logs] 
            
            credit_left = Credit.objects.get(user_id=request.user.id).credit

            return JsonResponse({'logs': results, 'credit_left' : credit_left}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
        except ObjectDoesNotExist:
            return JsonResponse({"message" : "NOT_EXIST"}, status=400)

class BookListAdminView(View):
    @admin_only
    def get(self, request): 
        try:
            data  = json.loads(request.body)
            start = data['start']
            end   = data['end']

            bookings = Booking.objects.filter(created_at__range=[start,end])

            results = [{
                    "user"        : User.objects.get(id=booking.user_id).phone,
                    "date"        : booking.created_at.date(),
                    "class"       : Class.objects.get(id=booking.class_id_id).name,
                    "price"       : Class.objects.get(id=booking.class_id_id).price
                } for booking in bookings.order_by('-created_at')]
            
            credits_paid = 0
            for booking in bookings:
                credits_paid = credits_paid + Class.objects.get(id=booking.class_id_id).price

            return JsonResponse({'bookings': results, 'credits_paid': credits_paid}, status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)
        except ObjectDoesNotExist:
            return JsonResponse({"message" : "NOT_EXIST"}, status=400)