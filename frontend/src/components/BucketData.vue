<script>
export default {
  props: {
    request: 0.0,
    value: 0.0
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
      // 显示 MB 以上的大小时，保留两位小数
      if (i >= 0) {
        return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i];
      }
    }
  }
}

</script>

<template>
  <md-list-item type="button">
    <div slot="headline">存储桶</div>
    <div slot="supporting-text">
      <div class="container">
        <div class="requests">
          <span class="label">请求次数:</span>
          <span class="data">{{this.request}}万</span>
        </div>
        <md-linear-progress :value="this.request" max="100" buffer="100"></md-linear-progress>
        <div class="outbound">
          <span class="vnic-name">出站流量:</span>
          <span class="outbound-data">{{formatBytes(this.value)}}</span>
        </div>
        <md-linear-progress :value="this.value" max="10240" buffer="10240"></md-linear-progress>
      </div>
    </div>
  </md-list-item>
  <md-divider/>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
}
.requests,.outbound {
  display: flex;
  justify-content: space-between;
}
.requests:hover,.outbound:hover {
//text-decoration: underline;
  background-color: #e1e1e1;
}

</style>