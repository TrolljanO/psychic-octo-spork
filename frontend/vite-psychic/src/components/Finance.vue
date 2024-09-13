<template>
  <div class="finance-container">

    <h2 class="title2">Gestão Financeira</h2>

    <!-- Container para Adicionar Créditos -->
    <div class="card credits-container mb-4">
      <div class="card-header">Adicionar Créditos</div>
      <div class="card-body">
        <form @submit.prevent="generatePix">
          <div class="form-group">
            <label for="amount">Valor (R$):</label>
            <input v-model="amount" type="text" id="amount" size="2" class="form-control" required />
          </div>
          <button type="submit" class="btn btn-primary">Recarregar Créditos</button>
        </form>
        <img v-if="qrCode" :src="qrCode" id="qr-code" style="width: 350px; height: 350px;" alt="QR Code" />
        <p v-if="paymentStatus">{{ paymentStatus }}</p>
      </div>
    </div>

    <!-- Container para o Histórico de Transações -->
    <div class="card transactions-container">
      <div class="card-header">Histórico de Transações</div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-bordered">
            <thead>
            <tr>
              <th>Data</th>
              <th>Descrição</th>
              <th>Quantia</th>
              <th>Status</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="transaction in transactions" :key="transaction.id">
              <td>{{ transaction.timestamp }}</td>
              <td>{{ transaction.description }}</td>
              <td>{{ transaction.amount }}</td>
              <td>{{ transaction.status }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FinancePage',
  data() {
    return {
      user: {
        profilePic: 'https://robohash.org/mail@ashallendesign.co.uk', // Placeholder ou URL real
      },
      amount: '',
      qrCode: null, // Para armazenar o QR code gerado
      paymentStatus: '',
      transactions: [], // Histórico de transações
    };
  },
  methods: {
    // Gera o QR Code para pagamento via PIX
    async generatePix() {
      try {
        const response = await axios.post('http://localhost:5000/generate_pix', {
          amount: this.amount,
        }, {withCredentials: true});

        this.qrCode = response.data.qr_code;
        this.paymentStatus = 'Aguardando pagamento...';
      } catch (error) {
        console.error('Erro ao gerar PIX:', error);
      }
    },
    // Busca o histórico de transações do usuário
    async fetchTransactions() {
      try {
        const response = await axios.get('http://localhost:5000/api/finance', {withCredentials: true});
        this.transactions = response.data.transactions;
      } catch (error) {
        console.error('Erro ao buscar transações:', error);
      }
    },
  },
  mounted() {
    // Carrega o histórico de transações quando o componente é montado
    this.fetchTransactions();
  },
};
</script>

<style scoped>
.finance-container {
  margin-top: 30px;
  padding: 20px;
}

/* Estilo do container de adicionar créditos */
.credits-container {
  background-color: #f9f9f9;
  padding: 20px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 20px;
}

.credits-container .form-group label {
  font-weight: bold;
}

#qr-code {
  margin-top: 20px;
}

.transactions-container {
  margin-top: 20px;
  background-color: #ffffff;
  padding: 20px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.transactions-container .table {
  margin-top: 20px;
}

.profile-pic {
  border-radius: 50%;
  cursor: pointer;
}

/* Ajustes adicionais para o layout responsivo */
@media (max-width: 768px) {
  .finance-container {
    padding: 10px;
  }

  .credits-container, .transactions-container {
    padding: 10px;
  }
}
</style>
