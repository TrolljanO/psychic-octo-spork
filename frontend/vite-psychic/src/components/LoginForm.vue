<template>
  <v-container>
    <v-form>
      <v-text-field
          label="Email"
          v-model="email"
      ></v-text-field>
      <v-text-field
          label="Senha"
          v-model="password"
          type="password"
      ></v-text-field>

      <v-btn @click="login">Entrar</v-btn>

      <v-alert v-if="flashStore.message" :type="flashStore.type">
        {{ flashStore.message }}
      </v-alert>
    </v-form>
    <p>Não tem conta? <router-link to="/signup">Inscrever-se</router-link></p>
  </v-container>
</template>

<script>
import { ref } from 'vue';
import { login } from '@/api/api';  // Importa a função de login

export default {
  name: 'LoginForm',
  setup() {
    const email = ref('');
    const password = ref('');

    const handleLogin = async () => {
      try {
        const response = await login(email.value, password.value);
        console.log(response);  // Sucesso no login
        // Redirecionar para a página de serviços ou exibir mensagem de sucesso
      } catch (error) {
        console.error('Erro ao realizar o login:', error);
        // Lidar com o erro de login
      }
    };

    return {
      email,
      password,
      handleLogin,
    };
  },
};
</script>

