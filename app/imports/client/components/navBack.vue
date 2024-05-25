<template>
  <v-btn @click="$router.go(-1)" icon class="back-button">
    <v-icon>mdi-keyboard-backspace</v-icon>
  </v-btn>
</template>

<script>
  export default {};
</script>

<style>
  .back-button {
    margin: 20px 0;
    background: #fff;
  }
</style>
