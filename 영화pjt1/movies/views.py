import requests
from django.shortcuts import render

# TMDb API 키
TMDB_API_KEY = '6195257da4446fc7851e62e6456c7e1b'

# 기분과 장르 매핑
MOOD_GENRE_MAPPING = {
    'happy': 35,        
    'sad': 18,          
    'interested': 28,       
    'calm': 10749    
}

# 메인 페이지 (기분 선택)
def index(request):
    
    return render(request, 'movies/index.html')


# 영화 추천 로직
def recommend_movie(request, mood):
    genre_id = MOOD_GENRE_MAPPING.get(mood)
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&language=ko-KR'
    
    response = requests.get(url)
    movies = []
    
    if response.status_code == 200:
        # TMDb 응답에서 영화 목록 가져오기
        data = response.json()
        movies = data.get('results', [])
        context = {
            'movies': movies,
            'mood': mood
        }
    return render(request, 'movies/recommend.html', context)


# 영화 상세 정보 로직
def movie_detail(request, movie_id):
    # 영화 상세 정보 가져오기
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ko-KR"
    response = requests.get(movie_url)
    movie = response.json()

    # 영화 예고편 가져오기
    trailer_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=ko-KR"
    trailer_response = requests.get(trailer_url)
    trailers = trailer_response.json().get('results', [])

    # 유튜브 예고편 필터링 (유튜브 영상만 필터링)
    youtube_trailer = None
    for trailer in trailers:
        if trailer['site'] == 'YouTube' and trailer['type'] == 'Trailer':
            youtube_trailer = trailer['key']
            break

    return render(request, 'movies/detail.html', {
        'movie': movie,
        'youtube_trailer': youtube_trailer,
    })