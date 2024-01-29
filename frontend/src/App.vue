<template>
  <index-view></index-view>
</template>

<script>
import IndexView from './components/IndexView.vue'

export default {
  title: "Bus Stops",
  name: 'App',
  components: {
    IndexView
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
