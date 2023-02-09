from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from client.views import auth_decoration
from trade.forms import TradeForm, TradeItemForm
from trade.models import TradeModel, TradeItemModel


class TradeAllView(View):
    def get(self, request):
        if request.user.profile.position == "DR":
            trades = TradeModel.objects.all().select_related('trade_client').select_related('manager').values('id',
                                                                                                              'create_date',
                                                                                                              'is_active',
                                                                                                              'client__name',
                                                                                                              'full_price',
                                                                                                              'manager__username')
        else:
            trades = TradeModel.objects.filter(manager=request.user.id).select_related('trade_client').values('id',
                                                                                                              'create_date',
                                                                                                              'is_active',
                                                                                                              'client__name',
                                                                                                              'full_price')
            pass
        data = {
            'trades': trades
        }

        return render(request, 'trade/trades.html', data)


class TradeAddView(View):
    @auth_decoration
    def get(self, request):
        form_trade = TradeForm()
        data = {
            'form_trade': form_trade
        }
        return render(request, 'trade/trade_add.html', data)

    @auth_decoration
    def post(self, request):
        form_trade = TradeForm(request.POST, request.FILES)
        if form_trade.is_valid():
            stage_name = form_trade.cleaned_data['stage_name']
            client = form_trade.cleaned_data['client']
            specification = form_trade.cleaned_data['specification']
            trade = TradeModel.objects.create(
                stage_name=stage_name,
                manager=request.user,
                client=client,
                specification=specification
            )
            return redirect('trade_all')
        else:
            data = {
                'form_trade': form_trade
            }
            return render(request, 'trade/trade_add.html', data)


class TradeDetailView(View):

    def get(self, request, id):
        form = TradeItemForm()
        query_trade = TradeItemModel.objects.filter(trade=id).select_related('_product').select_related(
            '_trade').annotate(full_price_i=F('count') * F('product__price')).annotate(
            full_weigth_i=F('count') * F('product__weigth_netto')).values('id', 'product__product_name', 'count',
                                                                          'full_price_i', 'full_weigth_i',
                                                                          'trade__full_price', 'trade__full_weight')
        if query_trade:
            data = {
                'query_trade': query_trade,
                'trade__full_price': query_trade[0]['trade__full_price'],
                'trade__full_weight': query_trade[0]['trade__full_weight'],
                'form': form
            }
        else:
            data = {'query_trade': None, 'form': form}

        return render(request, 'trade/trade_detail.html', data)

    def post(self, request, id):
        form = TradeItemForm(request.POST)
        trade = TradeModel.objects.get(id=id)
        if form.is_valid():
            product_list = TradeItemModel.objects.filter(trade=id).select_related('_product').values_list(
                'product__product_name', flat=True)
            product = form.cleaned_data['product']
            if product.product_name in product_list:
                trade_item = TradeItemModel.objects.filter(product=product).first()
                trade_item.count += form.cleaned_data['count']
                trade_item.save()
                trade.save()

            else:
                trade_product_item = TradeItemModel.objects.create(
                    trade=trade,
                    product=form.cleaned_data['product'],
                    count=form.cleaned_data['count']
                )
                trade.save()
            return redirect('trade_detail', id)


def ajax_edit(request):
    if request.user.is_authenticated:
        id_item = request.POST.get('id')
        val = request.POST.get('val')
        trade_item = TradeItemModel.objects.get(id=id_item)
        if val == '0' or val is None:
            trade_item.delete()
            data = {
                'reload': True
            }

        else:
            try:
                trade_item.count = int(val)
            except ValueError:
                trade_item.delete()
                data = {
                    'reload': True
                }
                return JsonResponse(data)
            trade_item.save()
            total_price_item = trade_item.total()
            total_weight_item = trade_item.total_weight()
            trade_model = TradeModel.objects.get(id=trade_item.trade.id)
            trade_model.save()
            total_price = trade_model.get_full_price()
            total_weight = trade_model.get_full_weight()
            data = {
                'id_item': id_item,
                'total_price_item': total_price_item,
                'total_weight_item': total_weight_item,
                'total_price': total_price,
                'total_weight': total_weight
            }
        return JsonResponse(data)
