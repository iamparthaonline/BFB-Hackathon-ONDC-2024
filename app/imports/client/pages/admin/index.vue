<template>
  <div>
    <input type="text" placeholder="Enter Url" v-model="url" />
    <v-btn @click="saveToDB">Save</v-btn>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        url: undefined,
      };
    },
    methods: {
      saveToDB() {
        if (this.url)
          Meteor.call('saveUrl', this.url, (err, res) => {
            console.log(err, res);
          });
      },
    },
  };
</script>

<style></style>
