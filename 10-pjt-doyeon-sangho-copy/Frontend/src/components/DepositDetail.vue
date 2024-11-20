<template>
    <div>
      <h1>정기예금 상세</h1>
      <div v-if="product">
        <p><strong>공시 제출월:</strong> {{ product.dcls_strt_day }}</p>
        <p><strong>금융회사명:</strong> {{ product.kor_co_nm }}</p>
        <p><strong>상품명:</strong> {{ product.fin_prdt_nm }}</p>
        <p><strong>가입제한:</strong> {{ product.join_deny }}</p>
        <p><strong>가입 방법:</strong> {{ product.join_way }}</p>
        <p><strong>우대조건:</strong> {{ product.spcl_cnd }}</p>
        
        <h3>가입 기간별 금리</h3>
        <ul>
          <li v-for="option in product.options" :key="option.id">
            {{ option.save_trm }}개월: 기본 금리 {{ option.intr_rate }}%, 우대 금리 {{ option.intr_rate2 || '-' }}%
          </li>
        </ul>
  
        <button v-if="isLoggedIn" @click="enrollProduct">가입하기</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  
  export default {
    setup() {
      const route = useRoute();
      const product = ref(null);
      const isLoggedIn = ref(false); // 로그인 상태를 관리하는 변수 (실제로는 Vuex 또는 Pinia 사용 권장)
  
      const fetchProductDetails = async () => {
        try {
          const finPrdtCd = route.params.fin_prdt_cd;
          const response = await axios.get(`http://127.0.0.1:8000/api/deposit-products/${finPrdtCd}/`);
          product.value = response.data;
        } catch (error) {
          console.error('Failed to fetch product details:', error);
        }
      };
  
      const enrollProduct = async () => {
        try {
          // 예시 API 호출 - 실제로는 사용자 정보와 연동하여 상품을 등록해야 함
          await axios.post('http://127.0.0.1:8000/api/enroll-product/', {
            product_id: product.value.id,
          });
          alert('가입 완료');
        } catch (error) {
          console.error('Failed to enroll product:', error);
          alert('가입 실패');
        }
      };
  
      onMounted(() => {
        fetchProductDetails();
        // 로그인 여부 체크 (예시)
        isLoggedIn.value = true; // 실제로는 인증 시스템과 연동해야 함
      });
  
      return {
        product,
        isLoggedIn,
        enrollProduct,
      };
    },
  };
  </script>
  
  <style scoped>
  button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  button:hover {
    background-color: #0056b3;
  }
  </style>
  