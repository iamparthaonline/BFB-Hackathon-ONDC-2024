<template>
  <v-dialog v-model="dialog" persistent width="600px" height="100%">
    <v-card>
      <pdfviewer :source="source" :pageNumber="pageNumber" />
      <v-icon class="close-btn" color="green darken-1" @click="$emit('closeModal')">mdi-close</v-icon>
    </v-card>
  </v-dialog>
</template>

<script>
  import pdfviewer from './pdfViewer.vue';

  export default {
    name: 'ModalPdfViewer',
    data() {
      return {
        dialog: false,
      };
    },
    props: {
      showModal: Boolean,
      source: String,
      pageNumber: Number,
    },
    components: {
      pdfviewer,
    },
    watch: {
      showModal() {
        this.dialog = this.showModal;
      },
    },
  };
</script>

<style lang="scss" scoped>
  .close-btn {
    padding: 16px;
    position: absolute;
    top: 0;
    right: 0;
  }
</style>
