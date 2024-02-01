<template>
  <div class="search-input-container">
    <div class="mb-4">
      <validation-observer ref="observer" v-slot="{invalid}">
        <form @submit.prevent="submit">
          <validation-provider v-slot="{errors}" name="Name" rules="required|max:200">
            <v-text-field v-model="name" :counter="200" :error-messages="errors" label="Name" required></v-text-field>
          </validation-provider>
          <div class="text-right mt-4">
            <v-btn class="mr-4" type="submit" color="primary" :loading="loading" :disabled="invalid || loading">
              Submit
            </v-btn>
            <v-btn @click="clear" :disabled="loading">Clear</v-btn>
          </div>
        </form>
      </validation-observer>
    </div>

    <v-alert v-if="timeTaken" dense text type="success">
      Processed your query in
      <strong>{{ parseFloat(timeTaken, 2) }} seconds</strong>
    </v-alert>
  </div>
</template>

<script>
  import {required, digits, max} from 'vee-validate/dist/rules';
  import {extend, ValidationObserver, ValidationProvider, setInteractionMode} from 'vee-validate';

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
    },
    props: {
      loading: Boolean,
      timeTaken: Number,
    },
    data: () => ({
      name: '',
    }),

    methods: {
      submit() {
        this.$refs.observer.validate();
        this.$emit('submit-form', this.name);
      },
      clear() {
        this.name = '';
        this.$refs.observer.reset();
      },
    },
  };
</script>

<style>
  .search-input-container {
    margin-top: 50px;
  }
</style>
