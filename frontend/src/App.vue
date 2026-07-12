<template>
  <div id="app-layout">
    <RouterView />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* Butun loyiha uchun umumiy va chiroyli shrift hamda stillar */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
  background-color: #f5f7fb;
  color: #333;
}
@import url('https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css');
</style>