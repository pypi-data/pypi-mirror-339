from django.urls import path, include
from netbox.plugins import PluginConfig

class ModuleSwapConfig(PluginConfig):
    name = 'module_swap'
    verbose_name = 'Module Swap'
    description = 'Plugin allows swapping modules between devices while keeping history.'
    version = '1.0'
    author = 'Viktor Kubec'
    author_email = 'Viktor.Kubec@gmail.com'
    base_url = 'module-swap'

config = ModuleSwapConfig
