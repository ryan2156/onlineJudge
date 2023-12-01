<template>
    <div>
      <h1>登入</h1>
      <form @submit.prevent="login">
        <div v-show="showIdEmpty">
          <p>帳號不能為空</p>
        </div>
        <div>
          <label>用戶名：</label>
          <input type="text" v-model="user_id">
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
  import router from "@/router"


  export default {
    name: "LoginView",
    data () {
      return {
        user_id: '',
        password: '',
        showIdEmpty: false,
        showPwEmpty: false,
      }
    },
    methods: {
      async submit(){                                           //新增
            let res = await login(this.account, this.password)    //新增
            if(res.status==0){                                    //新增
                router.push({name:"home"})                        //新增
            }                                                     //新增
        } 
    }
  }
</script>
  