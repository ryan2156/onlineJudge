<template>
  <div class="container-md">
    <QuesList></QuesList>
  </div>
</template>

<script>
// @ is an alias to /src
import QuesList from '@/components/QuesList.vue'

export default {
  name: 'HomeView',
  components: {
    QuesList,
}
}
</script>
