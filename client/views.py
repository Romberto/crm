from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from client.forms import ClientForm
from client.models import ClientModel


def auth_decoration(func):
    def wraper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')

        return func(self, request, *args, **kwargs)

    return wraper


# все кленты принадлежащию менеджеру

class AllClientsView(View):
    @auth_decoration
    def get(self, request):
        if request.user.profile.position != "DR":
            clients = ClientModel.objects.all().values('id',
                                                       'face_contact',
                                                       'name',
                                                       'phone',
                                                       'phone2',
                                                       'phone3',
                                                       ).order_by(
                '-id')
            if clients:

                data = {
                    'clients': clients
                }
            else:
                data = {
                    'clients': None
                }
            return render(request, 'client/all_clients.html', data)
        else:
            clients = ClientModel.objects.filter(owner_manager=request.user.id).values('id',
                                                                                       'face_contact',
                                                                                       'name',
                                                                                       'phone',
                                                                                       'phone2',
                                                                                       'phone3',
                                                                                       ).order_by(
                '-id')
            if clients:

                data = {
                    'clients': clients
                }
            else:
                data = {
                    'clients': None
                }
            return render(request, 'client/all_clients.html', data)


# конкретный клиент
class DetailClientView(View):
    @auth_decoration
    def get(self, request, id_client):
        try:
            client = ClientModel.objects.get(id=id_client)
            form_client = ClientForm(instance=client)
            data = {
                'client': client,
                'form_client': form_client
            }
        except ClientModel.DoesNotExist:
            data = {
                'client': None
            }

        return render(request, 'client/detail_client.html', data)

    @auth_decoration
    def post(self, request, id_client):
        if 'client' in request.POST:
            client_model = ClientModel.objects.get(id=id_client)
            form = ClientForm(request.POST, instance=client_model)
            if form.is_valid():
                form.save()
                clients = ClientModel.objects.all().values('id', 'face_contact', 'name',
                                                           'phone').order_by('-id')
                data = {
                    'clients': clients
                }
                return render(request, 'client/all_clients.html', data)
            else:
                data = {
                    'client': client_model,
                    'form_client': form
                }

                return render(request, "client/detail_client.html", data)


# добавить нового клиента

class AddClientView(View):
    @auth_decoration
    def get(self, request):
        data = {
            'form': ClientForm()
        }
        return render(request, 'client/add_client.html', data)

    @auth_decoration
    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            owner_manager = request.user

            name = form.cleaned_data['name']

            phone = ''
            for i in form.cleaned_data['phone']:
                if i == '+' or i.isdigit():
                    phone += i
            phone2 = ''
            if form.cleaned_data['phone2']:
                for i in form.cleaned_data['phone2']:
                    if i == '+' or i.isdigit():
                        phone2 += i
            phone3 = ''
            if form.cleaned_data['phone3']:
                for i in form.cleaned_data['phone3']:
                    if i == '+' or i.isdigit():
                        phone3 += i
            inn = form.cleaned_data['inn']
            mail = form.cleaned_data['mail']
            if not mail:
                mail = None
            fact_address = form.cleaned_data['fact_address']
            if not fact_address:
                fact_address = ''
            jurist_address = form.cleaned_data['jurist_address']
            if not jurist_address:
                jurist_address = ''
            activity = form.cleaned_data['activity']
            face_contact = form.cleaned_data['face_contact']
            site = form.cleaned_data['site']
            if not site:
                site = ''
            agreement = form.cleaned_data['agreement']

            new_client = ClientModel(
                owner_manager=owner_manager,
                name=name,
                phone=phone,
                phone2=phone2,
                phone3=phone3,
                mail=mail,
                inn=inn,
                fact_address=fact_address,
                jurist_address=jurist_address,
                activity=activity,
                face_contact=face_contact,
                site=site,
                agreement=agreement,
            )
            new_client.save()
            return redirect('all_clients')

        else:

            return render(request, 'client/add_client.html', {'form': form})


class ClientDeleteView(View):
    @auth_decoration
    def get(self, request, id_client):
        try:
            client = ClientModel.objects.get(id=id_client)

            client.delete()
        except ClientModel.DoesNotExist:
            return render(request, 'client/errors_client.html')
        return redirect('all_clients')
