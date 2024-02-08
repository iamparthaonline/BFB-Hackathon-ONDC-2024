<template>
  <v-card class="mx-auto" width="100%" :class="{active: isActive}">
    <v-card-text>
      <div class="flex flex-row">
        <v-progress-linear v-model="showScore" height="20" color="green" rounded readonly>
          <strong>{{ showScore }}% Match</strong>
        </v-progress-linear>
      </div>
      <div class="text--primary my-8">{{ result.page_content.substring(0, 300) }}...</div>
      <div class="text--primary">source: {{ result.source }}#page={{ result.source_page_number + 1 }}</div>
    </v-card-text>
    <v-card-actions>
      <v-btn text color="teal accent-4" @click="reveal = true">Read More</v-btn>
      <v-btn text color="teal accent-4" @click="openSource"><v-icon>mdi-open-in-new</v-icon></v-btn>
    </v-card-actions>
    <v-expand-transition>
      <v-card v-if="reveal" class="transition-fast-in-fast-out v-card--reveal overflow-auto" style="height: 100%">
        <v-card-text class="pb-0">
          <p class="text-h4 text--primary">Full Text</p>
          <p>
            {{ result.page_content }}
          </p>
        </v-card-text>
        <v-card-actions class="pt-0">
          <v-btn text color="teal accent-4" @click="reveal = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-expand-transition>
    <modalPdfViewer
      :showModal="showModal"
      @closeModal="closeModal"
      :source="fileName"
      :pageNumber="result.source_page_number + 1"
    />
  </v-card>
</template>

<script>
  import modalPdfViewer from './modalPdfViewer.vue';

  export default {
    data: () => ({
      reveal: false,
      showModal: false,
      hasError: true,
      fileName: null,
    }),
    props: {
      result: Object,
      idx: Number,
      sourceIdx: Number,
    },
    components: {
      modalPdfViewer,
    },
    mounted() {
      const parts = this.result.source.split('/');
      this.fileName = parts[parts.length - 1];
      if (this.idx === 0) this.openPdfInSide();
    },
    computed: {
      showScore() {
        return ((1 - this.result.similarity_score) * 100).toFixed(1);
      },
      isActive() {
        if (this.idx === this.sourceIdx && window.innerWidth > 960) return true;
        return false;
      },
    },
    methods: {
      openPdfInSide() {
        this.$emit('openPdfViewer', {
          source: this.fileName,
          pageNumber: this.result.source_page_number + 1,
          sourceIdx: this.idx,
        });
      },
      openSource() {
        this.openPdfInSide();
        if (window.innerWidth <= 960) this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
      },
    },
  };
</script>

<style lang="scss" scoped>
  .v-card {
    transition: all 0.2s ease-in;
    &.active {
      outline: 1px solid black;
      transform: translateX(15px);
    }
  }
  .v-card--reveal {
    bottom: 0;
    opacity: 1 !important;
    position: absolute;
    width: 100%;
  }
  .similarityScore {
    padding: 2px 8px;
    width: fit-content;
  }
</style>
