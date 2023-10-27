from django.shortcuts import render
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from alertlog.models import Filterlog, Roles
from alertlog.serializers import AllFilterLogSerializer, RoleSerializer, LogUpdateSerializer
from rest_framework import status
import mysql.connector
from datetime import datetime, timedelta, timezone, date
from django.db.models import Q
from django.db import connections
from django.db import connection


# Create your views here.
def  index(request):
    return HttpResponse("Welcome")

class AlertLogListApiView(ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.AllowAny ]
    http_method_names = ['get', 'put','post', 'patch', 'head', 'options', 'trace', 'delete',]

    queryset = Filterlog.objects.all().order_by('-timestamp')
    serializer_class = AllFilterLogSerializer

    def get_queryset(self):
        hostname = self.request.GET.get('hostname')
        severity = self.request.GET.get('severity')
        time1 = self.request.GET.get('time1')
        time2 = self.request.GET.get('time2')
        rolename = self.request.GET.get('rolename')
        is_know  = self.request.GET.get('is_know')


        filterlogs = self.queryset

        if severity:
            filterlogs = filterlogs.filter(severity__icontains=severity)
        if is_know:
            filterlogs = filterlogs.filter(is_know__icontains =is_know)
        if hostname:
            filterlogs = filterlogs.filter(Q(hostname__icontains=hostname))
        if rolename:
            filterlogs = filterlogs.filter(Q(role__icontains=rolename))
        if time1 and time2:
            filterlogs = filterlogs.filter(timestamp__range=(time1, time2))

        return filterlogs
 



    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # serializer = self.get_serializer(instance, data=request.data, partial=True)
        # serializer.is_valid(raise_exception=True)
            
        # 'is_known' sütununu güncelle
        is_known = request.data.get('is_know')
       

        # Diğer alanları güncelle
        # self.perform_update(serializer)

        # SQL sorgusunu çalıştır
        with connection.cursor() as cursor:
            sql_query = "UPDATE alertlog_filterlog SET is_know = %s WHERE id = %s"
            cursor.execute(sql_query, [is_known, instance.id])

        return Response({"message": "Records updated successfully."})

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
        
    #     # 'is_known' sütununu güncelle
    #     is_known = request.data.get('is_known')
    #     instance.is_known = is_known

    #     self.perform_update(serializer)
    #     return Response(serializer.data)


class RulesListApiView(ModelViewSet):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.AllowAny ]
    http_method_names = ['get', 'put','post', 'patch', 'head', 'options', 'trace', 'delete',]
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
    
    def perform_destroy(self, instance):
        instance.delete()



class TodoListApiView(APIView):
    #
    permission_classes = [permissions.AllowAny]
    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        #todos = Filterlog.objects.filter(user = request.user.id)
        todos = Filterlog.objects.all()
        serializer = AllFilterLogSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class CountLogs(APIView):
    def get(self, request):
        
        today = datetime.now().date()
        last_month = today - timedelta(days=30)
        last_week = today - timedelta(days=7)
        print(today)
        today1 = date.today()
        start_of_week = today1 - timedelta(days=today1.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        ################## today
        
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        data = self.request.GET.get('date')
        if date == 'month':
            alldata = Filterlog.objects.all().filter(Q(timestamp__gte=last_month) & Q(timestamp__lte=today))
            allcount = alldata.count()
            warning_count = alldata.filter(severity__icontains='warning').count()
            info_count = alldata.filter(severity__icontains='info').count()
            error_count = alldata.filter(severity__icontains='ERR').count()
            
            response_data = {
            'total' : allcount,
            'warning': warning_count,
            'info': info_count,
            'error': error_count,           
            }
            return Response(response_data)
            
        if date == 'week':
            print("week gecdi")
            alldata = Filterlog.objects.filter(timestamp__date__range=[start_of_week, end_of_week])
            #alldata = Filterlog.objects.all().filter(Q(timestamp__gte=last_week) & Q(timestamp__lte=today))
            allcount = alldata.count()
            warning_count = alldata.filter(severity__icontains='warning').count()
            info_count = alldata.filter(severity__icontains='info').count()
            error_count = alldata.filter(severity__icontains='ERR').count()
            
            response_data = {
            'total' : allcount,
            'warning': warning_count,
            'info': info_count,
            'error': error_count,           
            }
            return Response(response_data)
            
        
        if date == 'today':
            
            alldata = Filterlog.objects.filter(timestamp__range=(start_of_day, end_of_day))
            #alldata = Filterlog.objects.all().filter(Q(timestamp__date=today))
            allcount = alldata.count()
            warning_count = alldata.filter(severity__icontains='warning').count()
            info_count = alldata.filter(severity__icontains='info').count()
            error_count = alldata.filter(severity__icontains='ERR').count()
            print(alldata)
            response_data = {
            'total' : allcount,
            'warning': warning_count,
            'info': 3,
            'error': error_count,           
            }
            return Response(response_data)
        
            # queryset = YourModel.objects.filter(Q(created_at__gte=last_month) & Q(created_at__lte=today))
        allcount = Filterlog.objects.all().count()
        warning_count = Filterlog.objects.filter(severity__icontains='warning').count()
        info_count = Filterlog.objects.filter(severity__icontains='info').count()
        error_count = Filterlog.objects.filter(severity__icontains='ERR').count()
        response_data = {
            'total' : allcount,
            'warning': warning_count,
            'info': info_count,
            'error': error_count,           
        }
        return Response(response_data)

class FilterLogsViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = AllFilterLogSerializer
    
    queryset = Filterlog.objects.all().order_by('-timestamp')

    def get_queryset(self):
        hostname = self.request.GET.get('hostname')
        severity = self.request.GET.get('severity')
        time1 = self.request.GET.get('time1')
        time2 = self.request.GET.get('time2')
        rolename = self.request.GET.get('rolename')
        is_know  = self.request.GET.get('is_know')


        filterlogs = self.queryset

        if severity:
            filterlogs = filterlogs.filter(severity__icontains=severity)
        if is_know:
            filterlogs = filterlogs.filter(is_know__icontains =is_know)
        if hostname:
            filterlogs = filterlogs.filter(Q(hostname__icontains=hostname))
        if rolename:
            filterlogs = filterlogs.filter(Q(role__icontains=rolename))
        if time1 and time2:
            filterlogs = filterlogs.filter(timestamp__range=(time1, time2))

        return filterlogs


class ReporAPIVIEW(APIView):
    def get(self, request, *args , **kwargs):
            hostname = request.GET.get('hostname')
            severity = request.GET.get('severity')
            time1 = request.GET.get('time1')
            time2 = request.GET.get('time2')
            rolename  = request.GET.get('rolename')
            filterlogs = Filterlog.objects.all().order_by('-timestamp')
            if hostname:
                filterlogs = filterlogs.filter(Q(hostname__icontains=hostname)) 
            if severity :
                filterlogs = filterlogs.filter(severity__icontains = severity)
            if  time1 and time2 :
                print(time1, "ok  ",time2 )
                filterlogs = filterlogs.filter(timestamp__range=(time1, time2))

            serializer = AllFilterLogSerializer(filterlogs, many=True)
            return Response({
                "data":serializer.data,
               }
                ,
                status=status.HTTP_200_OK)
           # else:
            #    return Response({"message":"Sizin rugsadynyz yok"}, status=status.HTTP_404_NOT_FOUND)




class LogUpdateView(APIView):
    def put(self, request, format=None):
        serializer = LogUpdateSerializer(data=request.data)
        if serializer.is_valid():
            ids = request.data.get('id')
            print("my ids: ",ids)
            is_know = request.data.get('is_know')
            Filterlog.objects.filter(id__in=ids).update(is_know=is_know)
            return Response({"message": "Records updated successfully."})
        return Response(serializer.errors, status=400)

# class LogUpdateView(APIView):
#     def put(self, request, format=None):
#         serializer = LogUpdateSerializer(data=request.data)
#         if serializer.is_valid():
#             ids = request.data.get('id')
#             print("my ids: ",ids)
#             is_know = request.data.get('is_know')
            
#             connection = mysql.connector.connect(
#             host='192.168.9.25',
#             user='alert',
#             password='P@ssword1234560',
#             database='Alertsystem'
#             )

#         # Bağlantı üzerinden bir imleç oluşturma
#             cursor = connection.cursor()
            
            
#             id_list = ','.join(str(id) for id in ids)
#             sql_query = "UPDATE alertlog_filterlog SET is_know = %s WHERE id IN (%s)"
#             cursor.execute(sql_query, (is_know, id_list))
            
#         # Güncelleme sorgusunu çalıştırma
#             # sql_query = "UPDATE alertlog_filterlog SET is_know = " + is_know +" WHERE id = "+ ids +" "
#             # #sql_query = "UPDATE alertlog_filterlog SET is_know = " + str(is_know) + " WHERE id = " + str(ids) + " "
#             # cursor.execute(sql_query)

#             # Değişiklikleri kaydetme
#             connection.commit()

#             # Bağlantıyı ve imleci kapatma
#             cursor.close()
#             connection.close()
#         #    Filterlog.objects.filter(id__in=ids).update(is_know=is_know)
#             return Response({"message": "Records updated successfully."})
#         return Response(serializer.errors, status=400)


# class LogUpdateView(APIView):
#     def put(self, request, format=None):
#         serializer = LogUpdateSerializer(data=request.data)
#         if serializer.is_valid():
#             ids = request.data.getlist('id')
#             ids = [int(id) for id in ids]
#             #ids = request.data.get('id')
#             print("my ids: ",ids)
#             is_know = request.data.get('is_know')
            
#             connection = mysql.connector.connect(
#             host='192.168.9.25',
#             user='alert',
#             password='P@ssword1234560',
#             database='Alertsystem'
#             )

#         # Bağlantı üzerinden bir imleç oluşturma
#             cursor = connection.cursor()

            
#             id_list = ','.join(str(id) for id in ids)
#             sql_query = "UPDATE alertlog_filterlog SET is_know = %s WHERE id IN (%s)"
#             cursor.execute(sql_query, (is_know, id_list))
#         # # Güncelleme sorgusunu çalıştırma
#         #     sql_query = "UPDATE alertlog_filterlog SET is_know = " + is_know +" WHERE id = "+ ids +" "
#         #     cursor.execute(sql_query)

#             # Değişiklikleri kaydetme
#             connection.commit()

#             # Bağlantıyı ve imleci kapatma
#             cursor.close()
#             connection.close()
#         #    Filterlog.objects.filter(id__in=ids).update(is_know=is_know)
#             return Response({"message": "Records updated successfully."})
#         return Response(serializer.errors, status=400)

        
#             # Veritabanına bağlantı kurma
        
    
    
    
    



class ProcessDataView(APIView):
    def post(self, request):
        message = request.data.get('message')
        split_character = request.data.get('split_character')
        index_number = request.data.get('index_number')

#        if message is None or split_character is None or index_number is None:
#            return Response({'error': 'Invalid request data'}, status=400)

        data = message.split(split_character)
        if index_number < len(data):
            result = data[index_number]
            return Response({'result': result})
        else:
            return Response({'error': 'Invalid index number'}, status=400)
