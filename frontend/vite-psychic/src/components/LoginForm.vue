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

      <v-btn @click="handleLogin">Entrar</v-btn>

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
import { useFlashStore } from '@/stores/flashStore';  // Store para mensagens
import router from "@/router/index.js";  // Importa o roteador para redirecionamento

export default {
  name: 'LoginForm',
  setup() {
    const email = ref('');
    const password = ref('');
    const flashStore = useFlashStore();  // Usa o flashStore da Pinia

    const handleLogin = async () => {
      try {
        // Chama a API de login e espera pela resposta
        const response = await login(email.value, password.value);

        if (response.message === "login efetuado com sucesso") {
          // Define a mensagem flash
          flashStore.setMessage({
            message: 'Login efetuado com sucesso!',
            type: 'success',
          });

          // Redireciona para a página /index
          router.push('/index');
        }
      } catch (error) {
        // Em caso de erro, mostra a mensagem de erro
        flashStore.setMessage({
          message: 'Erro no login. Verifique suas credenciais.',
          type: 'error',
        });
      }
    };

    return {
      email,
      password,
      handleLogin,
      flashStore,
    };
  }
};
</script>
