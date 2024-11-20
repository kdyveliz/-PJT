from django.shortcuts import render
from django.conf import settings
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from rest_framework import status
from .models import DepositProducts, DepositOptions, SavingsProducts, SavingsOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingsProductsSerializer, SavingsOptionsSerializer
from datetime import datetime


# 날자 문자열을 Python 날짜 객체로 반환하는 헬퍼 함수
def parse_date(date_str):
    if date_str and len(date_str) == 8:  # "YYYYMMDD" 형식
        return datetime.strptime(date_str, "%Y%m%d").date()
    return None


# 예금 상품 데이터를 외부 API에서 가져와 저장
@api_view(['GET'])
def save_deposit_products(request):
    API_KEY = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()

    data_product = response['result']['baseList'] # 예금 상품 데이터
    data_options = response['result']['optionList'] # 예금 상품 옵션 데이터

    product_dict = {} # 예금 상품 코드를 기반으로 매핑하기 위한 딕셔너리
    for value in data_product:
        # 예금 상품을 저장하거나 업데이트
        deposit_product, created = DepositProducts.objects.update_or_create(
            fin_prdt_cd=value["fin_prdt_cd"],
            defaults={
                'kor_co_nm': value["kor_co_nm"], # 금융회사명
                'fin_prdt_nm': value["fin_prdt_nm"], # 금융상품명
                'etc_note': value.get("etc_note"), # 기타유의사항
                'join_deny': value.get("join_deny", 1), # 가입제한조건
                'join_member': value["join_member"], # 가입대상
                'join_way': value["join_way"], # 가입방법
                'spcl_cnd': value.get("spcl_cnd"), # 우대조건
                'dcls_strt_day': parse_date(value.get("dcls_strt_day")), # 공시시작일 ( 필요없음 )
                'dcls_end_day': parse_date(value.get("dcls_end_day")), # 공시종료일 ( 필요없음 )
                'fin_co_subm_day': parse_date(value.get("fin_co_subm_day")), # 금융회사제출일 ( 필요없음 )
                'dcls_month': value.get("dcls_month"),  # 공시월
            }
        )
        product_dict[value["fin_prdt_cd"]] = deposit_product

    for option_data in data_options:
        if option_data['fin_prdt_cd'] in product_dict:
            # 적금 상품 옵션 저장 또는 업데이트
            DepositOptions.objects.update_or_create(
                product=product_dict[option_data['fin_prdt_cd']],
                fin_prdt_cd=option_data['fin_prdt_cd'],
                defaults={
                    'intr_rate_type_nm': option_data.get('intr_rate_type_nm', 'Unknown'),
                    'intr_rate': float(option_data['intr_rate']) if option_data.get('intr_rate') else -1,
                    'intr_rate2': float(option_data['intr_rate2']) if option_data.get('intr_rate2') else -1,
                    'save_trm': option_data.get('save_trm', 0),
                }
            )
    return Response({"message": "Deposit products saved successfully."})


# 적금 상품 저장
@api_view(['GET'])
def save_savings_products(request):
    API_KEY = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()

    data_product = response['result']['baseList']
    data_options = response['result']['optionList']

    product_dict = {}
    for value in data_product:
        savings_product, created = SavingsProducts.objects.update_or_create(
            fin_prdt_cd=value["fin_prdt_cd"],
            defaults={
                'kor_co_nm': value["kor_co_nm"],
                'fin_prdt_nm': value["fin_prdt_nm"],
                'etc_note': value.get("etc_note"),
                'join_deny': value.get("join_deny", 1),
                'join_member': value["join_member"],
                'join_way': value["join_way"],
                'spcl_cnd': value.get("spcl_cnd"),
                'dcls_strt_day': parse_date(value.get("dcls_strt_day")),
                'dcls_end_day': parse_date(value.get("dcls_end_day")),
                'fin_co_subm_day': parse_date(value.get("fin_co_subm_day")),
                'dcls_month': value.get("dcls_month"),  # 공시월 저장
            }
        )
        product_dict[value["fin_prdt_cd"]] = savings_product

    for option_data in data_options:
        if option_data['fin_prdt_cd'] in product_dict:
            SavingsOptions.objects.update_or_create(
                product=product_dict[option_data['fin_prdt_cd']],
                fin_prdt_cd=option_data['fin_prdt_cd'],
                defaults={
                    'intr_rate_type_nm': option_data['intr_rate_type_nm'],
                    'intr_rate': float(option_data.get('intr_rate', -1)),
                    'intr_rate2': float(option_data.get('intr_rate2', -1)),
                    'save_trm': option_data['save_trm'],
                }
            )
    return Response({"message": "Savings products saved successfully."})

# 예금 상품 조회 및 추가
@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 특정 예금 상품 옵션 조회
@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    # 특정 예금 상품 코드(fin_prdt_cd)에 해당하는 옵션 데이터를 조회
    if request.method == 'GET':
        options = get_list_or_404(DepositOptions, fin_prdt_cd=fin_prdt_cd)
        serializer = DepositOptionsSerializer(options, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 최고 금리 예금 상품 조회
@api_view(['GET'])
def top_rate(request):
    top_option = DepositOptions.objects.order_by('-intr_rate2').first()
    if not top_option:
        return Response({"error": "No deposit options available."}, status=status.HTTP_404_NOT_FOUND)

    product = top_option.product
    product_serializer = DepositProductsSerializer(product)
    options = DepositOptions.objects.filter(product=product)
    options_serializer = DepositOptionsSerializer(options, many=True)

    return Response({
        "product": product_serializer.data,
        "options": options_serializer.data
    }, status=status.HTTP_200_OK)


# 적금 상품 조회 및 추가
@api_view(['GET', 'POST'])
def savings_products(request):
    if request.method == 'GET':
        products = SavingsProducts.objects.all()
        serializer = SavingsProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = SavingsProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 특정 적금 상품 옵션 조회
@api_view(['GET'])
def savings_product_options(request, fin_prdt_cd):
    if request.method == 'GET':
        options = get_list_or_404(SavingsOptions, fin_prdt_cd=fin_prdt_cd)
        serializer = SavingsOptionsSerializer(options, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 최고 금리 적금 상품 조회
@api_view(['GET'])
def top_rate_savings_products(request):
    top_option = SavingsOptions.objects.order_by('-intr_rate2').first()
    if not top_option:
        return Response({"error": "No savings options available."}, status=status.HTTP_404_NOT_FOUND)

    product = top_option.product
    product_serializer = SavingsProductsSerializer(product)
    options = SavingsOptions.objects.filter(product=product)
    options_serializer = SavingsOptionsSerializer(options, many=True)

    return Response({
        "product": product_serializer.data,
        "options": options_serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProducts.objects.all()
        product_data = []

        for product in products:
            # 각 상품에 대한 직렬화 데이터 생성
            product_serializer = DepositProductsSerializer(product)
            product_dict = product_serializer.data

            # 해당 상품의 옵션 직렬화 추가
            options = DepositOptions.objects.filter(product=product)
            options_serializer = DepositOptionsSerializer(options, many=True)
            
            # 각 금리 기간별 데이터를 초기화
            product_dict['rate_6m'] = "-"
            product_dict['rate_12m'] = "-"
            product_dict['rate_24m'] = "-"
            product_dict['rate_36m'] = "-"

            # 각 옵션 데이터를 순회하며 저장
            for option in options_serializer.data:
                save_term = option['save_trm']
                rate = option['intr_rate']
                if save_term == 6:
                    product_dict['rate_6m'] = rate
                elif save_term == 12:
                    product_dict['rate_12m'] = rate
                elif save_term == 24:
                    product_dict['rate_24m'] = rate
                elif save_term == 36:
                    product_dict['rate_36m'] = rate

            product_data.append(product_dict)

        return Response(product_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def deposit_product_detail(request, fin_prdt_cd):
    try:
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        product_serializer = DepositProductsSerializer(product)
        options = DepositOptions.objects.filter(product=product)
        options_serializer = DepositOptionsSerializer(options, many=True)
        product_data = product_serializer.data
        product_data['options'] = options_serializer.data
        return Response(product_data, status=status.HTTP_200_OK)
    except DepositProducts.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)