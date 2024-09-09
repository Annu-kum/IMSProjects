# from django.shortcuts import render
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework import filters
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated,AllowAny
# from .models import InstallatonModels
# from .serializers import InstallSerializers
# from rest_framework.parsers import MultiPartParser, FormParser,JSONParser

# # Create your views here.


# class GetInstallviewset(generics.ListAPIView):
#     queryset=InstallatonModels.objects.all().order_by('MILLER_NAME')
#     serializer_class=InstallSerializers
#     permission_classes=[AllowAny]
#     filter_backends=[filters.SearchFilter]
#     parser_classes=[MultiPartParser,FormParser,JSONParser]
#     search_fields=['MILLER_TRANSPORTER_ID']
#     lookup_field='MILLER_TRANSPORTER_ID'
#     def get(self, request, *args,**kwargs):  
#         MILLER_TRANSPORTER_ID=kwargs.get('MILLER_TRANSPORTER_ID',None)
#         # result = InstallatonModels.objects.get(id=id)  
#         if MILLER_TRANSPORTER_ID:
#             MILLERID = InstallatonModels.objects.get(MILLER_TRANSPORTER_ID=MILLER_TRANSPORTER_ID)  
#             serializers = InstallSerializers(MILLERID)  
#             return Response(serializers.data, status=200)  
  
#         result = InstallatonModels.objects.all()  
#         serializers = InstallSerializers(result, many=True)  
#         return Response(serializers.data, status=200)  
# class postInstallviewset(generics.CreateAPIView):
#    queryset = InstallatonModels.objects.all()
#    serializer_class = InstallSerializers
#    permission_classes=[AllowAny]
#    parser_classes = (MultiPartParser, FormParser)
   

#    def post(self, request, *args, **kwargs):
#         serializer = InstallSerializers(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






#     # queryset=InstallatonModels.objects.all().order_by('MILLER_NAME')
#     # serializer_class=InstallSerializers
#     # permission_classes=[AllowAny]
#     # parser_classes=[MultiPartParser,FormParser,JSONParser]
#     # filter_backends=[filters.SearchFilter]
#     # search_fields=['MILLER_NAME']


#     # def post(self, request):
#     #     # Ensure rows are received as a list of dictionaries
#     #     data = request.data.get('rows', [])
        
#     #     # Check if 'data' is a list
#     #     if not isinstance(data, list):
#     #         return Response({"error": "Invalid data format. 'rows' should be a list."}, status=status.HTTP_400_BAD_REQUEST)

#     #     file = request.FILES.get('File', None)
        
#     #     # Iterate over each dictionary in the data list
#     #     for row in data:
#     #         if isinstance(row, dict):
#     #             row['Installation_letterHead'] = file

#     #     serializer = InstallSerializers(data=data, many=True)
        
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class DeleteInstallviewsets(generics.DestroyAPIView):
#     queryset=InstallatonModels.objects.all().order_by('id')
#     serializer_class=InstallSerializers
#     permission_classes=[AllowAny]
#     parser_classes=[MultiPartParser,FormParser,JSONParser]
#     filter_backends=[filters.SearchFilter]
#     search_fields=['MILLER_NAME','MILLER_TRANSPORTER_ID']
#     lookup_field='id'
    
#     def destory(self,request,*args,**kwargs):
#         id=kwargs.get('id',None)
#         if id:
#          try:
#                 id = InstallatonModels.objects.get(id=id)
#                 id.delete()
#                 return Response({'message':'Name deleted successfully'},status=status.HTTP_200_OK)
#          except InstallatonModels.DoesNotExist:
#               return Response({'error':'Name does not exist'},status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({'error':'Name parameter is required'},status=status.HTTP_400_BAD_REQUEST) 
        
# class updateInstallviewsets(generics.UpdateAPIView):
#     queryset=InstallatonModels.objects.all().order_by('MILLER_NAME')
#     serializer_class=InstallSerializers
#     permission_classes=[AllowAny]
#     parser_classes = (MultiPartParser, FormParser)
#     filter_backends=[filters.SearchFilter]
#     search_fields=['MILLER_NAME']
#     lookup_field='id'











# from django.shortcuts import render
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework import filters
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# from .models import InstallatonModels
# from .serializers import InstallSerializers

# class GetInstallviewset(generics.ListAPIView):
#     queryset = InstallatonModels.objects.all().order_by('MILLER_NAME')
#     serializer_class = InstallSerializers
#     permission_classes = [AllowAny]
#     filter_backends = [filters.SearchFilter]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
#     search_fields = ['MILLER_TRANSPORTER_ID']
#     lookup_field = 'MILLER_TRANSPORTER_ID'

#     def get_serializer_context(self):
#         return {'request': self.request}

#     def get(self, request, *args, **kwargs):
#         MILLER_TRANSPORTER_ID = kwargs.get('MILLER_TRANSPORTER_ID', None)
#         if MILLER_TRANSPORTER_ID:
#             try:
#                 MILLERID = InstallatonModels.objects.get(MILLER_TRANSPORTER_ID=MILLER_TRANSPORTER_ID)
#                 serializer = InstallSerializers(MILLERID, context={'request': request})
#                 return Response(serializer.data, status=200)
#             except InstallatonModels.DoesNotExist:
#                 return Response({'error': 'Miller not found'}, status=status.HTTP_404_NOT_FOUND)

#         result = InstallatonModels.objects.all()
#         serializer = InstallSerializers(result, many=True, context={'request': request})
#         return Response(serializer.data, status=200)

# class postInstallviewset(generics.CreateAPIView):
#     queryset = InstallatonModels.objects.all()
#     serializer_class = InstallSerializers
#     permission_classes = [AllowAny]
#     parser_classes = [MultiPartParser, FormParser]

#     def get_serializer_context(self):
#         return {'request': self.request}

#     def post(self, request, *args, **kwargs):
#         serializer = InstallSerializers(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DeleteInstallviewsets(generics.DestroyAPIView):
#     queryset = InstallatonModels.objects.all().order_by('id')
#     serializer_class = InstallSerializers
#     permission_classes = [AllowAny]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['MILLER_NAME', 'MILLER_TRANSPORTER_ID']
#     lookup_field = 'id'

#     def get_serializer_context(self):
#         return {'request': self.request}

#     def destroy(self, request, *args, **kwargs):
#         id = kwargs.get('id', None)
#         if id:
#             try:
#                 instance = InstallatonModels.objects.get(id=id)
#                 instance.delete()
#                 return Response({'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
#             except InstallatonModels.DoesNotExist:
#                 return Response({'error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         return Response({'error': 'ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

# class updateInstallviewsets(generics.UpdateAPIView):
#     queryset = InstallatonModels.objects.all().order_by('MILLER_NAME')
#     serializer_class = InstallSerializers
#     permission_classes = [AllowAny]
#     parser_classes = [MultiPartParser, FormParser]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['MILLER_NAME']
#     lookup_field = 'id'

#     def get_serializer_context(self):
#         return {'request': self.request}





from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser,FileUploadParser
from .models import InstallatonModels
from .serializers import InstallSerializers,InstallpostSerializers
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from datetime import datetime,timedelta
from rest_framework.pagination import PageNumberPagination
import logging
import pandas as pd
from Dealer.models import Dealersmodel 


logger = logging.getLogger(__name__)

class Paginations(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100

class GetInstallviewset(generics.ListAPIView):
    queryset = InstallatonModels.objects.all().order_by('MILLER_NAME')
    serializer_class = InstallSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    search_fields = ['MILLER_TRANSPORTER_ID']
    lookup_field = 'MILLER_TRANSPORTER_ID'
    pagination_class = Paginations

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = InstallatonModels.objects.all().order_by('-id')
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%d-%m-%Y').date()
                end_date = datetime.strptime(end_date, '%d-%m-%Y').date()
                queryset = queryset.filter(InstallationDate__range=(start_date, end_date))
            except ValueError as e:
                logger.error(f"Date parsing error: {e}")
                pass  # Handle the error as needed

        return queryset

    def get(self, request, *args, **kwargs):
        MILLER_TRANSPORTER_ID = kwargs.get('MILLER_TRANSPORTER_ID', None)
        if MILLER_TRANSPORTER_ID:
            # Use filter instead of get
            miller_instances = InstallatonModels.objects.filter(MILLER_TRANSPORTER_ID=MILLER_TRANSPORTER_ID)
            if miller_instances.exists():
                serializer = self.get_serializer(miller_instances, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Miller not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fallback to the default queryset if MILLER_TRANSPORTER_ID is not provided
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class postInstallviewset(generics.CreateAPIView):
    queryset = InstallatonModels.objects.all()
    serializer_class = InstallpostSerializers
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, *args, **kwargs):
        serializer = InstallpostSerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteInstallviewsets(generics.DestroyAPIView):
    queryset = InstallatonModels.objects.all().order_by('id')
    serializer_class = InstallSerializers
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser,JSONParser ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['MILLER_NAME', 'MILLER_TRANSPORTER_ID']
    lookup_field = 'id'

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if id:
            try:
                instance = InstallatonModels.objects.get(id=id)
                instance.delete()
                return Response({'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
            except InstallatonModels.DoesNotExist:
                return Response({'error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

class updateInstallviewsets(generics.UpdateAPIView):
    queryset = InstallatonModels.objects.all().order_by('MILLER_NAME')
    serializer_class = InstallSerializers
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser, FileUploadParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['MILLER_NAME']
    lookup_field = 'id'

    def post_serializer_context(self):
        return {'request': self.request}

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, partial=True)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, partial=False)



class UpdateLetterHeadViewSets(generics.UpdateAPIView):
    queryset = InstallatonModels.objects.all().order_by('MILLER_NAME')
    serializer_class = InstallSerializers
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser, FileUploadParser]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        id = kwargs.get(self.lookup_field)
        if not id:
            return Response({'error': 'Transporter ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        installations = InstallatonModels.objects.filter(id=id)
        if not installations.exists():
            return Response({'error': 'Installation not found'}, status=status.HTTP_404_NOT_FOUND)

        if installations.count() > 1:
            # Update all installations with the same MILLER_TRANSPORTER_ID
            for installation in installations:
                serializer = self.get_serializer(installation, data=request.data, partial=True)
                if serializer.is_valid():  # Call is_valid() first
                    if 'Installation_letterHead' in request.data:
                        serializer.validated_data['Installation_letterHead'] = request.data['Installation_letterHead']
                        try:
                            serializer.save()
                        except Exception as e:
                            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'message': 'All installations with MILLER_TRANSPORTER_ID updated successfully'}, status=status.HTTP_200_OK)

        installation = installations.first()
        # Only update the Installation_letterHead field
        serializer = self.get_serializer(installation, data=request.data, partial=True)
        if serializer.is_valid():  # Call is_valid() first
            if 'Installation_letterHead' in request.data:
                serializer.validated_data['Installation_letterHead'] = request.data['Installation_letterHead']
                try:
                    serializer.save()
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_file_url(request, id):
    installer = get_object_or_404(InstallatonModels, id=id)
    if installer.Installation_letterHead:
        file = installer.Installation_letterHead
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.name}"'
        return response
    else:
        return JsonResponse({'error': 'File not found'}, status=404)

class InstallCountView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        count = InstallatonModels.objects.count()
        return Response({'count': count}, status=status.HTTP_200_OK)


class NewInstallCountView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        new_count = InstallatonModels.objects.filter(NewRenewal__iexact='New').count()
        return Response({'count': new_count}, status=status.HTTP_200_OK)
    
class RenewalInstallCountView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        new_count = InstallatonModels.objects.filter(NewRenewal__iexact='Renewal').count()
        return Response({'count': new_count}, status=status.HTTP_200_OK)

class TodayInstallCountView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        new_count = InstallatonModels.objects.filter(
                         InstallationDate__gte=today, 
                         InstallationDate__lt=tomorrow,
                         ).count()
        return Response({'count': new_count}, status=status.HTTP_200_OK)



class TodayNewInstallCountView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        new_count = InstallatonModels.objects.filter(
            InstallationDate__gte=today,
            InstallationDate__lt=tomorrow,
            NewRenewal__iexact='New'
        ).count()
        return Response({'count': new_count}, status=status.HTTP_200_OK)
    

class TodayRenewalInstallCountView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        new_count = InstallatonModels.objects.filter(
            InstallationDate__gte=today,
            InstallationDate__lt=tomorrow,
            NewRenewal__iexact='Renewal'
        ).count()
        return Response({'count': new_count}, status=status.HTTP_200_OK)

class YesterdayInstallCountView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        yesterday_count = InstallatonModels.objects.filter(InstallationDate=yesterday).count()
        return Response({'count': yesterday_count}, status=status.HTTP_200_OK)



class YesterdayNewInstallCountView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        new_count = InstallatonModels.objects.filter(
            InstallationDate=yesterday,
            NewRenewal__iexact='New'
        ).count()
        return Response({'count': new_count}, status=status.HTTP_200_OK)

class YesterdayRenewalInstallCountView(generics.ListAPIView):
    permission_classes=[AllowAny]

    def get(self, request, *args, **kwargs):

        today=timezone.now().date()
        yesterday = today - timedelta(days=1)
        renewal_count = InstallatonModels.objects.filter(
            InstallationDate=yesterday,
            NewRenewal__iexact='Renewal'
        ).count()
        return Response({'count':renewal_count},status=status.HTTP_200_OK)
    

class BulkImportView(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check the file extension
        if not (file.name.endswith('.xlsx') or file.name.endswith('.xls') or file.name.endswith('.csv')):
            return Response({'error': 'Unsupported file type. Please upload an Excel or CSV file.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Read the file into a DataFrame
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            # Filter only the relevant columns
            df = df[['MILLER_TRANSPORTER_ID','MILLER_NAME','district','MillerContactNo','Dealer_Name','Entity_id','GPS_IMEI_NO',
                  'SIM_NO','Device_Name','NewRenewal','OTR','vehicle1','vehicle2','vehicle3',
                'InstallationDate','Employee_Name',
                  'Device_Fault','Fault_Reason','Replace_DeviceIMEI_NO','Remark1','Remark2','Remark3','Installation_letterHead']]

            # Validate DataFrame columns
            expected_columns = ['MILLER_TRANSPORTER_ID','MILLER_NAME','district','MillerContactNo','Dealer_Name','Entity_id','GPS_IMEI_NO',
                  'SIM_NO','Device_Name','NewRenewal','OTR','vehicle1','vehicle2','vehicle3',
                'InstallationDate','Employee_Name','Device_Fault','Fault_Reason','Replace_DeviceIMEI_NO','Remark1','Remark2','Remark3','Installation_letterHead']
            if not all(col in df.columns for col in expected_columns):
                return Response({'error': f'Missing one or more required columns: {expected_columns}'}, status=status.HTTP_400_BAD_REQUEST)



            # Replace NaN  values with empty string
            df = df.fillna('')


            # Iterate through the DataFrame and create model instances
            entries = []
            for _, row in df.iterrows():
                  # Fetch the Dealersmodel instance
                try:
                    dealer_instance = Dealersmodel.objects.get(Dealer_Name=row['Dealer_Name'])
                except Dealersmodel.DoesNotExist:
                    return Response({'error': f"Dealer '{row['Dealer_Name']}' does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                entry = InstallatonModels(
                    MILLER_TRANSPORTER_ID=row['MILLER_TRANSPORTER_ID'],
                    MILLER_NAME=row['MILLER_NAME'],
                    district=row['district'],
                    MillerContactNo=row['MillerContactNo'],
                    Dealer_Name = dealer_instance,
                    Entity_id = row['Entity_id'],
                    GPS_IMEI_NO= row['GPS_IMEI_NO'],
                    SIM_NO = row['SIM_NO'],
                    Device_Name=row['Device_Name'],
                    NewRenewal=row['NewRenewal'],
                    OTR = row['OTR'],
                    vehicle1 = row['vehicle1'],
                    vehicle2=row['vehicle2'],
                    vehicle3=row['vehicle3'],
                    InstallationDate = row['InstallationDate'],
                    Employee_Name= row['Employee_Name'],
                    Device_Fault=row['Device_Fault'],
                    Fault_Reason=row['Fault_Reason'],
                    Replace_DeviceIMEI_NO=row['Replace_DeviceIMEI_NO'],
                    Remark1=row['Remark1'],
                    Remark2=row['Remark2'],
                    Remark3=row['Remark3'],
                    Installation_letterHead=row['Installation_letterHead'],
                )
                entries.append(entry)

            # Bulk create entries
            InstallatonModels.objects.bulk_create(entries)

            return Response({'message': 'File processed successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




