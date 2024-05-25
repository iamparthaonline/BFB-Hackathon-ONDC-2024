<template>
  <app-wrapper>
    <div class="product-packaging-scanner-container">
      <nav-back />
      <h1>Ask your questions</h1>
      <div v-if="status === 'INITIAL'">
        <p class="description">
          Ask any questions about the legal and compliance of your business.
          <br />
          E.g. "i want to sell ice creams online on ecommerce platform, what regulations do I have to follow"
        </p>

        <div class="actions">
          <div :class="`action-item ${tab === 'WRITE' ? 'active' : ''}`" @click="changeTab('WRITE')" v-ripple>
            <div class="action-img"><img src="/keyboard.png" /></div>
            <h2>I want to write</h2>
          </div>
          <div :class="`action-item ${tab === 'TALK' ? 'active' : ''}`" @click="changeTab('TALK')" v-ripple>
            <div class="action-img"><img src="/microphone.png" /></div>
            <h2>I want to talk</h2>
          </div>
        </div>
        <div v-if="tab === 'WRITE'" class="write-container">
          <h2>Write your query in your language</h2>

          <validation-observer ref="observer" v-slot="{invalid}">
            <form @submit.prevent="submit" class="mt-4">
              <validation-provider v-slot="{errors}" name="Query" rules="required|max:200">
                <v-textarea
                  filled
                  auto-grow
                  v-model="name"
                  outlined
                  :counter="200"
                  :error-messages="errors"
                  label="Enter your query"
                  required
                ></v-textarea>
                <v-select class="mt-3" :items="['hindi', 'bengali']" label="Language" outlined></v-select>
              </validation-provider>
              <div class="text-center mt-2">
                <v-btn
                  block
                  class="mr-4"
                  type="submit"
                  color="#7930f0"
                  :loading="loading"
                  :disabled="invalid || loading"
                >
                  Submit
                </v-btn>
                <!-- <v-btn @click="clear" :disabled="loading" color="#ccc">Clear</v-btn> -->
              </div>
            </form>
          </validation-observer>
        </div>
        <div v-else-if="tab === 'TALK'" class="write-container talk-container">
          <h2>Speak your query in your language</h2>
          <div class="recorder-wrapper">
            <div class="recorder-time-action">
              <div class="recorder-time">00:00</div>
              <v-btn
                block
                class="mr-4"
                type="submit"
                color="red"
                :loading="loading"
                :disabled="recording !== 'RECORDING'"
              >
                Cancel
              </v-btn>
            </div>
            <div v-ripple class="record-action" v-if="recording === 'INITIAL'">
              <img src="/start-record.png" alt="" />
              <span>Start Recording</span>
            </div>
            <div v-ripple class="record-action" v-else-if="recording === 'RECORDING'">
              <img src="/stop-record.png" alt="" />
              <span>Stop Recording</span>
            </div>
          </div>
          <v-select class="mt-3" :items="['hindi', 'bengali']" label="Language" outlined></v-select>
          <v-btn block class="mr-4" type="submit" color="#7930f0" :loading="loading" :disabled="invalid || loading">
            Submit
          </v-btn>
        </div>
      </div>
      <div v-else-if="status === 'LOADING' || status === 'SUCCESS' || status === 'REPORT'" class="scanning-image">
        <div class="original-query mb-3">
          <h2>Your Query</h2>
          <figure class="my-2">
            <figcaption>Listen to your query</figcaption>
            <audio controls src="/media/cc0-audio/t-rex-roar.mp3"></audio>
          </figure>

          <p>"{{ name }}"</p>
        </div>
        <div v-if="status === 'REPORT'" class="report-paragraph">
          <v-alert v-if="timeTaken && !loading" dense text type="success">
            Processed your query in
            <strong>{{ parseFloat(timeTaken, 2) }} seconds</strong>
          </v-alert>

          <results v-if="response" :aiResponse="aiResponse" :semanticSearchResponse="semanticSearchResponse"></results>

          <v-btn block @click="status = 'INITIAL'" class="mt-3" outlined color="#4b06ba">Check another</v-btn>
        </div>
        <v-overlay v-if="status === 'LOADING' || status === 'SUCCESS'">
          <div class="loader-container" v-if="status === 'LOADING'">
            <h2>Please wait</h2>
            <img src="/ai.gif" class="loader" alt="" />
            <p>
              Processing your query.
              <br />
              Note: Currently we are only processing food and electronics categories
            </p>
          </div>
          <div class="loader-container" v-else>
            <h2>Processing complete</h2>
            <img src="/verified.gif" class="loader" alt="" />
            <p>Successfully completed processing your query.</p>
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
      </div>
    </div>
    <p class="my-3">
      Multi language Support added via
      <a href="https://bhashini.gov.in/">Bhashini</a>
    </p>
  </app-wrapper>
</template>

<script>
  import {required, digits, max} from 'vee-validate/dist/rules';
  import {extend, ValidationObserver, ValidationProvider, setInteractionMode} from 'vee-validate';
  import appWrapper from '../../../components/appWrapper.vue';
  import navBack from '../../../components/navBack.vue';
  import results from '../../home/results.vue';

  setInteractionMode('eager');

  extend('digits', {
    ...digits,
    message: '{_field_} needs to be {length} digits. ({_value_})',
  });

  extend('required', {
    ...required,
    message: '{_field_} can not be empty',
  });

  extend('max', {
    ...max,
    message: '{_field_} may not be greater than {length} characters',
  });

  export default {
    components: {
      ValidationProvider,
      ValidationObserver,
      appWrapper,
      navBack,
      results,
    },
    props: {},
    data: () => ({
      name: '',
      status: 'INITIAL', // LOADING || SUCCESS
      tab: 'WRITE',
      recording: 'INITIAL', // RECORDING || PROCESSING
      timeTaken: Number,
      response: false,
      semanticSearchResponse: '',
      aiResponse: '',
    }),

    methods: {
      submit() {
        this.$refs.observer.validate();
        this.searchQuery(this.name);
      },
      clear() {
        this.name = '';
        this.$refs.observer.reset();
      },
      changeTab(tab) {
        this.tab = tab;
      },
      async searchQuery(queryText) {
        this.status = 'LOADING';
        this.semanticSearchResponse = '';
        this.aiResponse = '';
        this.response = false;
        const startTime = +new Date();
        const response = await fetch(`${Meteor.settings.public.API_HOST}/generate-AI-response`, {
          method: 'POST',
          cache: 'no-cache',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({queryText, k: 25}),
        });

        this.aiResponse = await response.json();
        const semanticSearch = await fetch(
          `${Meteor.settings.public.API_HOST}/semantic-search?query=${queryText}&k=25`,
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
        this.status = 'REPORT';

        this.response = true;
        this.timeTaken = (+new Date() - startTime) / 1000;
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
        padding: 8px 16px;
        cursor: pointer;
        box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
        &:hover {
          box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
        }
        display: flex;
        align-items: center;
        gap: 8px;
        h2 {
          font-size: 12px;
          margin: 0;
        }
        .action-img {
          padding: 10px;
          background-color: #e1e0fd;
          border-radius: 50%;
          display: inline-flex;
          align-items: center;
          justify-content: space-around;
          img {
            width: 16px;
            height: 16px;
          }
        }

        &.active {
          background-color: #7930f0;
          h2 {
            color: #fff;
          }
          .action-img {
            background-color: #fff;
          }
        }
      }
    }
    .write-container {
      background-color: #fff;
      .v-input .v-label {
        color: #7930f0;
      }
      h2 {
        color: #444;
        text-align: center;
        margin: 16px 0;
      }
      &.talk-container {
        text-align: center;
        .recorder-wrapper {
          display: flex;
          align-items: center;
          justify-content: space-around;
        }
        .recorder-time {
          font-size: 24px;
          font-family: courier;
          margin: 20px 0;
          padding: 0 40px;
        }
        .record-action {
          display: flex;
          align-items: center;
          flex-direction: column;
          background: #e1e0fd;
          display: inline-flex;
          border-radius: 12px;
          padding: 12px;
          gap: 12px;
          margin: 20px 0;
          img {
            width: 40px;
          }
          span {
            color: #7930f0;
            font-weight: bold;
          }
        }
      }
      border-radius: 12px;
      padding: 8px 16px;
      box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
      button {
        color: #fff;
      }
    }
    .original-query {
      background-color: #fff;
      border-radius: 12px;
      padding: 24px;
      p {
        font-size: 16px;
      }
    }
  }
</style>
