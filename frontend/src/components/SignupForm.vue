<template>
  <div class="signup">
    <h2>Signup</h2>
    <form @submit.prevent="signup">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Signup</button>
    </form>
    <p v-if="message" :class="{ success: success, error: !success }">{{ message }}</p>
  </div>
</template>

<script>
import apiClient from '../api/api';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      message: null,
      success: false,
    };
  },
  methods: {
    async signup() {
      try {
        const response = await apiClient.post('/signup', {
          username: this.username,
          email: this.email,
          password: this.password,
        });

        console.log('Resposta da API:', response);
        this.success = true;
        this.message = response.data.message;

        setTimeout(() => {
          this.$router.push('/login');
        }, 2000);

      } catch (err) {
        console.error('Erro na requisição:', err);
        this.success = false;
        if (err.response && err.response.status === 409) {
          this.message = 'Este e-mail já está em uso.';
        } else {
          this.message = 'Falha ao cadastrar. Por favor, tente novamente.';
        }
      }
    }
  }
};
</script>
