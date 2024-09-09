from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser,FileUploadParser
from .models import DeactivationModels
from .serializers import DeactivateSerializers,DeactivatepostSerializers
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta,datetime
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
import logging
import pandas as pd
from Dealer.models import Dealersmodel

logger = logging.getLogger(__name__)


class Paginations(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100

class GetDeactiveviewset(generics.ListAPIView):
    queryset = DeactivationModels.objects.all().order_by('MILLER_NAME')
    serializer_class = DeactivateSerializers
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    search_fields = ['MILLER_TRANSPORTER_ID']
    lookup_field = 'MILLER_TRANSPORTER_ID'
    pagination_class = Paginations

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = DeactivationModels.objects.all().order_by('-id')
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%d-%m-%Y').date()
                end_date = datetime.strptime(end_date, '%d-%m-%Y').date()
                queryset = queryset.filter(DeactivationDate__range=(start_date, end_date))
            except ValueError as e:
                logger.error(f"Date parsing error: {e}")
                pass  # Handle the error as needed

        return queryset

    def get(self, request, *args, **kwargs):
        MILLER_TRANSPORTER_ID = kwargs.get('MILLER_TRANSPORTER_ID', None)
        if MILLER_TRANSPORTER_ID:
            # Use filter instead of get
            miller_instances = DeactivationModels.objects.filter(MILLER_TRANSPORTER_ID=MILLER_TRANSPORTER_ID)
            if miller_instances.exists():
                serializer = self.get_serializer(miller_instances, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Miller not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fallback to the default queryset if MILLER_TRANSPORTER_ID is not provided
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class postDeactivateviewset(generics.CreateAPIView):
    queryset = DeactivationModels.objects.all()
    serializer_class = DeactivatepostSerializers
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, *args, **kwargs):
        serializer = DeactivatepostSerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteDeactivateviewsets(generics.DestroyAPIView):
    queryset = DeactivationModels.objects.all().order_by('id')
    serializer_class = DeactivateSerializers
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
                instance = DeactivationModels.objects.get(id=id)
                instance.delete()
                return Response({'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
            except DeactivationModels.DoesNotExist:
                return Response({'error': 'Record does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

class updateDeactivateviewsets(generics.UpdateAPIView):
    queryset = DeactivationModels.objects.all().order_by('MILLER_NAME')
    serializer_class = DeactivateSerializers
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser,JSONParser,FileUploadParser]
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

class UpdatedeactivateLetterHeadViewSets(generics.UpdateAPIView):
    queryset = DeactivationModels.objects.all().order_by('MILLER_NAME')
    serializer_class = DeactivateSerializers
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser, FileUploadParser]
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        id = kwargs.get(self.lookup_field)
        if not id:
            return Response({'error': 'Transporter ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        deactivations = DeactivationModels.objects.filter(id=id)
        if not deactivations.exists():
            return Response({'error': 'Deactivation not found'}, status=status.HTTP_404_NOT_FOUND)

        if deactivations.count() > 1:
            # Update all installations with the same MILLER_TRANSPORTER_ID
            for deactivation in deactivations:
                serializer = self.get_serializer(deactivation, data=request.data, partial=True)
                if serializer.is_valid():  # Call is_valid() first
                    if 'Deactivation_letterHead' in request.data:
                        serializer.validated_data['Deactivation_letterHead'] = request.data['Deactivation_letterHead']
                        try:
                            serializer.save()
                        except Exception as e:
                            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'message': 'All deactivation with MILLER_TRANSPORTER_ID updated successfully'}, status=status.HTTP_200_OK)
        deactivation = deactivations.first()
        # Only update the Installation_letterHead field
        serializer = self.get_serializer(deactivation, data=request.data, partial=True)
        if serializer.is_valid():  # Call is_valid() first
            if 'Deactivation_letterHead' in request.data:
                serializer.validated_data['Deactivation_letterHead'] = request.data['Deactivation_letterHead']
                try:
                    serializer.save()
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_file_url(request, id):
    installer = get_object_or_404(DeactivationModels, id=id)
    if installer.Deactivation_letterHead:
        file = installer.Deactivation_letterHead
        response = HttpResponse(file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.name}"'
        return response
    else:
        return JsonResponse({'error': 'File not found'}, status=404)


class DeactivationcountView(generics.ListAPIView):
    permission_classes=[AllowAny]

    def get(self,request, *args, **kwargs):
        count=DeactivationModels.objects.count()
        return Response({'count':count},status=status.HTTP_200_OK)


class NewDeactivateCountView(generics.ListAPIView):
    permission_classes=[AllowAny]

    def get(self,request,*args, **kwargs):
        new_count = DeactivationModels.objects.filter(NewRenewal__iexact='New').count()
        return Response({'count':new_count},status=status.HTTP_200_OK)
    
class RenewalDeactivationCountView(generics.ListAPIView):
    permission_classes=[AllowAny]

    def get(self,request,*args,**kwargs):
        renewal_count = DeactivationModels.objects.filter(NewRenewal__iexact='Renewal').count()
        return Response({'count':renewal_count},status=status.HTTP_200_OK)
    

class TodaydeactivateCountview(generics.ListAPIView):
    permission_classes=[AllowAny]

    def get(self,request,*args,**kwargs):
        today=timezone.now().date()
        tomorrow = today + timedelta(days=1)
        new_count = DeactivationModels.objects.filter(
            DeactivationDate__gte=today, 
            DeactivationDate__lt=tomorrow
            ).count()
                     
        return Response({'count':new_count},status=status.HTTP_200_OK)

class TodayNewDeactivationCountView(generics.ListAPIView):
    permission_classes=[AllowAny]

    def get(self,request,*args,**kwargs):
        today=timezone.now().date()
        tomorrow=today + timedelta(days=1)
        new_count=(DeactivationModels.objects
                       .filter(DeactivationDate__gte=today,
                               DeactivationDate__lt=tomorrow,
                               NewRenewal__iexact='New')
                       .values('MILLER_TRANSPORTER_ID')
                       .distinct()
                       .count())
        return Response({'count':new_count},status=status.HTTP_200_OK)


class TodayRenewalDeactivationCountView(generics.ListAPIView):
    permission_classes=[AllowAny]

    def get(self,request,*args,**kwargs):
        today=timezone.now().date()
        tomorrow=today + timedelta(days=1)

        renewal_count=DeactivationModels.objects.filter(
            DeactivationDate__gte=today,
            DeactivationDate__lt=tomorrow,
            NewRenewal__iexact='Renewal').count()
        return Response({'count':renewal_count},status=status.HTTP_200_OK)

class YesterdayDeactivateCountViews(generics.ListAPIView):
    permission_classes=[AllowAny]

    def get(self,request,*args,**kwargs):
        today=timezone.now().date()
        yesterday= today - timedelta(days=1)
        yesterday_count=DeactivationModels.objects.filter(DeactivationDate=yesterday).count()
        return Response({'count':yesterday_count},status=status.HTTP_200_OK)

class YesterdayNewDeactivationContViews(generics.ListAPIView):
    permission_classes=[AllowAny]

    def get(self,request,*args,**kwargs):
        today=timezone.now().date()
        yesterday=today - timedelta(days=1)

        new_count=DeactivationModels.objects.filter(
            DeactivationDate=yesterday,
            NewRenewal__iexact='New'
        ).count()
        return Response({'count':new_count},status=status.HTTP_200_OK)

class YesterdayRenewalDeactivationCountViews(generics.ListAPIView):
   permission_classes=[AllowAny]
   def get(self, request, *args, **kwargs):
            today=timezone.now().date()
            yesterday=today - timedelta(days=1)

            renewal_count=DeactivationModels.objects.filter(
                DeactivationDate=yesterday,
                NewRenewal__iexact='Renewal').count()
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
                'DeactivationDate','Employee_Name',
                  'Device_Fault','Fault_Reason','Replace_DeviceIMEI_NO','Remark1','Remark2','Remark3','Deactivation_letterHead']]

            # Validate DataFrame columns
            expected_columns = ['MILLER_TRANSPORTER_ID','MILLER_NAME','district','MillerContactNo','Dealer_Name','Entity_id','GPS_IMEI_NO',
                  'SIM_NO','Device_Name','NewRenewal','OTR','vehicle1','vehicle2','vehicle3',
                'DeactivationDate','Employee_Name','Device_Fault','Fault_Reason','Replace_DeviceIMEI_NO','Remark1','Remark2','Remark3','Deactivation_letterHead']
            if not all(col in df.columns for col in expected_columns):
                return Response({'error': f'Missing one or more required columns: {expected_columns}'}, status=status.HTTP_400_BAD_REQUEST)


            # Replace NaN values with empty string
            df = df.fillna('')

            # Prepare a list to collect the new entries
            entries = []

            # Iterate through the DataFrame and create model instances
            for _, row in df.iterrows():
                # Check if an entry with the same MILLER_TRANSPORTER_ID already exists
                if not DeactivationModels.objects.filter(MILLER_TRANSPORTER_ID=row['MILLER_TRANSPORTER_ID']).exists():
                    entry = DeactivationModels(
                        MILLER_TRANSPORTER_ID=row['MILLER_TRANSPORTER_ID'],
                        MILLER_NAME=row['MILLER_NAME'],
                        district=row['district'],
                        MillerContactNo=row['MillerContactNo'],
                        Dealer_Name = row['Dealer_Name'],
                        Entity_id = row['Entity_id'],
                        GPS_IMEI_NO= row['GPS_IMEI_NO'],
                        SIM_NO = row['SIM_NO'],
                        Device_Name=row['Device_Name'],
                        NewRenewal=row['NewRenewal'],
                        OTR = row['OTR'],
                        vehicle1=row['vehicle1'],
                        vehicle2=row['vehicle2'],
                        vehicle3=row['vehicle3'],
                        DeactivationDate = row['DeactivationDate'],
                        Employee_Name= row['Employee_Name'],
                        Device_Fault=row['Device_Fault'],
                        Fault_Reason=row['Fault_Reason'],
                        Replace_DeviceIMEI_NO=row['Replace_DeviceIMEI_NO'],
                        Remark1=row['Remark1'],
                        Remark2=row['Remark2'],
                        Remark3=row['Remark3'],
                        Deactivation_letterHead=row['Deactivation_letterHead'],
                    )
                    entries.append(entry)

            # Bulk create entries
            DeactivationModels.objects.bulk_create(entries)

            return Response({'message': 'File processed successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
