from django.shortcuts import render, redirect
from django.views import View

from client.views import auth_decoration
from product.forms import ProductGroupForm, ProductForm
from product.models import GroupProductModel, ProductModel

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
                                                                                                           'quality_certificate',
                                                                                                           'product_group__group_title')
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
        data = {'form': form, 'product': product}

        return render(request, 'product/product_edit.html', data)

    @auth_decoration
    def post(self, request, id):
        form = ProductForm(request.POST, request.FILES)
        product = ProductModel.objects.get(id=id)
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
            product.save()
            products = ProductModel.objects.filter(product_group_id=product.product_group.id).select_related(
                'product_group').values('id',
                                        'article',
                                        'product_name',
                                        'price',
                                        'declaration',
                                        'protocol',
                                        'specification',
                                        'quality_certificate',
                                        'product_group__id',
                                        'product_group__group_title')
            product_group_title = products[0]['product_group__group_title']
            product_group_id = products[0]['product_group__id']
            data = {
                'products': products,
                'product_group_title': product_group_title,
                'product_groupe_id': product_group_id
            }
            return redirect('product_list', product_group_id)
        else:
            data = {'form': form, 'product': product}

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
