<template>
  <div class="page-container">
    <v-container>
      <search-input-vue :loading="loading" @submit-form="searchQuery" :timeTaken="timeTaken" />
      <results v-if="response" :aiResponse="aiResponse" :semanticSearchResponse="semanticSearchResponse"></results>
    </v-container>
  </div>
</template>

<script>
  import results from './results.vue';
  import searchInputVue from './searchInput.vue';

  export default {
    components: {results, searchInputVue},
    data() {
      return {loading: false, response: false, semanticSearchResponse: '', aiResponse: '', timeTaken: undefined};
    },
    methods: {
      async searchQuery(queryText) {
        this.loading = true;
        const startTime = +new Date();
        const response = await fetch(`${Meteor.settings.public.API_HOST}generate-AI-response`, {
          method: 'POST',
          cache: 'no-cache',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({queryText, k: 25}),
        });

        this.aiResponse = await response.json();
        const semanticSearch = await fetch(
          `${Meteor.settings.public.API_HOST}semantic-search?query=${queryText}&k=25`,
          {
            method: 'POST',
            cache: 'no-cache',
            headers: {
              'Content-Type': 'application/json',
            },
          },
        );

        this.semanticSearchResponse = await semanticSearch.json();
        this.semanticSearchResponse.sort((a, b) => a.document.similarity_score - b.document.similarity_score);
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
  }
</style>
