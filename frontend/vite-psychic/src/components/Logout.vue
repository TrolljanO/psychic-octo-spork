<template>
  <div>
    <p>Fazendo logout...</p>
  </div>
</template>

<script>
export default {
  name: 'UserLogout',  // Mude o nome do componente aqui
  mounted() {
    // Remove o token JWT do localStorage
    localStorage.removeItem('token');

    // Redirecionar para a página de login após logout
    setTimeout(() => {
      this.$router.push('/login');
    }, 1000);
  }
};
</script>
