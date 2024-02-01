<template>
  <div class="mt-4">
    <v-tabs color="deep-purple accent-4" left>
      <v-tab>AI Response</v-tab>
      <v-tab>Knowledge bank</v-tab>
      <v-tab>Others</v-tab>
      <v-tab-item>
        <div v-if="aiResponse">
          <p class="my-4">{{ aiResponse }}</p>
          <p class="my-4">For more information check out the related things,</p>
          <v-btn
            :loading="loading3"
            :disabled="loading3"
            color="blue-grey"
            class="ma-2 white--text"
            @click="loader = 'loading3'"
          >
            Knowledge Bank
            <v-icon right>arrow-right-circle-outline</v-icon>
          </v-btn>
        </div>
      </v-tab-item>
      <v-tab-item>
        <div class="results-list">
          <v-container fluid>
            <v-row>
              <v-col v-for="i in 6" :key="i" cols="12" md="3">
                <result-card-vue v-for="n in 3" :key="n" left class="mb-4" />
              </v-col>
            </v-row>
          </v-container>
        </div>
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script>
  import resultCardVue from './resultCard.vue';

  export default {
    name: 'Results',
    props: {
      aiResponse: String,
    },
    components: {resultCardVue},
  };
</script>

<style>
  .results-list {
    padding: 20px 0;
  }
</style>
