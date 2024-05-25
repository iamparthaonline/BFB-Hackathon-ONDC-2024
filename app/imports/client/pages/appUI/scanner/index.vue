<template>
  <app-wrapper>
    <div class="product-packaging-scanner-container">
      <nav-back />
      <h1>Scan and Validate Your Product Packaging</h1>
      <div v-if="status === 'INITIAL'">
        <p class="description">
          Simply upload your product packaging photos to get insights on how does they fit with legal and compliance
          side of the world
        </p>
        <ul>
          <li>
            <strong>Ensure Good Lighting:</strong>
            Make sure the image is taken in well-lit conditions to enhance the readability and accuracy of text and
            details on the product's backside.
          </li>
          <li>
            <strong>High Resolution:</strong>
            Use a high-resolution camera setting to capture the image.
          </li>
          <li>
            <strong>No Obstructions:</strong>
            Ensure that nothing is covering any part of the product's backside. Hands, fingers, or other objects should
            not obstruct the view of the label.
          </li>
        </ul>
        <div class="actions">
          <div class="action-item" @click="process" v-ripple>
            <div class="action-img"><img src="/photo.png" /></div>

            <h2>Upload Image</h2>
            <p>Upload a photo from your device</p>
          </div>
          <div class="action-item" v-ripple>
            <div class="action-img"><img src="/camera.png" /></div>
            <h2>Open Camera</h2>
            <p>Click and upload a picture from camera</p>
          </div>
        </div>
      </div>
      <div v-else-if="status === 'LOADING' || status === 'SUCCESS' || status === 'REPORT'" class="scanning-image">
        <img
          src="/test.webp"
          :class="`uploaded-img ${status === 'LOADING' || status === 'SUCCESS' ? '' : 'success-report'}`"
          alt=""
        />
        <div v-if="status === 'REPORT'" class="report-paragraph">
          <h3>Report for your packaging</h3>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
            dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex
            ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat
            nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit
            anim id est laborum.
          </p>
          <v-btn block @click="status = 'INITIAL'" class="mt-3" outlined color="#4b06ba">Check another</v-btn>
        </div>
        <v-overlay v-if="status === 'LOADING' || status === 'SUCCESS'">
          <div class="loader-container" v-if="status === 'LOADING'">
            <h2>Please wait</h2>
            <img src="/search.gif" class="loader" alt="" />
            <p>
              Processing your image.
              <br />
              Note: Currently we are only processing food and electronics product
            </p>
          </div>
          <div class="loader-container" v-else>
            <h2>Processing complete</h2>
            <img src="/verified.gif" class="loader" alt="" />
            <p>Completed the scanning and processing of your packaging image</p>
          </div>
        </v-overlay>
      </div>
      <div v-else>
        <h4>
          Umm...
          <br />
          something went wrong. Please try again.
        </h4>
        <v-btn block @click="status = 'INITIAL'" class="mb-3" outlined color="#4b06ba">Try Again</v-btn>
        <h3>Please consider below things before uploading a packaging image,</h3>
        <ul>
          <li>
            <strong>Ensure Good Lighting:</strong>
            Make sure the image is taken in well-lit conditions to enhance the readability and accuracy of text and
            details on the product's backside.
          </li>
          <li>
            <strong>High Resolution:</strong>
            Use a high-resolution camera setting to capture the image.
          </li>
          <li>
            <strong>No Obstructions:</strong>
            Ensure that nothing is covering any part of the product's backside. Hands, fingers, or other objects should
            not obstruct the view of the label.
          </li>
        </ul>
      </div>
    </div>
  </app-wrapper>
</template>

<script>
  import appWrapper from '../../../components/appWrapper.vue';
  import navBack from '../../../components/navBack.vue';

  export default {
    components: {appWrapper, navBack},
    data() {
      return {
        status: 'INITIAL', // LOADING || SUCCESS
      };
    },
    methods: {
      process() {
        this.status = 'LOADING';
        setTimeout(() => {
          this.status = 'SUCCESS';
        }, 3000);
        setTimeout(() => {
          this.status = 'REPORT';
        }, 6000);
      },
    },
  };
</script>

<style lang="scss" scoped>
  .product-packaging-scanner-container {
    .scanning-image {
      text-align: center;
      margin: 20px 0;
      position: relative;
      .report-paragraph {
        background: #fff;
        padding: 16px;
        border-radius: 12px;
        font-size: 16px;
        display: block;
        text-align: left;
        font-weight: 400;
        @media only screen and (min-width: 600px) {
          p {
            font-size: 16px;
          }
        }
        h3 {
          margin-top: 0;
        }
      }
      .uploaded-img {
        width: 300px;
        height: 400px;
        border-radius: 12px;
        object-fit: cover;
      }
      .success-report {
        width: 200px;
        height: 200px;
        position: absolute;
        opacity: 0.1;
        display: flex;
        align-self: center;
        bottom: 20px;
        right: 20px;
        filter: grayscale(1);
      }
      .loader-container {
        padding: 20px;
        background-color: #fff;
        border-radius: 12px;
        width: 300px;
        p,
        h2 {
          color: #444;
        }
        p {
          font-size: 12px;
        }
        .loader {
          width: 100px;
          height: 100px;
          object-fit: cover;
        }
      }
    }
    .description {
      font-size: 14px;
      margin: 16px 0;
    }
    ul {
      margin: 20px 0;
      font-size: 12px;
    }
    h3,
    h4 {
      margin: 20px 0;
    }
    .actions {
      display: flex;
      gap: 16px;
      align-items: center;
      margin: 24px 0;

      .action-item {
        background: #fff;
        border-radius: 12px;
        padding: 16px;
        cursor: pointer;
        min-width: 135px;
        box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
        &:hover {
          box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
        }
        h2 {
          font-size: 16px;
        }
        .action-img {
          padding: 10px;
          background-color: #e1e0fd;
          border-radius: 50%;
          display: inline-flex;
          align-items: center;
          justify-content: space-around;
          margin-bottom: 14px;
          img {
            width: 24px;
            height: 24px;
          }
        }
      }
    }
  }
</style>
