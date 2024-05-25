<template>
  <iframe
    id="pdf-js-viewer"
    :src="`/pdfjs/web/viewer.html?file=${encodeURIComponent(mask())}`"
    title="webviewer"
    frameborder="0"
    ref="viewer"
  ></iframe>
</template>

<script>
  export default {
    props: {
      source: String,
      content: String,
    },
    methods: {
      mask() {
        return `${window.location.origin}/${this.source}`;
      },
      find() {
        this.$refs.viewer.addEventListener('load', () => {
          const iframeDocument = this.$refs.viewer.contentWindow;

          iframeDocument.PDFViewerApplication.eventBus.dispatch('find', {
            caseSensitive: false,
            findPrevious: undefined,
            highlightAll: true,
            phraseSearch: false,
            query: this.content,
          });
        });
      },
    },
    mounted() {
      this.find();
    },
  };
</script>

<style lang="scss" scoped>
  #pdf-js-viewer {
    height: 100%;
    width: 100%;
  }
</style>
