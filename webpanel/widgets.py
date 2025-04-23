from django import forms
from django.utils.safestring import mark_safe
import json

class PortMappingWidget(forms.Widget):
    template_name = "webpanel/port_mapping_widget.html"

    def format_value(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = {}
        return value or {}

    def value_from_datadict(self, data, files, name):
        raw = {}
        keys = data.getlist(f"{name}_key")
        values = data.getlist(f"{name}_value")
        for k, v in zip(keys, values):
            if k:
                try:
                    raw[k] = int(v)
                except ValueError:
                    raw[k] = v
        return json.dumps(raw)  # <-- FIX: return JSON string instead of dict

    def get_context(self, name, value, attrs):
        value = self.format_value(value)
        context = super().get_context(name, value, attrs)
        context["widget"].update({
            "name": name,
            "value": value,
        })
        return context
