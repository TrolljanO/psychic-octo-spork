<template>
  <v-container>
    <v-card class="mx-auto" max-width="800">
      <v-card-title>Limpa Pasta - Upload de Arquivo ZIP</v-card-title>
      <v-card-text>
        <!-- Formulário de Upload -->
        <v-form @submit.prevent="uploadFile">
          <v-file-input
              v-model="selectedFile"
              label="Escolha um arquivo ZIP"
              accept=".zip"
              prepend-icon="mdi-folder"
              required
          ></v-file-input>
          <v-btn type="submit" color="primary" :disabled="!selectedFile">Enviar</v-btn>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- Histórico de Uploads -->
    <v-card class="mx-auto mt-5" max-width="1200">
      <v-card-title>Histórico de Uploads</v-card-title>
      <v-data-table
          :headers="headers"
          :items="files"
          class="elevation-1"
          item-key="id"
          :items-per-page="5"
          disable-sort
      >
        <template v-slot:item.statusPago="{ item }">
          {{ item.statusPago ? 'Pago' : 'Aguardando Pagamento' }}
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn v-if="!item.statusPago" @click="generatePix(item.id)" color="primary">
            Gerar PIX
          </v-btn>
          <v-img v-if="item.qr_code" :src="item.qr_code" alt="QR Code" max-width="100"></v-img>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import apiClient from '../api/api';  // Axios configurado

export default {
  data() {
    return {
      selectedFile: null,
      files: [], // Histórico de uploads
      headers: [
        { text: 'Nome do Arquivo', value: 'filename' },
        { text: 'Status do Processamento', value: 'status' },
        { text: 'Status do Pagamento', value: 'statusPago' },
        { text: 'Valor', value: 'cost' },
        { text: 'Data de Upload', value: 'upload_date' },
        { text: 'Ações', value: 'actions', sortable: false }
      ]
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },

    // Upload de arquivo
    async uploadFile() {
      if (!this.selectedFile) {
        alert('Selecione um arquivo!');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        const response = await apiClient.post('/upload_file', formData);
        alert(response.data.message);
        this.fetchUploadedFiles();
      } catch (error) {
        console.error('Erro ao fazer upload:', error);
      }
    },

    // Buscar histórico de uploads
    async fetchUploadedFiles() {
      try {
        const response = await apiClient.get('/files');
        this.files = response.data.files;
      } catch (error) {
        console.error('Erro ao buscar arquivos:', error);
      }
    },

    // Gerar PIX para pagamento
    async generatePix(fileId) {
      try {
        const response = await apiClient.post(`/generate_pix/${fileId}`);
        const qrCode = response.data.qr_code;
        const fileIndex = this.files.findIndex(file => file.id === fileId);
        if (fileIndex !== -1) {
          this.$set(this.files[fileIndex], 'qr_code', qrCode);
        }
        alert('PIX gerado com sucesso!');
      } catch (error) {
        console.error('Erro ao gerar PIX:', error);
      }
    }
  },
  mounted() {
    this.fetchUploadedFiles();
  }
};
</script>

<style scoped>
.table {
  width: 100%;
  align-self: center;
}
</style
