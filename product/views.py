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
        products = ProductModel.objects.filter(product_group_id=id).values('id', 'article', 'product_name')
        group_title = GroupProductModel.objects.filter(id=id).only('group_title')[0]
        data = {
            'products': products,
            'group_title': group_title
        }
        return render(request, 'product/product_list.html', data)


class ProductItemView(View):
    pass


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
    def get(self, request):
        form = ProductForm()
        data = {
            'form': form
        }
        return render(request, 'product/product_add.html', data)

    @auth_decoration
    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.article = form.cleaned_data['article']
            form.product_name = form.cleaned_data['product_name']
            form.product_group = form.cleaned_data['product_group']
            form.declaration = form.cleaned_data['declaration']
            form.protocol = form.cleaned_data['protocol']
            form.specification = form.cleaned_data['specification']
            form.quality_certificate = form.cleaned_data['quality_certificate']
            form.save()

            id = form.cleaned_data['product_group']
            products = ProductModel.objects.filter(product_group_id=id).values('id', 'article', 'product_name')
            group_title = GroupProductModel.objects.filter(group_title=id).only('group_title')[0]
            data = {
                'products': products,
                'group_title': group_title
            }
            return render(request, 'product/product_list.html', data)

        data = {
            'form': form
        }
        return render(request, 'product/product_add.html', data)
