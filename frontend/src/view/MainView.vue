<script setup>
import ServerData from "@/components/ServerData.vue";
import BucketData from "@/components/BucketData.vue";
</script>
<script>
export default {
  props: {
    data: null
  },
  data() {
    return {
      instance: null,
      bucket: null,
      request: 0.0,
      outbound: 0.0
    }
  },
  mounted() {
    if (this.data) {
      this.instance = this.data["instance"]
      let bucket = this.data["bucket"]
      this.request = bucket['request']
      this.outbound = bucket['outbound']
    }
  },
  updated() {
    this.instance = this.data["instance"]
    let bucket = this.data["bucket"]
    this.request = bucket['requests']
    this.outbound = bucket['outbound']
  }
}
</script>

<template>
  <md-divider/>
  <md-list>
    <ServerData v-for="server in instance" :data="server"/>
    <BucketData :request="request" :value="outbound"/>
  </md-list>
</template>

<style scoped>
md-list {
  height: 100%;
  padding: 0;
}
</style>