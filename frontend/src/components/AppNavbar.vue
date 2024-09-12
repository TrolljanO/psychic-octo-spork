<template>
  <nav class="navbar navbar-mainbg">
    <div class="container-fluid">
      <a class="navbar-logo" href="#">FlowBoost.TECH</a>
      <div class="navbar-links">
        <router-link class="nav-link" to="/">Início</router-link>
        <router-link class="nav-link" to="/Profile">Perfil</router-link>
        <router-link class="nav-link" to="/Finance">Financeiro</router-link>
      </div>
      <div class="navbar-right">
        <span class="balance">Saldo: R$ {{ balance }}</span>
        <div class="dropdown">
          <a href="#" @click.prevent="toggleDropdown" class="nav-link dropdown-toggle">
            <img :src="user.profile_pic" class="profile-pic" alt="Profile" />
          </a>
          <ul class="dropdown-menu" v-if="dropdownOpen">
            <li class="dropdown-item">
              <router-link to="/Profile">Perfil</router-link>
            </li>
            <li class="dropdown-item">
              <router-link to="/Logout">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';
export default {
  name: 'AppNavbar',
  data() {
    return {
      dropdownOpen: false,
      balance: 0,  // Inicializa com 0 até que os dados do servidor sejam recebidos
      user: {
        profile_pic: "https://robohash.org/mail@ashallendesign.co.uk" // Placeholder ou URL real
      }
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    async fetchUserData() {
      try {
        // Obtém o token JWT do armazenamento local (localStorage ou sessionStorage)
        const token = localStorage.getItem('jwt_token'); // ou sessionStorage.getItem('jwt_token')

        // Verifica se o token existe
        if (!token) {
          console.error('Token JWT não encontrado');
          return;
        }

        // Faz a requisição para a API com o token JWT no cabeçalho
        const response = await axios.get('http://localhost:5000/api/limpa-pasta', {
          headers: {
            Authorization: `Bearer ${token}`  // Envia o token JWT
          },
          withCredentials: true
        });

        this.balance = response.data.credits;  // Atualiza o saldo com a resposta da API
      } catch (error) {
        console.error('Erro ao buscar os dados do usuário:', error);
      }
    }
  },
  mounted() {
    // Chama a função para buscar os dados do usuário ao montar o componente
    this.fetchUserData();
  }
};
</script>

<style scoped>
/* Navbar Principal */
.navbar-mainbg {
  background-color: rgba(33, 0, 93, 0.57); /* Translucidez */
  box-shadow: 0 4px 8px -2px rgba(0, 0, 0, 0.6); /* Sombra 3D */
  padding: 10px 30px;
  border-radius: 0 0 20px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 10;
  backdrop-filter: blur(10px); /* Efeito de desfoque */
}

.container-fluid {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.navbar-logo {
  color: #fff;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 20px; /* Ajuste de tamanho de fonte */
}

.navbar-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: #fff;
  font-size: 16px; /* Ajuste de tamanho de fonte */
  padding: 10px 15px;
  cursor: pointer;
  text-decoration: none;
  transition: background-color 0.3s, color 0.3s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}

/* Ajuste da Navbar Direita */
.navbar-right {
  display: flex;
  align-items: center;
  gap: 10px; /* Espaçamento entre saldo e imagem de perfil */
  margin-left: auto; /* Força o alinhamento à direita */
  padding-right: 20px; /* Garante que os elementos fiquem longe da borda direita */
}

.balance {
  color: white;
  font-weight: bold;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  object-fit: cover; /* Garante que a imagem fique bem dentro do contêiner */
}

/* Ajuste para o Dropdown */
.dropdown {
  position: relative; /* Faz o dropdown ficar no fluxo do layout */
}

.dropdown-menu {
  background-color: rgba(33, 0, 93, 0.95); /* Restaurando o fundo mais escuro */
  position: absolute;
  top: 100%; /* Coloca o dropdown abaixo da imagem */
  right: 0; /* Alinha o dropdown à direita */
  list-style: none;
  padding: 10px 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  z-index: 1; /* Garante que o dropdown fique acima de outros elementos */
}

.dropdown-item {
  color: white;
  cursor: pointer;
  padding: 5px 0;
  text-decoration: none;
}

.dropdown-item:hover {
  color: #ffc107; /* Efeito hover restaurado */
}

.dropdown-toggle {
  color: white;
  text-decoration: none;
  cursor: pointer;
}

@media (max-width: 991px) {
  .navbar-logo {
    font-size: 16px; /* Ajuste de tamanho de fonte para telas menores */
  }

  .nav-link {
    font-size: 14px; /* Ajuste de tamanho de fonte para telas menores */
    padding: 8px 10px;
  }

  .dropdown-menu {
    right: 0; /* Garante que o dropdown esteja sempre alinhado à direita */
    transform: translateX(0); /* Evita que o dropdown seja cortado em telas menores */
  }
}
</style>