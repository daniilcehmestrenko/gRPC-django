import uuid
import json
import requests

from django.conf import settings
from django.shortcuts import render

from foo.forms import JRPCRequestFrom


def main_view(request):
    result = None
    if request.method == 'POST':
        form = JRPCRequestFrom(request.POST)
        if form.is_valid():
            cert = (settings.CER_PATH, settings.KEY_PATH)
            url = form.cleaned_data['endpoint']
            headers = {"content-type": "application/json"}
            payload = {
                "jsonrpc": "2.0",
                "method": form.cleaned_data['method_name'],
                "id": str(uuid.uuid4()),
            }
            if params := form.cleaned_data['params']:
                payload.update(params=params)
            try:
                payload = json.dumps(payload)
                response = requests.post(
                    url=url,
                    data=payload,
                    headers=headers,
                    cert=cert,
                )
                result = response.json()
            except Exception as error:
                result = str(error)
    else:
        form = JRPCRequestFrom()
    context = {
        'form': form,
        'result': result
    }
    return render(request, 'foo/main.html', context)
