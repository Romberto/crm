import decimal
import datetime

from django.db.models import F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from client.models import ClientModel
from client.views import auth_decoration
from product.models import ProductModel, GroupProductModel
from trade.forms import TradeForm, TradeItemForm, TradeAgentForm
from trade.models import TradeModel, TradeItemModel, TradeAgentItem, TradeAgent
from decimal import Decimal


class TradeAllView(View):
    @auth_decoration
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
            client = form_trade.cleaned_data['client']
            if client.agreement:
                stage_name = '2'
            else:
                stage_name = '1'
            specification = form_trade.cleaned_data['specification']
            trade = TradeModel.objects.create(
                stage_name=stage_name,
                manager=request.user,
                client=client,
                specification=specification
            )
            return redirect('trade_detail', trade.id)
        else:
            data = {
                'form_trade': form_trade
            }
            return render(request, 'trade/trade_add.html', data)


class TradeDetailView(View):
    @auth_decoration
    def get(self, request, id):
        form = TradeItemForm()
        query_trade = TradeItemModel.objects.filter(trade=id).select_related('_product').select_related(
            '_trade').annotate(full_weigth_i=F('count') * F('product__weigth_netto'),
                               full_price_i=F('count') * (F('product__price')+F('trade__logistic')),
                               logistic_full=F('count') * F('trade__logistic'),
                               logistic_price=F('product__price') + F('trade__logistic')).values('id', 'product__id',
                                                                                                 'product__product_group_id',
                                                                                                 'product__packing',
                                                                                                 'product__packing__packing_name',
                                                                                                 'product__price',
                                                                                                 'product__product_name',
                                                                                                 'count',
                                                                                                 'full_price_i',
                                                                                                 'full_weigth_i',
                                                                                                 'trade__id',
                                                                                                 'trade__client__id',
                                                                                                 'trade__compare',
                                                                                                 'trade__full_price',
                                                                                                 'trade__full_weight',
                                                                                                 'trade__client__name',
                                                                                                 'trade__client__face_contact',
                                                                                                 'trade__client__phone',
                                                                                                 'trade__client__phone2',
                                                                                                 'trade__client__phone3',
                                                                                                 'trade__client__mail',
                                                                                                 'trade__client__fact_address',
                                                                                                 'trade__client__jurist_address',
                                                                                                 'trade__client__site',
                                                                                                 'trade__client__agreement',
                                                                                                 'trade__client__activity',
                                                                                                 'trade__logistic',
                                                                                                 'logistic_full',
                                                                                                 'logistic_price',
                                                                                                 ).order_by(
            'id')
        try:
            # поставщик id
            supplier_id = TradeAgent.objects.filter(trade=int(query_trade[0]['trade__id'])).first()
        except Exception as er:
            supplier_id = None
        if supplier_id:
            query_supplier = TradeAgentItem.objects.filter(trade_agent=supplier_id).select_related('product', 'trade_agent').annotate(supplier_full_price=F('count')*F('price'),
                                                                                                                       supplier_full_weight=F('count')*F('product__weigth_netto')).values(
                'count', 'date_delivery', 'price', 'product__product_name', 'supplier_full_price', 'supplier_full_weight', 'id', 'trade_agent__full_price', 'trade_agent__full_weight'
            ).order_by('id')
            supplier_full_price = query_supplier[0]['trade_agent__full_price']
            supplier_full_weight = query_supplier[0]['trade_agent__full_weight']

        else:
            query_supplier = None
            supplier_full_price = None
            supplier_full_weight = None
        if query_trade:
            warning_list = []
            # предупреждение что грузовая спецификация не созданна
            for product in query_trade:
                if not product['product__packing']:
                    warning_list.append({'product__product_name': product['product__product_name'],
                                         'group_product_id': product['product__product_group_id'],
                                         'product__id': product['product__id']})

            data = {
                'supplier': supplier_id,
                'supplier_full_weight':supplier_full_weight,
                'supplier_full_price':supplier_full_price,
                'query_supplier': query_supplier,
                'logistic_full': query_trade[0]['logistic_full'],
                'query_trade': query_trade,
                'trade__logistic': query_trade[0]['trade__logistic'],
                'trade__full_price': (query_trade[0]['trade__full_price']+query_trade[0]['logistic_full']),
                'trade__full_weight': query_trade[0]['trade__full_weight'],
                'form': form,
                'warning_list': warning_list,
                'trade__compare': query_trade[0]['trade__compare'],
                'trade__client__id': query_trade[0]['trade__client__id'],
                'trade_client': query_trade[0]['trade__client__name'],
                'trade__client__face_contact': query_trade[0]['trade__client__face_contact'],
                'trade__client__phone': query_trade[0]['trade__client__phone'],
                'trade__client__phone2': query_trade[0]['trade__client__phone2'],
                'trade__client__phone3': query_trade[0]['trade__client__phone3'],
                'trade__client__mail': query_trade[0]['trade__client__mail'],
                'trade__client__fact_address': query_trade[0]['trade__client__fact_address'],
                'trade__client__jurist_address': query_trade[0]['trade__client__jurist_address'],
                'trade__client__site': query_trade[0]['trade__client__site'],
                'trade__client__agreement': query_trade[0]['trade__client__agreement'],
                'trade__client__activity': query_trade[0]['trade__client__activity'],
                'id': id,
                'product__packing': query_trade[0]['product__packing__packing_name']
            }
        else:
            data = {'query_trade': None, 'form': form}

        return render(request, 'trade/trade_detail.html', data)

    @auth_decoration
    def post(self, request, id):
        form = TradeItemForm(request.POST)
        trade = TradeModel.objects.get(id=id)
        if form.is_valid():
            product_list = TradeItemModel.objects.filter(trade=trade).select_related('_product').values_list(
                'product__product_name', flat=True)
            product = form.cleaned_data['product']
            if product.product_name in product_list:
                query_list = TradeItemModel.objects.filter(trade=trade)
                for elem in query_list:
                    if elem.product.product_name == product.product_name:
                        elem.count += form.cleaned_data['count']
                        elem.save()
                trade.compare = False
            else:
                trade_product_item = TradeItemModel.objects.create(
                    trade=trade,
                    product=form.cleaned_data['product'],
                    count=form.cleaned_data['count'],
                )
            trade.compare = False
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

        elif int(val) < 0:
            data = {
                'ValueError': 'ошибка даных'
            }

        else:
            try:
                trade_item.count = int(val)
            except ValueError:
                data = {
                    'ValueError': 'ошибка даных'
                }
                return JsonResponse(data)
            trade_item.save()
            total_price_item = trade_item.total()
            total_weight_item = trade_item.total_weight()
            trade_model = TradeModel.objects.get(id=trade_item.trade.id)
            trade_model.compare = False
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


def ajax_text(request):
    msg = ''
    if request.user.is_authenticated:
        upac_key = {
            'AJ': 'коробок',
            'K': 'канистр',
            'P': 'вёдер',
            'T': 'тонн'
        }
        id_trade = request.GET.get('id')
        trade_items = TradeItemModel.objects.filter(trade=id_trade).select_related('_product').select_related(
            '_trade').values('count', 'product__weigth_netto',
                             'product__packing__quantity_element_in',
                             'product__packing__quantity_box',
                             'product__packing__packing_name',
                             'product__price',
                             'product__product_name',
                             'trade__full_weight', 'trade__full_price', 'trade__logistic')
        for elem in trade_items:
            D = decimal.Decimal
            tara = "коробок"
            tara_elem = "бутылок"

            if elem['product__packing__quantity_element_in'] == 1:
                if elem['product__packing__packing_name'] == 'K':
                    tara = 'канистр'
                    tara_elem = 'канистр'
                elif elem['product__packing__packing_name'] == 'P':
                    tara = 'вёдер'
                    tara_elem = 'вёдер'
                elif elem['product__packing__packing_name'] == 'AJ':
                    tara = 'коробок'
                    tara_elem = 'коробок'
                elif elem['product__packing__packing_name'] == 'T':
                    if len(trade_items) > 1:
                        msg = "В заявке смешиваютя сыпучие и тарированные товаты, если ошибки нет, сделайте две разные сделки "
                        return HttpResponse(msg)
                    else:
                        logistik = trade_items[0]['trade__logistic']
                        price = int(elem['product__price']) + logistik
                        other_price = int(elem['trade__full_weight']) * price / 1000
                        msg = f"<b>{elem['product__product_name']}</b> - {elem['trade__full_weight']/1000} тонн * {price} руб.= " \
                              f"{other_price} руб." \
                              f""
                        return HttpResponse(msg)

            quantity_box = D(int(elem['count']) / int(elem['product__packing__quantity_element_in'])).quantize(
                D("1.00"))
            quantity_pallet = D(quantity_box / int(elem['product__packing__quantity_box'])).quantize(D("1.0"),
                                                                                                     decimal.ROUND_CEILING)
            elem_netto = elem['count'] * elem['product__weigth_netto']
            full_price = D(int(elem['count']) * int(elem['product__price'])).quantize(D("1.00"), decimal.ROUND_CEILING)
            msg += f"<p>в кг. : <br><b>{elem['product__product_name']}</b> - " \
                   f"{str(quantity_pallet)} палет * {elem['product__packing__quantity_box']} {upac_key[elem['product__packing__packing_name']]} =" \
                   f" {quantity_box} {tara} * {elem['product__packing__quantity_element_in']} шт.= {elem['count']} {tara_elem}. * {elem['product__weigth_netto']} кг.= " \
                   f"<span class='popup_full_price'>{elem_netto}</span> кг. <br>в рублях: <br>{elem['count']} {tara_elem}. * {elem['product__price']} руб. = <span class='popup_full_price'>{full_price}</span> руб.</p>"

        full_weight = trade_items[0]['trade__full_weight']
        full_money = trade_items[0]['trade__full_price']

        msg += f"<p><b>Общий вес: </b>{full_weight} кг.</p><p><b>Общая сумма: </b>{full_money} руб.</p>"
        data = {
            msg
        }
        return HttpResponse(data)
    else:
        msg = '<p>пользователь не зарегистрирован</p>'
        data = {
            msg
        }
        return HttpResponse(data)


def ajax_message(request):
    msg = ''
    if request.user.is_authenticated:
        id_client = request.GET.get('id')
        client = ClientModel.objects.filter(id=id_client).values('phone', 'phone2', 'phone3')
        msg += f'<p>телефон: </p>'
        msg += f'<p><a href="https://wa.me/{client[0]["phone"]}" target="_blank">{client[0]["phone"]}</a></p>'
        if client[0]['phone2']:
            msg += f'<p><a href="https://wa.me/{client[0]["phone2"]}" target="_blank">{client[0]["phone2"]}</a></p>'
        if client[0]['phone3']:
            msg += f'<p><a href="https://wa.me/{client[0]["phone3"]}" target="_blank">{client[0]["phone3"]}</a></p>'

        data = {
            msg
        }

        return HttpResponse(data)
    else:
        msg = '<p>пользователь не зарегистрирован</p>'
        data = {
            msg
        }
        return HttpResponse(data)


def ajax_compare(request):
    if request.user.is_authenticated:
        id_trade = request.GET.get('id')
        obj = TradeModel.objects.filter(id=int(id_trade)).values('compare').first()
        data = {
            'compare': obj['compare']
        }

        return JsonResponse(data)


def ajax_logistic_valid(request):
    if request.user.is_authenticated:
        id_trade = request.GET.get('id')
        query = TradeItemModel.objects.filter(trade=id_trade).select_related('product').values('product__product_type')
        if len(query) > 1:
            if {'product__product_type': 'S'} in query:
                data = {
                    'error_valid_type': True
                }
            else:
                data = {
                    'tara': True
                }
        elif len(query) == 1 and {'product__product_type': 'S'} in query:
            data = {
                'loose': True
            }
        else:
            data = {
                'tara': True
            }

    else:
        data = {
            "error_auth": True
        }
    return JsonResponse(data)


def ajax_logistic_price(request):
    trade_id = request.POST.get('id')
    logistic_price = request.POST.get('logistic_price')
    try:
        trade = TradeModel.objects.get(id=trade_id)
        trade.logistic = Decimal(logistic_price)
        trade.save()

        data = {
            'success': True
        }
    except Exception as er:
        print(er)
        data = {
            'success': False,
            'error': 'ошибка trade.view.ajax_logistic_price'
        }
    return JsonResponse(data)

def ajax_get_agets(request):
    if request.user.is_authenticated:
        id_trade  = request.GET.get('id')
        agents = ClientModel.objects.filter(role='S').values('name')
        msg = '<h2 class="title_h2">выберите поставщика</h2>'
        msg += '<div class="agent_form_block">'
        msg += '<p><select name="agents" id="agents">'
        for item in agents:
            msg += f'<option>{item["name"]}</option>'
        msg += '</select></p>'
        msg += f'<a href="#" data-value="{id_trade}" class="btn_add_group" id="agent_btn">выбрать</a>'
        msg +='</div>'

    else:
        msg = '<p> пользователь не зарегистрирован</p>'
    return HttpResponse(msg)

def ajax_get_agent_form(request):
    if request.user.is_authenticated:
        id_trade = request.POST.get('id')
        name = request.POST.get('agent')
        csrf = request.POST.get('csrf')
        group = GroupProductModel.objects.filter(group_title=name).values('id').first()
        products = ProductModel.objects.filter(product_group=group['id']).values('product_name', 'id')
        if not products:
            msg = "Продуктов этого постовщика нет в базе"
        else:

            msg = f'<h2 class="title_h2">заявка поставщику {name}</h2>'
            msg += '<form method="post" action="#" class="trade_agent_form"'
            msg += '<p><label for="id_products">продукт:</label>'
            msg += '<select name="products" id="id_product" required>'
            for item in products:
                msg += f'<option>{item["product_name"]}</option>'
            msg += '</select></p>'
            msg += '<p><label for="id_count_product">кол-во:</label>'
            msg += '<input type="number" id="id_count_product" name="count_product" required></input></p>'
            msg += '<p><label for="id_price">цена:</label>'
            msg += '<input type="number" id="id_price" name="price" required></input></p>'
            msg += '<p><label for="id_date">дата поставки:</label>'
            msg += '<input type="date" id="id_date" name="date" required></input></p>'
            msg += f'<input type="hidden" id="id_trade_agent" name="trade" value="{id_trade}"></input>'
            msg += f'<input type="submit" value="создать" class="form__btn_action"></input>'
            msg += '</form>'


    else:
        msg = '<p> пользователь не зарегистрирован</p>'
    return HttpResponse(msg)

def ajax_post_agent_form(request):
    if request.user.is_authenticated:
        date = request.POST.get('date')
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d' ).date()
        date_today = datetime.datetime.today().date()
        if date_time_obj < date_today:
            data={
                'error_auth': False,
                'data_no_valid': True
            }
        else:

            #todo бизнес логика
            trade = request.POST.get('trade')
            price = request.POST.get('price')
            product = request.POST.get('products')
            count = request.POST.get('count_product')
            query_product = ProductModel.objects.get(product_name=product)
            trade = TradeModel.objects.get(id=int(trade))
            agent = TradeAgent.objects.filter(trade=trade).first()
            if agent:
                trade_agent = agent
            else:
                trade_agent = TradeAgent(
                    trade=trade
                )
                trade_agent.save()


            TradeAgentItem.objects.create(
                trade_agent=trade_agent,
                product=query_product,
                count=int(count),
                date_delivery=date_time_obj,
                price=float(price)
            )
            trade_agent.save(update_fields=['full_price', 'full_weight'])
            data = {
                'error_auth': False
            }
    else:
        data = {
            'error_auth': True
        }
    return JsonResponse(data)

def ajax_supplier_price(request):
    if request.user.is_authenticated:
        id = request.POST.get('id')
        item = TradeAgentItem.objects.get(id=id)
        price = request.POST.get('price')
        item.price = float(price)
        item_full_price = float(price) * item.count # стоимисть товара в позиции
        item.save(update_fields=['price'])
        a_item = TradeAgent.objects.get(id=item.trade_agent.id)
        a_item.save(update_fields=['full_price'])
        data = {
            'item_full_price': item_full_price,
            'full_price': a_item.full_price,

        }
    else:
        data={
            'no_auth': True
        }
    return JsonResponse(data)

def ajax_supplier_count(request):
    if request.user.is_authenticated:
        id = request.POST.get('id')
        item = TradeAgentItem.objects.get(id=id)
        count = request.POST.get('count')
        if int(count) > 0:
            item.count = count
            item_full_price = int(count) * item.price
            item_fill_weight = int(count) * item.product.weigth_netto
            item.save(update_fields=['count'])
            a_item = TradeAgent.objects.get(id=item.trade_agent.id)
            a_item.save()

            data = {
                'item_full_price':item_full_price,
                'item_fill_weight': item_fill_weight,
                'full_price': a_item.full_price,
                'full_weight':a_item.full_weight
            }
        else:
            item.delete()
            data = {
                'remove': True
            }
    else:
        data = {
            'no_auth': True
        }
    return JsonResponse(data)

def ajax_supplier_date(request):
    if request.user.is_authenticated:
        id = request.POST.get('id')
        date = request.POST.get('date')
        item = TradeAgentItem.objects.get(id=id)
        date_format = datetime.datetime.strptime(date, '%Y-%m-%d').date()


        try:
            item.date_delivery = date
            item.save()
        except Exception as er:
            print(er)
        data = {
            'date_delivery': date_format.strftime('%d %B %Y г.')
        }
    else:
        data = {
            'no_auth': True
        }
    return JsonResponse(data)