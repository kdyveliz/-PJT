import requests
from django.http import JsonResponse
from django.conf import settings
from urllib3.exceptions import InsecureRequestWarning
import urllib3

# 일본화폐, 중국화폐 안불러와짐

# Disable SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)

def get_exchange_rate(request):
    """
    한국수출입은행 API를 통해 환율 데이터를 가져옵니다.
    """
    base_currency = request.GET.get('base', 'KRW')  # 기준 통화 (기본값: KRW)
    target_currency = request.GET.get('target', 'USD')  # 대상 통화 (기본값: USD)
    amount = float(request.GET.get('amount', 1))  # 입력 금액 (기본값: 1)

    # 한국수출입은행 API 호출 URL
    url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXPORT_IMPORT_BANK_API_KEY}&searchdate=&data=AP01"

    try:
        # API 호출
        response = requests.get(url, verify=False)
        response.raise_for_status()
        exchange_data = response.json()

        # 기준 통화와 대상 통화의 환율 찾기
        base_rate = next((item for item in exchange_data if item['cur_unit'] == base_currency), None)
        target_rate = next((item for item in exchange_data if item['cur_unit'] == target_currency), None)

        if not base_rate:
            return JsonResponse({'error': f'Base currency {base_currency} not found.'}, status=400)
        if not target_rate:
            return JsonResponse({'error': f'Target currency {target_currency} not found.'}, status=400)

        base_exchange_rate = float(base_rate['deal_bas_r'].replace(',', ''))
        target_exchange_rate = float(target_rate['deal_bas_r'].replace(',', ''))

        print("Base Currency:", base_currency)
        print("Target Currency:", target_currency)
        print("Amount:", amount)
        print("Base Exchange Rate (KRW per Base):", base_exchange_rate)
        print("Target Exchange Rate (KRW per Target):", target_exchange_rate)

        # 계산
        if base_currency == 'KRW':
            # KRW → 타국 통화
            converted_value = amount / target_exchange_rate
        elif target_currency == 'KRW':
            # 타국 통화 → KRW
            converted_value = amount * base_exchange_rate
        else:
            # 타국 통화 A → KRW → 타국 통화 B
            converted_value = (amount * base_exchange_rate) / target_exchange_rate

        return JsonResponse({
            'result': 'success',
            'base_currency': base_currency,
            'target_currency': target_currency,
            'exchange_rate': target_exchange_rate if base_currency == 'KRW' else base_exchange_rate,
            'converted_value': round(converted_value, 2),
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    



# # import requests
# # from urllib3.exceptions import InsecureRequestWarning
# # from django.http import JsonResponse
# # from django.conf import settings

# # # SSL 경고 비활성화
# # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# # def get_exchange_rate(request):
# #     """
# #     한국수출입은행 API를 통해 환율 데이터를 가져옵니다.
# #     """
# #     base_currency = request.GET.get('base', 'KRW')  # 기준 통화 (기본값: KRW)
# #     target_currency = request.GET.get('target', 'USD')  # 대상 통화 (기본값: USD)
# #     amount = float(request.GET.get('amount', 1))  # 입력 금액 (기본값: 1)

# #     # 한국수출입은행 API 호출 URL
# #     url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXPORT_IMPORT_BANK_API_KEY}&searchdate=20241120&data=AP01"

# #     try:
# #         # API 호출 (verify=False로 SSL 검증 비활성화)
# #         response = requests.get(url, verify=False)
# #         response.raise_for_status()
# #         exchange_data = response.json()

# #         # 환율 찾기
# #         rate = next((item for item in exchange_data if item['cur_unit'] == target_currency), None)
# #         if not rate:
# #             return JsonResponse({'error': f'Currency {target_currency} not found.'}, status=400)

# #         exchange_rate = float(rate['deal_bas_r'].replace(',', ''))

# #         # 계산
# #         if base_currency == 'KRW':
# #             converted_value = amount / exchange_rate  # 원화를 타국 통화로 변환
# #         else:
# #             converted_value = amount * exchange_rate  # 타국 통화를 원화로 변환

# #         return JsonResponse({
# #             'result': 'success',
# #             'base_currency': base_currency,
# #             'target_currency': target_currency,
# #             'exchange_rate': exchange_rate,
# #             'converted_value': converted_value,
# #         })

# #     except Exception as e:
# #         return JsonResponse({'error': str(e)}, status=500)


# import requests
# from django.http import JsonResponse
# from django.conf import settings
# from urllib3.exceptions import InsecureRequestWarning
# import urllib3

# # SSL 경고 비활성화
# urllib3.disable_warnings(InsecureRequestWarning)

# def get_exchange_rate(request):
#     """
#     한국수출입은행 API를 통해 환율 데이터를 가져옵니다.
#     """
#     base_currency = request.GET.get('base', 'KRW')  # 기준 통화 (기본값: KRW)
#     target_currency = request.GET.get('target', 'USD')  # 대상 통화 (기본값: USD)
#     amount = float(request.GET.get('amount', 1))  # 입력 금액 (기본값: 1)

#     # 한국수출입은행 API 호출 URL
#     url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXPORT_IMPORT_BANK_API_KEY}&searchdate=&data=AP01"

#     try:
#         # API 호출
#         response = requests.get(url, verify=False)
#         response.raise_for_status()
#         exchange_data = response.json()

#         # 기준 통화와 대상 통화의 환율 찾기
#         base_rate = next((item for item in exchange_data if item['cur_unit'] == base_currency), None)
#         target_rate = next((item for item in exchange_data if item['cur_unit'] == target_currency), None)

#         if not base_rate:
#             return JsonResponse({'error': f'Base currency {base_currency} not found.'}, status=400)
#         if not target_rate:
#             return JsonResponse({'error': f'Target currency {target_currency} not found.'}, status=400)

#         base_exchange_rate = float(base_rate['deal_bas_r'].replace(',', ''))
#         target_exchange_rate = float(target_rate['deal_bas_r'].replace(',', ''))

#         # 계산
#         if base_currency == 'KRW':
#             # KRW → 타국 통화
#             converted_value = amount / target_exchange_rate
#         elif target_currency == 'KRW':
#             # 타국 통화 → KRW
#             converted_value = amount * base_exchange_rate
#         else:
#             # 타국 통화 A → KRW → 타국 통화 B
#             converted_value = (amount * base_exchange_rate) / target_exchange_rate

#         return JsonResponse({
#             'result': 'success',
#             'base_currency': base_currency,
#             'target_currency': target_currency,
#             'exchange_rate': target_exchange_rate if base_currency == 'KRW' else base_exchange_rate,
#             'converted_value': round(converted_value, 2),
#         })

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


