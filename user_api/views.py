from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test_api(request):
    return JsonResponse(
        {
            "result":666,
            "msg":"Aligado!"
        }
    )