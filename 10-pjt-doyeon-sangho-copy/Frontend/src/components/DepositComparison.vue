<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 상태 변수
const depositProducts = ref([]);
const selectedBank = ref('전체은행');
const selectedTerm = ref('전체기간');
const filteredProducts = ref([]);

const banks = ref(['전체은행','광주은행','경남은행','국민은행','농협은행주식회사','아이엠뱅크', '우리은행', '대구은행', '부산은행','수협은행','전북은행','제주은행' , '주식회사카카오뱅크','주식회사케이뱅크','중소기업은행' ,'토스뱅크주식회사', '한국스탠다드차타드은행','하나은행']); // 예시 은행 목록
const terms = ref(['전체기간', '6개월', '12개월', '24개월', '36개월']);

// API URL
const API_URL = 'http://127.0.0.1:8000/api/deposit-products/';

// 데이터 가져오기
const fetchDepositProducts = async () => {
  try {
    const response = await axios.get(API_URL);
    depositProducts.value = response.data;
    filterProducts();
  } catch (error) {
    console.error('Failed to fetch deposit products:', error);
  }
};

// 필터링 함수
const filterProducts = () => {
  filteredProducts.value = depositProducts.value.filter((product) => {
    const bankMatches = selectedBank.value === '전체은행' || product.kor_co_nm === selectedBank.value;
    const termMatches = selectedTerm.value === '전체기간' || checkTermMatch(product, selectedTerm.value);
    return bankMatches && termMatches;
  });
};

// 가입 기간에 따른 금리 데이터 확인 함수
const checkTermMatch = (product, term) => {
  const saveTerms = {
    '6개월': product.rate_6m,
    '12개월': product.rate_12m,
    '24개월': product.rate_24m,
    '36개월': product.rate_36m,
  };
  return saveTerms[term] !== undefined;
};

onMounted(() => {
  fetchDepositProducts();
});
</script>

<template>
  <div>
    <h1>정기예금</h1>
    <div class="filter-section">
      <label>
        은행을 선택하세요:
        <select v-model="selectedBank" @change="filterProducts">
          <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
        </select>
      </label>
      <label>
        예치 기간:
        <select v-model="selectedTerm" @change="filterProducts">
          <option v-for="term in terms" :key="term" :value="term">{{ term }}</option>
        </select>
      </label>
      <button @click="filterProducts">확인</button>
    </div>
    <table class="products-table">
      <thead>
        <tr>
          <th>공시 제출일</th>
          <th>금융회사명</th>
          <th>상품명</th>
          <th>6개월 금리</th>
          <th>12개월 금리</th>
          <th>24개월 금리</th>
          <th>36개월 금리</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd">
          <td>{{ product.dcls_strt_day }}</td>
          <td>{{ product.kor_co_nm }}</td>
          <td><router-link :to="`/deposit-products/${product.fin_prdt_cd}`">{{ product.fin_prdt_nm }}</router-link></td>
          <td>{{ product.rate_6m || '-' }}</td>
          <td>{{ product.rate_12m || '-' }}</td>
          <td>{{ product.rate_24m || '-' }}</td>
          <td>{{ product.rate_36m || '-' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.filter-section {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}
.products-table {
  width: 100%;
  border-collapse: collapse;
}
.products-table th, .products-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
.products-table th {
  background-color: #f2f2f2;
}
</style>
