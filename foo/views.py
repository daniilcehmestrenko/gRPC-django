import uuid

from django.shortcuts import render

from foo import client
from foo.forms import JRPCRequestFrom
from foo.utils import get_cert_file_name, get_key_file_name


def main_view(request):
    result = None
    if request.method == 'POST':
        form = JRPCRequestFrom(request.POST)
        if form.is_valid():
            cert = (get_cert_file_name(), get_key_file_name())
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
                response = client.post(url, payload, headers, cert)
                result = response.read().decode()
            except Exception as error:
                result = str(error)
    else:
        form = JRPCRequestFrom()
    context = {
        'form': form,
        'result': result
    }
    return render(request, 'foo/main.html', context)
