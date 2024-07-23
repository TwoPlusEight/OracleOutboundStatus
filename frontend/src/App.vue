<script setup>
import MainView from "@/view/MainView.vue";
import AccountView from "@/view/AccountView.vue";
import HeaderView from "@/view/HeaderView.vue";
</script>
<script>
import axios from "axios";

export default {
  data() {
    return{
      data: null,
      response: null
    }
  },
  methods:{
    fun() {
      axios.get('/data.json').then(
          response => {
            this.response = response.data["OracleCloud"]
          }
      );
    },
    selected_item() {
      return this.$store.state.index
    }
  },
  mounted() {
    this.fun()
    // let index = this.selected_item()
    // this.data = this.response[index]["data"]
  },
  updated() {
    if(this.response) {
      let index = this.selected_item()
      console.log(index)
      this.data = this.response[index]["data"]
    }
  }
}
</script>

<template>
  <header>
    <HeaderView/>
  </header>
  <sidebar>
    <AccountView :oraclecloud="response"/>
    <div style="display: none">{{selected_item()}}</div> <!--去掉就会更新失败, "代码非常稳定"XD-->
  </sidebar>
  <main>
    <MainView :data="data"/>
  </main>
</template>

<style scoped>
header {
  grid-column-start: 1;
  grid-column-end: 3;
  grid-row-start: 1;
  grid-row-end: 2;
}
sidebar,main {
  height: calc(100vh - 60px);
  overflow-y:auto;
}
sidebar {
  border-right: #ccb3cc 5px solid;
}
</style>
