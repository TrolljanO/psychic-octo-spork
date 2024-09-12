<template>
  <div class="limpa-pasta">
    <h1>Limpa Pasta</h1>

    <!-- Upload de Arquivo -->
    <section>
      <h3>Upload de Arquivo ZIP</h3>
      <form @submit.prevent="uploadFile">
        <input type="file" @change="onFileChange" />
        <button type="submit">Enviar</button>
      </form>
    </section>

    <!-- Histórico de Uploads -->
    <section>
      <h3>Histórico de Uploads</h3>
      <table>
        <thead>
        <tr>
          <th>Nome do Arquivo</th>
          <th>Status do Processamento</th>
          <th>Status do Pagamento</th>
          <th>Valor</th>
          <th>Data de Upload</th>
          <th>Ação</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="file in files" :key="file.id">
          <td>{{ file.filename }}</td>
          <td>{{ file.status }}</td>
          <td>{{ file.statusPago ? 'Pago' : 'Aguardando Pagamento' }}</td>
          <td>{{ file.cost }}</td>
          <td>{{ file.upload_date }}</td>
          <td>
            <!-- Renderiza o botão para gerar PIX se o pagamento não foi feito -->
            <button v-if="!file.statusPago" @click="generatePix(file.id)">
              Gerar PIX
            </button>

            <!-- Exibe o QR code se já foi gerado -->
            <img v-if="file.qr_code" :src="file.qr_code" alt="QR Code" />
          </td>
        </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      files: [] // Armazena o histórico de arquivos
    };
  },
  methods: {
    // Quando o arquivo é selecionado
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },

    // Função de upload de arquivo
    async uploadFile() {
      if (!this.selectedFile) {
        alert('Selecione um arquivo!');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        const response = await axios.post('http://localhost:5000/upload_file', formData, {
          withCredentials: true
        });
        alert(response.data.message);

        // Atualizar o histórico após o upload
        this.fetchUploadedFiles();
      } catch (error) {
        console.error('Erro ao fazer upload:', error);
      }
    },

    // Busca o histórico de uploads do usuário
    async fetchUploadedFiles() {
      try {
        const response = await axios.get('http://localhost:5000/files', {
          withCredentials: true
        });
        this.files = response.data.files;
      } catch (error) {
        console.error('Erro ao buscar arquivos:', error);
      }
    },

    // Função para gerar PIX
    async generatePix(fileId) {
      try {
        const response = await axios.post(`http://localhost:5000/generate_pix/${fileId}`, {
          withCredentials: true
        });

        // Atualiza o arquivo no array com o QR code gerado
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
    this.fetchUploadedFiles(); // Carrega o histórico ao montar o componente
  }
};
</script>

<style scoped>
.table {
  width: 100%;
  align-self: center;
}
</style>
