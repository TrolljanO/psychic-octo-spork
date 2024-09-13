<template>
  <v-form @submit.prevent="uploadFile">
    <v-file-input v-model="file" label="Escolher Arquivo" required></v-file-input>
    <v-btn type="submit" color="primary">Enviar</v-btn>
  </v-form>
</template>

<script>
import apiClient from '../api/api';  // Usa o Axios configurado

export default {
  data() {
    return {
      file: null,
    };
  },
  methods: {
    async uploadFile() {
      try {
        const formData = new FormData();
        formData.append('file', this.file);
        const response = await apiClient.post('/upload', formData);
        // Exibir mensagem de sucesso ou erro com base na resposta
      } catch (error) {
        console.error('Erro ao fazer upload:', error);
      }
    },
  },
};
</script>
