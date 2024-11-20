from django.http import JsonResponse
from django.conf import settings

def get_kakao_map_key(request):
    """
    카카오 맵 API 키를 반환하는 뷰
    """
    return JsonResponse({'api_key': settings.KAKAO_MAP_API_KEY})
