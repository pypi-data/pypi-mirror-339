# views.py
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from .forms import Step1SelectForm, Step2BayForm
from dcim.models import Module, ModuleBay


class Step1SelectView(View):
    template_name = 'module_swap/step1_select.html'

    def get(self, request):
        module_id = request.GET.get('module_id')
        form = Step1SelectForm(module_id=module_id)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = Step1SelectForm(request.POST)
        if form.is_valid():
            # Uložíme do session
            selected_module = form.cleaned_data['selected_module']
            target_device = form.cleaned_data['target_device']
            request.session['selected_module_id'] = selected_module.pk
            request.session['target_device_id'] = target_device.pk

            return redirect('plugins:module_swap:step2_bay')
        else:
            messages.error(request, "Neplatný výběr modulu nebo zařízení.")
            return render(request, self.template_name, {'form': form})

class Step2BayView(View):
    template_name = 'module_swap/step2_bay.html'

    def get(self, request):
        # zkusíme načíst z session
        device_id = request.session.get('target_device_id')
        if not device_id:
            messages.warning(request, "Nejdřív je potřeba vybrat zařízení v kroku 1.")
            return redirect('plugins:module_swap:step1_select')

        form = Step2BayForm(device_id=device_id)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        device_id = request.session.get('target_device_id')
        module_id = request.session.get('selected_module_id')
        if not (device_id and module_id):
            messages.warning(request, "Nejdřív je potřeba vybrat modul a zařízení v kroku 1.")
            return redirect('plugins:module_swap:step1_select')

        form = Step2BayForm(request.POST, device_id=device_id)
        if form.is_valid():
            target_module_bay = form.cleaned_data['target_module_bay']

            # Nyní můžeme udělat logiku přesunu:
            selected_module = Module.objects.get(pk=module_id)
            # Příklad logiky:
            try:
                with transaction.atomic():
                    # 1. Odpojit modul od původního bay (pokud existuje)
                    old_bay = ModuleBay.objects.filter(module=selected_module).first()
                    if old_bay:
                        old_bay.module = None
                        old_bay.save()

                    # 2. Připojit modul k novému bay
                    selected_module.module_bay = target_module_bay
                    selected_module.device_id = target_module_bay.device_id
                    selected_module.save()
                messages.success(request, "Modul byl úspěšně přesunut do nového module bay.")
                # Smazat session
                del request.session['target_device_id']
                del request.session['selected_module_id']
                return redirect('dcim:device', pk=target_module_bay.device.pk)
            except Exception as e:
                messages.error(request, f"Chyba při přesunu: {e}")
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, "Neplatný výběr module bay.")
            return render(request, self.template_name, {'form': form})
