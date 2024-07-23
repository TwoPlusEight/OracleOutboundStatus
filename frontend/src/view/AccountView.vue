<script setup>
import AccountData from "@/components/AccountData.vue";
</script>
<script>
Array.prototype.indexValue = function (arr) {
  for (var i = 0; i < this.length; i++) {
    if (this[i] === arr) {
      return i;
    }
  }
}
export default {
  props: {
    oraclecloud: null,
    index: 0
  },
  data() {
    return{
      days: 0
    }
  },
  methods: {
    calculate(dateStart) {
      const dateObject = new Date(dateStart);

      // 获取当前日期
      const currentDate = new Date();

      // 计算日期差异（以天为单位）
      const timeDifference = currentDate - dateObject;
      const daysPass = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
      if (!(daysPass > 0)) {
        return "死了"
      }
      return "已使用"+daysPass+"天";
    }
  }
}
</script>

<template>
  <md-list>
    <md-divider/>
    <AccountData v-for="data in oraclecloud"
                 :name="data['name']"
                 :region="data['region']"
                 :value="data['data']['outbound']"
                 :days="calculate(data['subsStartTime'])"
                 :index="oraclecloud.indexValue(data)"/>
  </md-list>
</template>

<style scoped>
md-list {
  height: 100%;
  padding: 0;
}
</style>