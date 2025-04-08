# forms.py
from django import forms
from django.db.models import Exists, OuterRef
from dcim.models import Device, Module, ModuleBay

def get_devices_with_free_bay():
    free_bays = ModuleBay.objects.filter(
        ~Exists(
            Module.objects.filter(module_bay_id=OuterRef('pk'))
        )
    )
    device_ids = free_bays.values_list('device_id', flat=True).distinct()
    return Device.objects.filter(pk__in=device_ids)

class Step1SelectForm(forms.Form):
    """
    Krok 1: Vybrat modul a cílové zařízení
    """
    selected_module = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        label="Modul k přesunu"
    )
    target_device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        label="Cílové zařízení"
    )

    def __init__(self, *args, module_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target_device'].queryset = get_devices_with_free_bay()
        # Pokud máme module_id, můžeme nastavit initial (nebo rovnou omezit queryset).
        if module_id:
            try:
                mod = Module.objects.get(pk=module_id)
                self.fields['selected_module'].initial = mod
                # Můžete i omezit queryset jen na [mod], jestli nechcete jinou volbu
                self.fields['selected_module'].queryset = Module.objects.filter(pk=module_id)
            except Module.DoesNotExist:
                pass

class Step2BayForm(forms.Form):
    """
    Krok 2: Vybrat ModuleBay pro vybrané zařízení
    """
    # sem nepotřebujeme selected_module, device atd. – už je máme v session
    target_module_bay = forms.ModelChoiceField(
        queryset=ModuleBay.objects.none(),
        label="Cílový module bay",
        required=True
    )

    def __init__(self, *args, **kwargs):
        # Device a modul, které jsme si zapamatovali v session
        device_id = kwargs.pop('device_id', None)
        super().__init__(*args, **kwargs)

        if device_id:
            self.fields['target_module_bay'].queryset = (
            ModuleBay.objects.filter(device_id=device_id))
