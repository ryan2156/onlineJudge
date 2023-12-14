<template>
  <div>
    <h1>登入</h1>
    <form @submit.prevent="submit()">
      <div v-show="showIdEmpty">
        <p>帳號不能為空</p>
      </div>
      <div>
        <label>帳號：</label>
        <input type="text" v-model="account">
      </div>
      <div v-show="showPwEmpty">
        <p>密碼不能為空</p>
      </div>
      <div>
        <label>密碼：</label>
        <input type="password" v-model="password">
      </div>
      <button type="submit" class="button">提交</button>
      <router-link to="/register" class="button">註冊帳號</router-link>
    </form>
  </div>
</template>

<style scoped>
  .button{
    margin: 0.5rem;
  }
</style>
  
<script>
  import { login } from "@/api/login"
  import router from "../router/index.js"

  export default {
    name: "LoginView",
    data () {
      return {
        account: '',
        password: '',
        showIdEmpty: false,
        showPwEmpty: false,
      }
    },  
    methods: {
      async submit(){
          console.log("123")
          let res = await login(this.account, this.password);
          console.log(res);
          if(res.status==0){
              router.push({name:"home"});
          }
        }
    }
  }
</script>
  