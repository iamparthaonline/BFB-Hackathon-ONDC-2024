<template>
  <app-wrapper>
    <div class="dashboard-container">
      <h1 id="heading"></h1>
      <ul class="meta-list">
        <li>✓ Easily check for any legal queries of your business</li>
        <li>✓ Quick and fast responses</li>
        <li>✓ Trained models on real compliance documents</li>
        <li>✓ Available in multiple languages</li>
        <li>✓ Scan and get feedback on your product packaging</li>
      </ul>
      <div class="feature-item" v-ripple @click="goToPage('query')">
        <img src="/animated/question.gif" alt="" />
        <div>
          <h2>Ask any questions</h2>
          <p>Get answer to any legal or compliance related query for your business</p>
        </div>
      </div>

      <div class="feature-item" v-ripple @click="goToPage('product-packaging-scanner')">
        <img src="/animated/scanning.gif" alt="" />
        <div>
          <h2>Scan product packages</h2>
          <p>Check if your product packaging is compliant ready, get feedbacks</p>
        </div>
      </div>

      <div v-if="isWeb" v-ripple class="download-app">Download Android App</div>
    </div>
  </app-wrapper>
</template>

<script>
  import appWrapper from '../../../components/appWrapper.vue';

  export default {
    components: {appWrapper},
    data() {
      return {
        heading: 'da',
        isWeb: !Meteor.isCordova,
      };
    },
    mounted: () => {
      const actualHeading = 'Get Legally Complaint in India Easily';
      let i = 0;
      const speed = 50; /* The speed/duration of the effect in milliseconds */

      const typeWriter = () => {
        if (i < actualHeading.length) {
          document.getElementById('heading').innerHTML += actualHeading.charAt(i);
          i += 1;
          setTimeout(typeWriter, speed);
        }
      };
      typeWriter();
    },
    methods: {
      goToPage(path) {
        setTimeout(() => {
          this.$router.push({path});
        }, 300);
      },
    },
  };
</script>

<style lang="scss" scoped>
  .dashboard-container {
    height: 100vh;
    .download-app {
      background-color: #7930f0;
      color: #fff;
      cursor: pointer;
      padding: 12px;
      border-radius: 10px;
      text-transform: uppercase;
      text-align: center;
      font-weight: 500;
      font-size: 14px;
      margin-bottom: 14px;
      &:hover {
        background-color: #4b06ba;
      }
    }
    h1 {
      min-height: 78px;
    }
  }
  .meta-list {
    list-style: none;
    margin-left: 0;
    padding-left: 1em;
    text-indent: -1em;
    margin: 20px 0;
  }

  .feature-item {
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding: 10px 16px;
    border-radius: 10px;
    margin-bottom: 20px;
    cursor: pointer;
    box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
    &:hover {
      box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    }

    img {
      width: 50px;
      margin-right: 16px;
    }
  }
</style>
