<template>
  <v-container>
    <v-form>
      <v-text-field
          label="Email"
          v-model="email"
          required
      ></v-text-field>

      <v-text-field
          label="Username"
          v-model="username"
          required
      ></v-text-field>

      <v-text-field
          label="Password"
          v-model="password"
          type="password"
          required
      ></v-text-field>

      <v-text-field
          label="Confirm Password"
          v-model="confirmPassword"
          type="password"
          required
      ></v-text-field>

      <v-btn @click="handleSubmit">Register</v-btn>
    </v-form>
  </v-container>
</template>


<script>
import { ref } from 'vue';
import { signup } from '@/api/api';  // Importa a função de signup

export default {
  name: 'SignupForm',
  setup() {
    const email = ref('');
    const username = ref('');
    const password = ref('');
    const confirmPassword = ref('');  // O campo confirmPassword deve ser com "C" maiúsculo

    const handleSubmit = async () => {
      try {
        const response = await signup(email.value, username.value, password.value, confirmPassword.value);
        console.log(response);  // Sucesso no cadastro
        // Redirecionar ou exibir mensagem de sucesso
      } catch (error) {
        console.error('Erro ao realizar o cadastro:', error);
        // Lidar com o erro de cadastro
      }
    };

    return {
      email,
      username,
      password,
      confirmPassword,
      handleSubmit,
    };
  },
};
</script>


