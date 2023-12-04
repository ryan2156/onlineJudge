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
        <button type="submit">提交</button>
      </form>
    </div>
  </template>
  
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
            let res = await login(this.account, this.password)
            if(res.status==0){
                router.push({name:"home"})
            }
        }
    }
  }
</script>
  