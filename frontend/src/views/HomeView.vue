<template>
  <div class="container-sm">
    <h2>題目</h2>
    <table class="table table-striped table-hover">
      <thead>
        <th scope="col-2" class="text-start">#</th>
        <th scope="col-4" class="text-start">title</th>
      </thead>
      <tbody>
        <tr @click="goQues">
          <th scope="row" class="text-start">1</th>
          <td class="text-start">Hello World</td>      
        </tr>        
      </tbody>
    </table>
  </div>
</template>

<script>
import router from '../router/index.js';
export default {
  name: 'HomeView',
  methods: {
    goQues(){
      router.push({name: "question"})
    }
  }
}
</script>
