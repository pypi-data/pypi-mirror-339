# netbox/plugins/module_inventory_binder/navigation.py

from netbox.plugins import PluginMenuItem

# Define menu items for the plugin
menu_items = (
    PluginMenuItem(
        link='plugins:module_swap:step1_select',
        link_text='Module Swap',
    ),
)
