from django import forms


class JRPCRequestFrom(forms.Form):
    endpoint = forms.URLField()
    method_name = forms.CharField()
    params = forms.JSONField(widget=forms.Textarea(), required=False)
