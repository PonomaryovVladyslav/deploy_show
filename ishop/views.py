from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.db import transaction

from Shop import settings
from ishop.forms import CustomUserCreationForm
from ishop.models import Good, ShopUser, Purchase, Refund
from ishop.tasks import delete_all_refunds
from ishop.tasks import approve_all_refunds


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class GoodsListView(ListView):
    paginate_by = 20
    http_method_names = ['post', 'get']
    template_name = 'goods_list.html'
    queryset = Good.objects.filter(in_stock__gt=0)
    extra_context = {'title': 'Online shop'}


class PurchaseView(View):
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            msg = "Only logged users can buy"
            messages.warning(self.request, msg)
            return redirect('login')

        user = self.request.user
        good = Good.objects.get(id=self.request.POST['pk'])
        quantity = int(self.request.POST['quantity'])
        price = good.price
        in_stock = good.in_stock
        wallet = user.wallet
        amount = quantity * price

        if wallet < amount:
            msg = "You don't have enough money for this purchase"
            messages.error(self.request, msg)
            return redirect('goods')

        if in_stock < quantity:
            msg = "We don't have enough goods in stock"
            messages.warning(self.request, msg)
            return redirect('goods')

        user.wallet -= amount
        good.in_stock -= quantity
        purchase = Purchase(customer=user, good=good, quantity=quantity, price=price)

        with transaction.atomic():
            user.save()
            good.save()
            purchase.save()

        msg = "Your purchase is done"
        messages.success(self.request, msg)

        return redirect('goods')


class PurchaseRefundView(View):
    http_method_names = ['post', ]

    @staticmethod
    def get_time_to_refund():
        interval = settings.INTERVAL_TO_REFUND
        return timezone.now() - timezone.timedelta(minutes=interval)

    def post(self, request, *args, **kwargs):
        purchase = Purchase.objects.get(pk=self.request.POST['pk'])

        if purchase.datetime < self.get_time_to_refund():
            msg = 'Your refund time has been expired'
            messages.error(self.request, msg)
            return redirect('account')

        Refund.objects.get_or_create(purchase=purchase)
        msg = 'Your refund request has been sent. Wait for approving.'
        messages.success(self.request, msg)

        return redirect('account')


class Account(LoginRequiredMixin, ListView):
    model = Purchase
    paginate_by = 10
    template_name = 'account.html'
    extra_context = {'title': 'My account'}

    def get_queryset(self):
        queryset = self.model.objects.filter(customer=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delta = PurchaseRefundView.get_time_to_refund()
        context['refund_possible'] = self.model.objects.filter(customer=self.request.user, datetime__gt=delta)
        in_refund = Refund.objects.filter(purchase__in=self.get_queryset())
        context['in_refund'] = in_refund.values_list('purchase__pk', flat=True)
        context['balance'] = self.request.user.wallet
        return context


class AdminRefundView(SuperUserRequiredMixin, ListView):
    model = Refund
    paginate_by = 10
    template_name = 'admin_refunds.html'
    extra_context = {'title': 'Admin: Purchases to refund'}


class AdminRefundProcessView(SuperUserRequiredMixin, View):
    http_method_names = ['post', ]
    model = Refund

    def post(self, request, *args, **kwargs):
        if request.POST.get('decline-all'):
            done = delete_all_refunds.delay()
            done.get()
            msg = 'All refunds have been declined'
            messages.success(self.request, msg)
            return redirect('adminrefund')

        if request.POST.get('approve-all'):
            done = approve_all_refunds.delay()
            done.get()
            msg = 'All refunds have been approved'
            messages.success(self.request, msg)
            return redirect('adminrefund')

        pk = self.request.POST['pk']
        approval = self.request.POST['approval']

        if approval == 'decline':
            self.model.objects.get(pk=pk).delete()
        else:
            refund = self.model.objects.get(pk=pk)
            user = refund.purchase.customer
            good = refund.purchase.good
            quantity = refund.purchase.quantity
            price = refund.purchase.price

            user.wallet += price * quantity
            good.in_stock += quantity

            with transaction.atomic():
                user.save()
                good.save()
                refund.purchase.delete()
                refund.delete()

        return redirect('adminrefund')


class AdminGoodsView(SuperUserRequiredMixin, ListView):
    model = Good
    paginate_by = 20
    template_name = 'admin_goods.html'
    extra_context = {'title': 'Admin: Goods'}


class AdminGoodEditView(SuperUserRequiredMixin, UpdateView):
    model = Good
    fields = ['title', 'description', 'price', 'image', 'in_stock']
    template_name = 'admin_good_edit.html'
    extra_context = {'title': 'Admin: edit'}
    success_url = '/admin-goods'


class AdminGoodAddView(SuperUserRequiredMixin, CreateView):
    model = Good
    template_name = 'admin_good_add.html'
    fields = '__all__'
    success_url = '/admin-goods'
    extra_context = {'title': 'Admin: add new good'}


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'

    def get_success_url(self):
        return self.success_url


class Register(CreateView):
    model = ShopUser
    form_class = CustomUserCreationForm
    success_url = '/'
    template_name = 'register.html'

    def form_valid(self, form):
        to_return = super().form_valid(form)
        login(self.request, self.object)
        msg = 'You have been successfully registered and logged in!'
        messages.success(self.request, msg)
        return to_return


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'
