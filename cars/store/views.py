from django.shortcuts import render, get_object_or_404
from .models import Car
from .forms import CarForm, FilterForm
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from hitcount.views import HitCountDetailView
from django.conf import settings
from django.db import transaction
from django.db.models import F, Q
import stripe
import random
import string

class HomeView(ListView):
    model = Car
    paginate_by = 10
    template_name = 'home.html'
    def get_queryset(self):

        category_field = self.request.GET.get('category_field')
        label_field = self.request.GET.get('label_field')
        # Do your filter and search here
        if category_field == 'All':
            return Car.objects.all()
        if category_field:
            return Car.objects.filter(category__icontains=category_field)

        return Car.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FilterForm(initial={

            'category_field': self.request.GET.get('category_field', ''),
        })

        return context



class ItemDetailView(HitCountDetailView):
    model = Car
    template_name = 'product.html'
    count_hit = True




@login_required
def car_update(request, slug):
    '''if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
        '''
    instance = get_object_or_404(Car, slug=slug)
    if request.user != instance.user:
        raise Http404
    form = CarForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'successfully created', extra_tags='safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    '''else:
        messages.success(request, 'not created successfully', extra_tags='attention')
    '''
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'car_form.html', context)

@login_required
def add_car(request):
    '''if not request.user.is_staff or not request.user.is_superuser:
        raise Http404'''
    form = CarForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, 'successfully created', extra_tags='safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.warning(request, 'not created successfully', extra_tags='attention')
    context = {
        'form': form,
    }
    return render(request, 'car_form.html', context)



@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })