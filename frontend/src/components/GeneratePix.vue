<template>
  <div v-if="qrCode">
    <img :src="qrCode" alt="QR Code para pagamento PIX" />
  </div>
  <button @click="generatePix(fileId, cost)">
    Gerar PIX
  </button>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      qrCode: null,
    };
  },
  methods: {
    async generatePix(fileId, cost) {
      try {
        const response = await axios.post(`http://localhost:5000/generate_pix/${fileId}`, {
          withCredentials: true
        });
        this.qrCode = response.data.qr_code;  // Exibe o QR code gerado
      } catch (error) {
        console.error("Erro ao gerar o PIX:", error);
      }
    }
  }
};
</script>
