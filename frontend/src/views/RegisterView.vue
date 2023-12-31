<template>
    <div>
      <h1>註冊</h1>
      <form @submit.prevent="register()">
        <div>
          <label>帳號：</label>
          <input type="text" v-model="formData.account">
        </div>
        <div>
          <label>密碼：</label>
          <input type="password" v-model="formData.password">
        </div>
        <div>
            <label>驗證密碼：</label>
            <input type="password" v-model="formData.comfirmPassword">
        </div>
        <div>
            <label>暱稱：</label>
            <input type="text" v-model="formData.name">
        </div>
        <button type="submit">提交</button>
      </form>
      <p v-if="registerationError">{{ registerationError }}</p>
      <router-link v-if="registerationSuccess" to="home">{{ registerationSuccess }}</router-link>
    </div>
  </template>

<script>
import axios from 'axios';
import router from '../router/index.js';

export default{
    name: "RegisterView",
    data(){
        return{
            formData:{
                account: '',
                password: '',
                comfirmPassword: '',
                name:''
            },
            registerationError: null,
            registerationSuccess: null
        }
            
    },
    methods:{
        async register(){
            const data = {
                account: this.formData.account,
                password: this.formData.password,
                name: this.formData.name
            }

            if(data.password != this.formData.comfirmPassword){
                this.registerationError = "密碼與驗證密碼不一樣";
                return;
            } else{
                this.registerationError = null;
            }

            const url = 'http://127.0.0.1:5000/register'
            const res = axios.post(url, data)
            try{
                if(!(await res.status)){
                    this.registerationSuccess = '註冊成功重新回至頁面';
                    alert('註冊成功，導回首頁')
                    router.push('login')
                }
            }
            catch(error){
                if(error.response.status === 409){
                    alert("此帳號已被註冊")
                } else{
                this.registerationError = "註冊時發生了未知錯誤"
        }
            }
            
        }
    }
}

</script>