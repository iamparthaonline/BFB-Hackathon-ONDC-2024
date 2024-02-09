<template>
  <div class="mt-4 main-container">
    <v-tabs color="deep-purple accent-4" left>
      <v-tab>AI Response</v-tab>
      <v-tab>Knowledge bank</v-tab>
      <v-tab>Others</v-tab>
      <v-tab-item>
        <div v-if="aiResponse" class="response">
          <p class="my-4">{{ aiResponse }}</p>
          <p class="my-4">For more information check out the Knowledge bank,</p>
        </div>
      </v-tab-item>
      <v-tab-item>
        <div class="results-list d-flex flex-row">
          <v-container class="" width="400">
            <div class="d-flex flex-row flex-wrap">
              <result-card-vue
                v-for="(result, idx) in semanticSearchResponse"
                :key="idx"
                :idx="idx"
                left
                class="mb-4"
                :result="result.document"
                :sourceIdx="sourceIdx"
                @openPdfViewer="openPdfViewer"
              />
            </div>
          </v-container>
          <v-container v-if="source" class="pdf-container d-none d-sm-none d-md-block flex-grow" fluid>
            <pdfviewer :source="source" :pageNumber="pageNumber" :sourceIdx="sourceIdx" class="child" />
          </v-container>
        </div>
      </v-tab-item>
    </v-tabs>
  </div>
</template>

<script>
  import resultCardVue from './resultCard.vue';
  import pdfviewer from './pdfViewer.vue';

  export default {
    name: 'Results',
    props: {
      aiResponse: String,
      semanticSearchResponse: Array,
    },
    data() {
      return {
        source: null,
        pageNumber: null,
        sourceIdx: null,
        loading: false,
      };
    },
    components: {resultCardVue, pdfviewer},
    methods: {
      openPdfViewer({source, pageNumber, sourceIdx}) {
        this.pageNumber = pageNumber;
        this.sourceIdx = sourceIdx;
        this.source = source;
      },
    },
  };
</script>

<style scoped>
  .response {
    p {
      white-space: pre-line;
      text-wrap: wrap;
      text-align: justify;
    }
  }
  .results-list {
    height: calc(100dvh - 87px);
    overflow-y: auto;
    .pdf-container {
      max-height: fit-content;
      position: relative;
      position: sticky;
      top: 0px;
      .child {
        height: fit-content;
      }
    }
  }
</style>
