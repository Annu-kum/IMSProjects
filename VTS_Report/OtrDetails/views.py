from django.shortcuts import render
from Installation.models import InstallatonModels
from Deactivation.models import DeactivationModels
from Reactivation.models import ReactivationModels 
from rest_framework import generics
from rest_framework import status
from django.db.models import Sum
from datetime import date
from rest_framework.response import Response
from django.db.models import Count, Q
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from Dealer.models import Dealersmodel
from Dealer.serializers import DealerSerializers
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class Paginations(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100


class OtrDetailsviews(generics.ListAPIView):
  permission_classes=[AllowAny]


  def get(self, request,*args,**kwargs):     
    installation_count = InstallatonModels.objects.filter(~Q(OTR='')).count()
    deactivation_count = DeactivationModels.objects.filter(~Q(OTR='')).count()

    # Count non-empty OTR entries in ReactivationModels
    reactivation_count = ReactivationModels.objects.filter(~Q(OTR='')).count()
    # Sum up all counts
    total_count = installation_count + deactivation_count + reactivation_count
    return Response({'count':total_count},status=status.HTTP_200_OK)

class NewOTRCountView(generics.ListAPIView):
    permission_classes=[AllowAny]
    def get(self, request, *args,**kwargs):
        # Count Renewal entries with OTR in InstallationModels
        installation_new_count = InstallatonModels.objects.filter(
            Q(NewRenewal='New') & ~Q(OTR='')
        ).count()

        # Count Renewal entries with OTR in DeactivationModels
        deactivation_new_count = DeactivationModels.objects.filter(
            Q(NewRenewal='New') & ~Q(OTR='')
        ).count()

        # Count Renewal entries with OTR in ReactivationModels
        reactivation_new_count = ReactivationModels.objects.filter(
            Q(NewRenewal='New') & ~Q(OTR='')
        ).count()

        # Total count from all models
        total_new_count = installation_new_count + deactivation_new_count + reactivation_new_count
        return Response({'count':total_new_count},status=status.HTTP_200_OK)


class RenewalOTRCountView(generics.ListAPIView):
        permission_classes=[AllowAny]
        def get(self, request, *args,**kwargs):
            # Count Renewal entries with OTR in InstallationModels
            installation_renewal_count = InstallatonModels.objects.filter(
                Q(NewRenewal='Renewal') & ~Q(OTR='')
            ).count()

            # Count Renewal entries with OTR in DeactivationModels
            deactivation_renewal_count = DeactivationModels.objects.filter(
                Q(NewRenewal='Renewal') & ~Q(OTR='')
            ).count()

            # Count Renewal entries with OTR in ReactivationModels
            reactivation_renewal_count = ReactivationModels.objects.filter(
                Q(NewRenewal='Renewal') & ~Q(OTR='')
            ).count()

            # Total count from all models
            total_renewal_count = installation_renewal_count + deactivation_renewal_count + reactivation_renewal_count
            return Response({'count':total_renewal_count},status=status.HTTP_200_OK)


class TodayOTRCountView(generics.ListAPIView):
   permission_classes = [AllowAny]

   def get(self, request, *args, **kwargs):
        today = timezone.now().date()

        installation_otr_count = InstallatonModels.objects.filter(Q(InstallationDate=today)  & ~Q(OTR='')).count()
        deactivation_otr_count = DeactivationModels.objects.filter(Q(DeactivationDate=today) &  ~Q(OTR='')).count()
        reactivation_otr_count = ReactivationModels.objects.filter(Q(ReactivationDate=today) &  ~Q(OTR='')).count()

        today_otr_count = installation_otr_count + deactivation_otr_count + reactivation_otr_count
        return Response({'count':today_otr_count},status=status.HTTP_200_OK)

class TodayNewOTRCountView(generics.ListAPIView):
   permission_classes = [AllowAny]

   def get(self, request, *args, **kwargs):
        today = timezone.now().date()

        installation_otr_count = InstallatonModels.objects.filter(Q(InstallationDate=today) & Q(NewRenewal='New') & ~Q(OTR='')).count()
        deactivation_otr_count = DeactivationModels.objects.filter(Q(DeactivationDate=today) & Q(NewRenewal='New') & ~Q(OTR='')).count()
        reactivation_otr_count = ReactivationModels.objects.filter(Q(ReactivationDate=today) & Q(NewRenewal='New') & ~Q(OTR='')).count()

        today_otr_count = installation_otr_count + deactivation_otr_count + reactivation_otr_count
        return Response({'count':today_otr_count},status=status.HTTP_200_OK)
class TodayRenewalOTRCountView(generics.ListAPIView):
    permission_classes=[AllowAny]
    def get(self,request, *args, **kwargs):
        today = timezone.now().date()

        installation_otr_count = InstallatonModels.objects.filter(Q(InstallationDate=today) & Q(NewRenewal='Renewal') & ~Q(OTR='')).count()
        deactivation_otr_count = DeactivationModels.objects.filter(Q(DeactivationDate=today) & Q(NewRenewal='Renewal') & ~Q(OTR='')).count()
        reactivation_otr_count = ReactivationModels.objects.filter(Q(ReactivationDate=today) & Q(NewRenewal='Renewal') & ~Q(OTR='')).count()

        today_otr_count = installation_otr_count + deactivation_otr_count + reactivation_otr_count
        return Response({'count':today_otr_count},status=status.HTTP_200_OK)
    

class YesterdayOTRCountView(generics.ListAPIView):
    permission_classes=[AllowAny]
    def get(self,request, *args, **kwargs):
        current_date = date.today()
        yesterday= current_date - timedelta(days=1)

        installation_otr_count = InstallatonModels.objects.filter(Q(InstallationDate=yesterday) &  ~Q(OTR='')).count()
        deactivation_otr_count = DeactivationModels.objects.filter(Q(DeactivationDate=yesterday) & ~Q(OTR='')).count()
        reactivation_otr_count = ReactivationModels.objects.filter(Q(ReactivationDate=yesterday) & ~Q(OTR='')).count()

        today_otr_count = installation_otr_count + deactivation_otr_count + reactivation_otr_count
        return Response({'count':today_otr_count},status=status.HTTP_200_OK)





class YesterdayNewOTRCountView(generics.ListAPIView):
   permission_classes = [AllowAny]

   def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        yesterday= today - timedelta(days=1)
        installation_otr_count = InstallatonModels.objects.filter(Q(InstallationDate=yesterday) & Q(NewRenewal='New') & ~Q(OTR='')).count()
        deactivation_otr_count = DeactivationModels.objects.filter(Q(DeactivationDate=yesterday) & Q(NewRenewal='New') & ~Q(OTR='')).count()
        reactivation_otr_count = ReactivationModels.objects.filter(Q(ReactivationDate=yesterday) & Q(NewRenewal='New') & ~Q(OTR='')).count()

        today_otr_count = installation_otr_count + deactivation_otr_count + reactivation_otr_count
        return Response({'count':today_otr_count},status=status.HTTP_200_OK)



class YesterdayRenewalOTRCountView(generics.ListAPIView):
    permission_classes=[AllowAny]
    def get(self,request, *args, **kwargs):
        today = timezone.now().date()
        yesterday= today - timedelta(days=1)
        installation_otr_count = InstallatonModels.objects.filter(Q(InstallationDate=yesterday) & Q(NewRenewal='Renewal') & ~Q(OTR='')).count()
        deactivation_otr_count = DeactivationModels.objects.filter(Q(DeactivationDate=yesterday) & Q(NewRenewal='Renewal') & ~Q(OTR='')).count()
        reactivation_otr_count = ReactivationModels.objects.filter(Q(ReactivationDate=yesterday) & Q(NewRenewal='Renewal') & ~Q(OTR='')).count()

        today_otr_count = installation_otr_count + deactivation_otr_count + reactivation_otr_count
        return Response({'count':today_otr_count},status=status.HTTP_200_OK)
    



class DealerReport(generics.ListAPIView):
    
    permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs):
       # Aggregating counts for Installations
        installation_counts = InstallatonModels.objects.values('Dealer_Name__Dealer_Name').annotate(
            total_installations=Count('id'),
            total_new_installations=Count('id', filter=Q(NewRenewal='New')),
            total_renewal_installations=Count('id',filter=Q(NewRenewal='Renewal')),
            total_otr_installations=Count('id',filter=Q(OTR='OTR')),
        )
        
        # Aggregating counts for Deactivations
        deactivation_counts = DeactivationModels.objects.values('Dealer_Name').annotate(
            total_deactivations=Count('id'),
            total_new_deactivations=Count('id', filter=Q(NewRenewal='New')),
            total_renewal_deactivations=Count('id',filter=Q(NewRenewal='Renewal')),
            total_otr_deactivations=Count('id',filter=Q(OTR='OTR'))
        )
        
        # Aggregating counts for Reactivations
        reactivation_counts = ReactivationModels.objects.values('Dealer_Name').annotate(
            total_reactivations=Count('id'),
            total_new_reactivations=Count('id', filter=Q(NewRenewal='New')),
            total_renewal_reactivations=Count('id',filter=Q(NewRenewal='Renewal')),
            total_otr_reactivations=Count('id',filter=Q(OTR='OTR'))
        )

       
        result = {}

       
        for item in installation_counts:
            dealer = item['Dealer_Name__Dealer_Name']
            if dealer not in result:
                result[dealer] = {
                    'total_count': item['total_installations'],# Initialize total_count
                    'total_new': item['total_new_installations'],  # Initialize total_new
                    'total_renewal':item['total_renewal_installations'] ,#Initialize total_renewal
                    'total_otr' : item['total_otr_installations'],
                        
                }
            else:
               
                result[dealer]['total_count'] += item['total_installations']  # Update total_count
                result[dealer]['total_new'] += item['total_new_installations'] # Update total_n ew
                result[dealer]['total_renewal'] += item['total_renewal_installations']#Update total_renewal
                result[dealer]['total_otr'] += item['total_otr_installations']
        # Add deactivation counts to result
        for item in deactivation_counts:
            dealer = item['Dealer_Name']
            if dealer not in result:
                result[dealer] = {
                           
                    'total_count': item['total_deactivations'],  # Initialize total_count
                    'total_new': item['total_new_deactivations'],  # Initialize total_new
                    'total_renewal' : item['total_renewal_deactivations'],
                    'total_otr' : item['total_otr_deactivations']
                }
            else:
                result[dealer]['total_count'] += item['total_deactivations']  # Update total_count
                result[dealer]['total_new'] += item['total_new_deactivations']  # Update total_new
                result[dealer]['total_renewal'] += item['total_renewal_deactivations'] #Update total_renewal
                result[dealer]['total_otr'] += item['total_otr_deactivations']
        # Add reactivation counts to result
        for item in reactivation_counts:
            dealer = item['Dealer_Name']
            if dealer not in result:
                result[dealer] = {
                    
                    'total_count': item['total_reactivations'] , # Initialize total_count
                    'total_new': item['total_new_reactivations'],  # Initialize total_new
                    'total_renewal': item['total_renewal_reactivations'],
                    'total_otr' : item['total_otr_reactivations']
                }
            else:
                result[dealer]['total_count'] += item['total_reactivations']  # Update total_count
                result[dealer]['total_new'] += item['total_new_reactivations']  # Update total_new
                result[dealer]['total_renewal'] += item['total_renewal_reactivations'] #Update total_renewal
                result[dealer]['total_otr'] += item['total_otr_reactivations']
        return Response(result)

class GetSumofEnteries(generics.ListAPIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Aggregating counts for Installations
        installation_counts = InstallatonModels.objects.values('Dealer_Name__Dealer_Name').annotate(
            total_installations=Count('id'),
            total_new_installations=Count('id', filter=Q(NewRenewal='New')),
            total_renewal_installations=Count('id', filter=Q(NewRenewal='Renewal')),
            total_otr_installations=Count('id', filter=Q(OTR='OTR')),
        )

        
        deactivation_counts = DeactivationModels.objects.values('Dealer_Name').annotate(
            total_deactivations=Count('id'),
            total_new_deactivations=Count('id', filter=Q(NewRenewal='New')),
            total_renewal_deactivations=Count('id', filter=Q(NewRenewal='Renewal')),
            total_otr_deactivations=Count('id', filter=Q(OTR='OTR'))
        )

       
        reactivation_counts = ReactivationModels.objects.values('Dealer_Name').annotate(
            total_reactivations=Count('id'),
            total_new_reactivations=Count('id', filter=Q(NewRenewal='New')),
            total_renewal_reactivations=Count('id', filter=Q(NewRenewal='Renewal')),
            total_otr_reactivations=Count('id', filter=Q(OTR='OTR'))
        )

       
        result = {}
        overall_totals = {
            'total_count': 0,
            'total_new': 0,
            'total_renewal': 0,
            'total_otr': 0
        }

        # Add installation counts to result
        for item in installation_counts:
            dealer = item['Dealer_Name__Dealer_Name']
            if dealer not in result:
                result[dealer] = {
                    'total_count': item['total_installations'],
                    'total_new': item['total_new_installations'],
                    'total_renewal': item['total_renewal_installations'],
                    'total_otr': item['total_otr_installations'],
                }
            else:
                result[dealer]['total_count'] += item['total_installations']
                result[dealer]['total_new'] += item['total_new_installations']
                result[dealer]['total_renewal'] += item['total_renewal_installations']
                result[dealer]['total_otr'] += item['total_otr_installations']
            
            overall_totals['total_count'] += item['total_installations']
            overall_totals['total_new'] += item['total_new_installations']
            overall_totals['total_renewal'] += item['total_renewal_installations']
            overall_totals['total_otr'] += item['total_otr_installations']

        # Add deactivation counts to result
        for item in deactivation_counts:
            dealer = item['Dealer_Name']
            if dealer not in result:
                result[dealer] = {
                    'total_count': item['total_deactivations'],
                    'total_new': item['total_new_deactivations'],
                    'total_renewal': item['total_renewal_deactivations'],
                    'total_otr': item['total_otr_deactivations']
                }
            else:
                result[dealer]['total_count'] += item['total_deactivations']
                result[dealer]['total_new'] += item['total_new_deactivations']
                result[dealer]['total_renewal'] += item['total_renewal_deactivations']
                result[dealer]['total_otr'] += item['total_otr_deactivations']
            
            overall_totals['total_count'] += item['total_deactivations']
            overall_totals['total_new'] += item['total_new_deactivations']
            overall_totals['total_renewal'] += item['total_renewal_deactivations']
            overall_totals['total_otr'] += item['total_otr_deactivations']

        # Add reactivation counts to result
        for item in reactivation_counts:
            dealer = item['Dealer_Name']
            if dealer not in result:
                result[dealer] = {
                    'total_count': item['total_reactivations'],
                    'total_new': item['total_new_reactivations'],
                    'total_renewal': item['total_renewal_reactivations'],
                    'total_otr': item['total_otr_reactivations']
                }
            else:
                result[dealer]['total_count'] += item['total_reactivations']
                result[dealer]['total_new'] += item['total_new_reactivations']
                result[dealer]['total_renewal'] += item['total_renewal_reactivations']
                result[dealer]['total_otr'] += item['total_otr_reactivations']
            
            overall_totals['total_count'] += item['total_reactivations']
            overall_totals['total_new'] += item['total_new_reactivations']
            overall_totals['total_renewal'] += item['total_renewal_reactivations']
            overall_totals['total_otr'] += item['total_otr_reactivations']

        # Include overall totals in the result
        result['overall_totals'] = overall_totals

        return Response(result)



class FetchDealerData(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    pagination_class = Paginations
    def get(self, request, dealer_name, *args, **kwargs):
        installation_data = InstallatonModels.objects.filter(Dealer_Name__Dealer_Name=dealer_name)
        deactivation_data = DeactivationModels.objects.filter(Dealer_Name=dealer_name)
        reactivation_data = ReactivationModels.objects.filter(Dealer_Name=dealer_name)

        context = {
            'dealer_name': dealer_name,
            'installation_data': installation_data.values(),
            'deactivation_data': deactivation_data.values(),
            'reactivation_data': reactivation_data.values(),
        }

        return Response(context)