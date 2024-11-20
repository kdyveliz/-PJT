<template>
  <div>
    <h1>근처 은행 찾기</h1>
    <div id="map" style="width: 100%; height: 500px;"></div>
  </div>
</template>

<script>
export default {
  name: "BankLocator",
  data() {
    return {
      map: null,
    };
  },
  async mounted() {
    // 백엔드에서 API 키를 가져옵니다.
    const response = await fetch("/api/kakao-map-key/");
    const data = await response.json();
    const KAKAO_MAP_API_KEY = data.api_key;

    // 카카오맵 SDK 동적 로드
    const script = document.createElement("script");
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_MAP_API_KEY}&libraries=services`;
    script.onload = this.initMap; // 스크립트 로드 후 지도 초기화
    document.head.appendChild(script);
  },
  methods: {
    initMap() {
      const container = document.getElementById("map");
      const options = {
        center: new kakao.maps.LatLng(37.5665, 126.978), // 서울 중심 좌표
        level: 3, // 지도 확대 레벨
      };
      this.map = new kakao.maps.Map(container, options); // 지도 생성
    },
  },
};
</script>

<style scoped>
#map {
  margin: 20px 0;
}
</style>
