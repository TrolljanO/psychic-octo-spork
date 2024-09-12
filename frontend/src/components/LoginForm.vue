<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <div>
        <input type="checkbox" v-model="remember" />
        <label for="remember">Remember me</label>
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="message" :class="{ success: success, error: !success }">{{ message }}</p>
  </div>
</template>

<script>
import apiClient from '../api/api';

export default {
  data() {
    return {
      email: '',
      password: '',
      remember: false,
      message: null,
      success: false,
    };
  },
  methods: {
    async login() {
      try {
        const response = await apiClient.post('/login', {
          email: this.email,
          password: this.password,
          remember: this.remember,
        });

        this.success = true;
        this.message = response.data.message;

        // Armazenar o token JWT no localStorage
        localStorage.setItem('token', response.data.access_token);

        setTimeout(() => {
          this.$router.push('/services');
        }, 2000);

      } catch (err) {
        this.success = false;
        if (err.response && err.response.status === 401) {
          this.message = 'Por favor, verifique seus dados e tente novamente.';
        } else {
          this.message = 'Falha no login. Por favor, tente novamente.';
        }
      }
    },
  },
};
</script>
