
from decimal import Decimal

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from client.views import auth_decoration
from product.forms import ProductGroupForm, ProductForm, ProductPackingForm
from product.models import GroupProductModel, ProductModel, ProductPackagingModel

from django.core import serializers
from django.http import JsonResponse, HttpResponse


class ProductsView(View):
    @auth_decoration
    def get(self, request):
        groups = GroupProductModel.objects.all().order_by('id')
        form = ProductGroupForm()
        data = {
            'groups': groups,
            'form': form
        }
        return render(request, 'product/products.html', data)


class AddProductGroup(View):
    @auth_decoration
    def get(self, request):
        form = ProductGroupForm()
        data = {
            'form': form
        }
        return render(request, 'product/product_group_add.html', data)

    @auth_decoration
    def post(self, request):
        form = ProductGroupForm(request.POST)
        if form.is_valid():
            group_title = form.cleaned_data['group_title']
            form.group_title = group_title
            form.save()
            return redirect('products')
        else:
            data = {
                'form': form
            }
            return render(request, 'product/product_group_add.html', data)


class ProductListView(View):
    # показывает продукты определённой группы
    @auth_decoration
    def get(self, request, id):
        products = ProductModel.objects.filter(product_group_id=id).select_related('product_group').values('id',
                                                                                                           'article',
                                                                                                           'product_name',
                                                                                                           'price',
                                                                                                           'declaration',
                                                                                                           'protocol',
                                                                                                           'specification',
                                                                                                           'product_type',
                                                                                                           'quality_certificate',
                                                                                                           'product_group__group_title',
                                                                                                           'packing')
        if products:
            product_group_title = products[0]['product_group__group_title']

            data = {
                'products': products,
                'product_group_title': product_group_title,
                'product_groupe_id': id
            }
            return render(request, 'product/product_list.html', data)
        else:
            product_group_title = GroupProductModel.objects.filter(id=id).only('group_title')

            data = {
                'product_group_title': product_group_title[0],
                'product_groupe_id': id
            }
            return render(request, 'product/product_list.html', data)


class ProductItemView(View):

    @auth_decoration
    def get(self, request, id):
        product = \
            ProductModel.objects.filter(id=id).select_related('product_group').values('id', 'article', 'product_name',
                                                                                      'product_group', 'declaration',
                                                                                      'protocol', 'specification',
                                                                                      'quality_certificate',
                                                                                      'product_group',
                                                                                      'product_group__group_title')[0]
        data = {
            'product': product
        }
        return render(request, 'product/product_item.html', data)

    @auth_decoration
    def post(self, request, id):
        return render(request)


def delete_product_group(request):
    if request.user.is_authenticated and request.user.profile.position == 'DR':
        id = request.GET.get('id')
        try:
            group = GroupProductModel.objects.get(id=id)
            group.delete()
            data = {
                'error': False
            }

        except GroupProductModel.DoesNotExist:
            data = {
                'error': True,
                'msg': 'группа отсутсевует'
            }


    else:
        data = {
            'error': True,
            'msg': 'не зарегистрированный пользователь'
        }
    return JsonResponse(data)


def edit_product_group(request):
    if request.user.is_authenticated:
        id = request.GET.get('id')
        val = request.GET.get('val')
        name_list = GroupProductModel.objects.all().values_list('group_title', flat=True)
        if val in name_list:
            data = {
                'error': True,
                'msg': 'группа с таким названием уже есть'
            }
        elif len(val) == 0:
            data = {
                'error': True,
                'msg': 'пустые значения не допустимы'
            }
        elif request.user.profile.position != 'DR':
            data = {
                'error': True,
                'msg': 'менять название может только директор'
            }
        else:
            try:
                group = GroupProductModel.objects.get(id=id)
                group.group_title = val
                group.save()
                data = {
                    'error': False
                }
            except GroupProductModel.DoesNotExist:
                data = {
                    'error': True,
                    'msg': 'группы не существует'
                }
    else:
        data = {
            'error': True,
            'msg': 'не зарегистрированный пользователь'
        }
    return JsonResponse(data)


class AddProductView(View):

    @auth_decoration
    def get(self, request, id):
        form = ProductForm()
        group_product = GroupProductModel.objects.get(id=id)
        data = {
            'form': form,
            'group_product': group_product.group_title
        }
        return render(request, 'product/product_add.html', data)

    @auth_decoration
    def post(self, request, id):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_group = GroupProductModel.objects.get(id=id)
            form.article = form.cleaned_data['article']
            form.product_name = form.cleaned_data['product_name']
            form.declaration = form.cleaned_data['declaration']
            form.protocol = form.cleaned_data['protocol']
            form.specification = form.cleaned_data['specification']
            form.quality_certificate = form.cleaned_data['quality_certificate']
            form.price = form.cleaned_data['price']
            form.product_type = form.cleaned_data['product_type']
            el = form.save(commit=False)
            el.product_group = product_group
            el.save()
            return redirect('product_list', id)

        group_product = GroupProductModel.objects.get(id=id)
        data = {
            'form': form,
            'group_product': group_product.group_title
        }
        return render(request, 'product/product_add.html', data)


class EditProductView(View):

    @auth_decoration
    def get(self, request, id):
        product = ProductModel.objects.get(id=id)
        form = ProductForm(instance=product)
        if product.packing:
            pac = ProductPackagingModel.objects.get(id=product.packing.id)
            form_packing = ProductPackingForm(instance=pac)
        else:
            form_packing = ProductPackingForm()
        data = {'form': form, 'product': product, 'form_packing':form_packing}

        return render(request, 'product/product_edit.html', data)

    @auth_decoration
    def post(self, request, id):
        product = ProductModel.objects.get(id=id)
        if 'product' in request.POST:
            form = ProductForm(request.POST, request.FILES)

            if form.is_valid():
                product.article = form.cleaned_data['article']
                product.product_name = form.cleaned_data['product_name']
                if form.cleaned_data['declaration']:
                    product.declaration = form.cleaned_data['declaration']
                if form.cleaned_data['protocol']:
                    product.protocol = form.cleaned_data['protocol']
                if form.cleaned_data['specification']:
                    product.specification = form.cleaned_data['specification']
                if form.cleaned_data['quality_certificate']:
                    product.quality_certificate = form.cleaned_data['quality_certificate']
                product.price = form.cleaned_data['price']
                product.product_type = form.cleaned_data['product_type']
                product.save()
                product_group_id = product.product_group.id
                return redirect('product_list', product_group_id)
            else:
                form_packing = ProductPackingForm()
                data = {'form': form, 'product': product, 'form_packing':form_packing}

                return render(request, 'product/product_edit.html', data)
        elif 'packing' in request.POST:
            form_packing = ProductPackingForm(request.POST)
            if form_packing.is_valid():
                new_packing = ProductPackagingModel.objects.create(
                    product = product.product_name,
                    packing_name = form_packing.cleaned_data['packing_name'],
                    netto = form_packing.cleaned_data['netto'],
                    brutto = form_packing.cleaned_data['brutto'],
                    quantity_box = form_packing.cleaned_data['quantity_box']
                )
                product.packing = new_packing
                product.save()
                product_group_id = product.product_group.id
                return redirect('product_list', product_group_id)
            else:
                form = ProductForm()
                data = {'form': form, 'product': product, 'form_packing':form_packing}

                return render(request, 'product/product_edit.html', data)

def delete_product(request):
    if request.user.is_authenticated:
        id = request.GET.get('id')
        product = ProductModel.objects.get(id=id)
        product.delete()
        data = {
            'error': False
        }
        return JsonResponse(data)

    else:
        data = {
            'error': True,
            'msg': 'не зарегистрированный пользователь'
        }
    return JsonResponse(data)


def pruduct_packing(request):
    if request.user.is_authenticated:
        id = request.GET.get('id')
        obj = ProductPackagingModel.objects.get(id=id)
        product = obj.product
        packing_name = obj.packing_name
        netto = obj.netto
        brutto = obj.brutto
        quantity_box = obj.quantity_box
        pallet_weight_netto = obj.pallet_weight_netto
        pallet_weight_brutto = obj.pallet_weight_brutto
        data = f'<p class="popup_title_text">{product}</p>' \
               f'<p class="popup_text">упаковка: {packing_name};</p>' \
               f'<p class="popup_text">масса нетто (кор/вед): {netto};</p>' \
               f'<p class="popup_text">масса брутто (кор/вед): {brutto};</p>' \
               f'<p class="popup_text">кол-во (кор/вед) на поддоне: {quantity_box};</p>' \
               f'<p class="popup_text">масса палета нетто: {pallet_weight_netto};</p>' \
               f'<p class="popup_text">масса палета брутто: {pallet_weight_brutto};</p>' \
      #         f'<a href="#" id="packing_edit" class="btn_add_group packing_center" data-value="{id}">изменить</a>'
        return HttpResponse(data)
    else:
        data = '<p>ошибка запроса пользователь не авторизован</p>'
        return HttpResponse(data)

def packing_edit_get(request):
    if request.user.is_authenticated:
        id = request.GET.get('id')
        obj = ProductPackagingModel.objects.get(id=id)
        form = ProductPackingForm(instance=obj)
        data = f'<p class="popup_title_text">{obj.product}</p>' \
               f'{form.as_p()}' \
               f'<a href="#" id="packing_edit_post" class="btn_add_group packing_center" data-value="{id}">отправить</a>'

        return HttpResponse(data)
    else:
        data = '<p>ошибка запроса пользователь не авторизован</p>'
        return HttpResponse(data)

def packing_edit_post(request):
    if request.user.is_authenticated:
        id = request.GET.get('id')
        packing_name = request.GET.get('packing_name')
        netto = request.GET.get('netto')
        brutto = request.GET.get('brutto')
        quantity_box = request.GET.get('quantity_box')
        obj = ProductPackagingModel.objects.get(id=id)
        obj.packing_name = packing_name
        obj.netto = Decimal(netto.replace(',','.'))
        obj.brutto =Decimal(brutto.replace(',','.'))
        obj.quantity_box = int(quantity_box)
        obj.save()

        data = {
            'error': False
        }
        return JsonResponse(data)
    else:
        data = {
            'error': True
        }
        return JsonResponse(data)
