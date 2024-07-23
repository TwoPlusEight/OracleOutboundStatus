<!--
账号名称与区域
-->
<script>
export default {
  props: {
    name: "",
    region: "",
    index: 0,
    value: 0.0,
    days: ""
  },
  methods:{
    formatBytes(bytes) {
      if (bytes === 0) return '0 GB';
      const k = 1024;
      const sizes = ['GB', 'TB'];
      const i = parseInt(Math.floor(Math.log(bytes) / Math.log(k)));
      if (bytes < 1) {
        return bytes.toFixed(2)+" GB"
      }
      if (i >= 0) {
        return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i];
      }
    },
    selecte_item(index) {
      this.$store.commit('setindex',index)
    },
    selected_item() {
      return this.$store.state.index
      // return this.$store
    }
  }
}
</script>

<template>
  <md-list-item type="button" @click="this.selecte_item(index)" :disabled="selected_item() === index">
    <div slot="headline">
      <div class="supporting-text">
        <span>{{index+1}}.{{name}}</span>
        <span>{{days}}</span>
      </div>
    </div>
    <div slot="supporting-text">
      <div class="supporting-text">
        <span class="region">区域: {{region}}</span>
        <span class="data">{{formatBytes(this.value)}}/{{formatBytes(10240)}}</span>
      </div>
      <md-linear-progress :value="this.value" max="10240" buffer="10240"/>
<!--      <div style="transform: translateY(-24px)translateX(100%);position: absolute">{{formatBytes(this.value)}}/{{formatBytes(10240)}}</div>-->
    </div>
  </md-list-item>
  <md-divider/>
</template>

<style scoped>
.supporting-text {
  display: flex;
  justify-content: space-between;
}
</style>