<template>
  <v-app>
    <v-main>
      <v-responsive height="100%">
        <router-view></router-view>
      </v-responsive>
    </v-main>
  </v-app>
</template>

<script>
  export default {};
</script>

<style lang="scss" scoped>
  .v-main {
    .v-responsive {
      overflow: auto;
    }
  }
</style>
