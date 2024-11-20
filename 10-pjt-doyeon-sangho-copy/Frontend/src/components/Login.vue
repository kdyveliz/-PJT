<template>
    <div>
      <h1>로그인</h1>
      <form @submit.prevent="loginUser">
        <label>
          사용자 이름:
          <input v-model="username" type="text" required />
        </label>
        <label>
          비밀번호:
          <input v-model="password" type="password" required />
        </label>
        <button type="submit">로그인</button>
      </form>
      <p>{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        message: '',
      };
    },
    methods: {
      async loginUser() {
        try {
          const response = await axios.post('http://127.0.0.1:8000/api/accounts/login/', {
            username: this.username,
            password: this.password,
          });
          this.message = response.data.message;
        } catch (error) {
          this.message = '로그인 실패';
          console.error(error);
        }
      },
    },
  };
  </script>
  