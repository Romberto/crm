from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from client.views import auth_decoration
from trade.models import TradeModel, TradeItemModel


class WorkPlaceView(View):
    @auth_decoration
    def get(self, request):
        trades = TradeModel.objects.filter(is_active=True).select_related('manager').select_related('trade_client').values('id',
                                                                                                           'manager__username',
                                                                                                           'client__name',
                                                                                                            'compare')

        data = {
            'trades': trades
        }
        return render(request, "work_place/work_place.html", data)


class AgreementView(View):

    @auth_decoration
    def get(self, request, id):
        items_trade = TradeItemModel.objects.filter(trade=id).select_related('_product').select_related(
            '_trade').annotate(full_price_i=F('count') * F('product__price')).annotate(
            full_weigth_i=F('count') * F('product__weigth_netto')).values('id', 'product__product_name', 'product__id',
                                                                          'product__price',
                                                                          'count', 'full_price_i', 'full_weigth_i',
                                                                          'trade__full_weight','trade__full_price')

        if items_trade:
            trade__full_weight = items_trade[0]['trade__full_weight']
            trade__full_price = items_trade[0]['trade__full_price']
        else:
            trade__full_weight = 0
            trade__full_price = 0

        data = {
            'trade__full_weight': trade__full_weight,
            'trade__full_price': trade__full_price,
            'items_trade': items_trade,
            'id':id
        }
        return render(request, 'work_place/work_agreement.html', data)

def ajax_stamp(request):
    id = request.GET.get('id')
    trade = TradeModel.objects.filter(id=id).values('compare').first()
    return JsonResponse(trade)

def ajax_agreement(request):
    id = request.POST.get('id')
    try:
        trade = TradeModel.objects.get(id=id)
        trade.compare = True
        trade.save()
        data = {
            'error': False
        }
    except:
        data = {
            'error': True
        }

    return JsonResponse(data)