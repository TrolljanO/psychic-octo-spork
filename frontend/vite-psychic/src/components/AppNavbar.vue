<template>
  <v-app-bar app>
    <v-app-bar-nav-icon></v-app-bar-nav-icon>
    <v-toolbar-title>FlowBoost.TECH</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text to="/">Início</v-btn>
    <v-btn text to="/profile">Perfil</v-btn>
    <v-btn text @click="logout">Logout</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: 'AppNavbar',
  methods: {
    logout() {
      // Lógica para logout
      apiClient.post('/logout').then(() => {
        this.$router.push('/login');  // Redireciona para a página de login após o logout
      });
    }
  }
};
</script>
