<!--
单个服务器的流量信息(各个网卡的出站流量)
-->
<script>
export default {
  props: {
    data: null,
  },
  methods: {
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
    fun(){
      this.total = 0
      this.name = this.data["name"]
      this.shape = this.data["shape"]
      this.cpu = this.data["cpu"]
      this.name = this.data["name"]
      this.vnics = this.data["vnic"]
      for (let i = 0;i<this.vnics.length;i++) {
        this.total += this.vnics[i]["outbound"]
      }
    }
  },
  data(){
    return {
      name: "",
      shape: "",
      cpu: "",
      vnics: [],
      total: 0.0
    }
  },
  created() {
    this.fun()
  },
  watch: {
    data(){
      this.fun()
    }
  }
}
</script>

<template>
  <md-list-item type="button">
    <div class="container">
      <div class="name">
        <span class="label">名称:</span><span class="data">{{name}}</span>
      </div>
      <div class="shape">
        <span class="label">实例:</span><span class="data">{{shape}}</span>
      </div>
      <div class="CPU">
        <span class="label">处理器:</span><span class="data">{{cpu}}</span>
      </div>
      <div class="vnics">网卡流量 ↓</div>
      <div class="vnics" v-for="row in this.vnics">
        <div class="outbound">
          <span class="vnic-name">-> {{row["name"]}}</span>
          <span class="outbound-data">{{formatBytes(row["outbound"])}}</span>
        </div>
<!--        <md-linear-progress :value="this.value" max="100" buffer="100"></md-linear-progress>-->
      </div>
      <div class="outbound">
        <span class="vnic-name">总出站流量:</span>
        <span class="outbound-data">{{formatBytes(total)}}</span>
      </div>
      <md-linear-progress :value="parseInt(total)" max="10240" buffer="10240"></md-linear-progress>
    </div>
  </md-list-item>
  <md-divider/>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
}
.name,.shape,.CPU,.outbound {
  display: flex;
  justify-content: space-between;
}
.name:hover,.shape:hover,.CPU:hover,.outbound:hover {
  //text-decoration: underline;
  background-color: #e1e1e1;
}
.name .data,.shape .data,.CPU .data,.outbound .outbound-data{
  margin-left: 5px;
}
</style>