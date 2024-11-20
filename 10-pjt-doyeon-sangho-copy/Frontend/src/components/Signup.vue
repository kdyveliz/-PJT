<template>
    <div>
      <h1>회원가입</h1>
      <form @submit.prevent="registerUser">
        <label>
          사용자 이름:
          <input v-model="username" type="text" required />
        </label>
        <label>
          비밀번호:
          <input v-model="password" type="password" required />
        </label>
        <button type="submit">회원가입</button>
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
      async registerUser() {
        try {
          const response = await axios.post('http://127.0.0.1:8000/api/accounts/register/', {
            username: this.username,
            password: this.password,
          });
          this.message = response.data.message;
        } catch (error) {
          this.message = '회원가입 실패';
          console.error(error);
        }
      },
    },
  };
  </script>
  