<template>
  <v-container>
    <v-card class="mx-auto" max-width="600">
      <v-card-title>Atualizar Perfil</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateProfile">
          <v-text-field
              label="Email"
              v-model="email"
              :rules="[rules.required]"
          ></v-text-field>
          <v-file-input label="Foto de Perfil" v-model="profilePic"></v-file-input>
          <v-btn type="submit" color="primary">Atualizar Perfil</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      email: '', // Carregar o email do usuário aqui
      profilePic: null,
      rules: {
        required: value => !!value || 'Este campo é obrigatório.',
      },
    };
  },
  methods: {
    updateProfile() {
      // Lógica para atualizar o perfil do usuário
    },
  },
};
</script>
