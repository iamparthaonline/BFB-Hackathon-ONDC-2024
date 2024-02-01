<template>
  <div class="page-container">
    <app-bar />
    <v-sheet id="app-sheet" class="overflow-y-auto" max-height="600">
      <v-container style="height: 150vh">
        <search-input-vue :loading="loading" @submit-form="searchQuery" :timeTaken="timeTaken" />
        <results v-if="response" :aiResponse="aiResponse"></results>
      </v-container>
    </v-sheet>
  </div>
</template>

<script>
  import results from './results.vue';
  import searchInputVue from './searchInput.vue';
  import appBar from '../../components/appBar.vue';

  export default {
    components: {results, searchInputVue, appBar},
    data() {
      return {loading: false, response: false, aiResponse: '', timeTaken: undefined};
    },
    methods: {
      async searchQuery(queryText) {
        this.loading = true;
        const startTime = +new Date();
        const response = await fetch(`${Meteor.settings.public.API_HOST}generate-AI-response`, {
          method: 'POST', // *GET, POST, PUT, DELETE, etc.
          cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({queryText, k: 25}), // body data type must match "Content-Type" header
        });

        this.aiResponse = await response.json();

        this.loading = false;
        this.response = true;
        this.timeTaken = (+new Date() - startTime) / 1000;
      },
    },
  };
</script>

<style lang="scss" scoped>
  .page-container {
    margin: 25px;
    padding-bottom: 50px;
  }
</style>
