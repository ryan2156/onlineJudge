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
        <button type="submit">提交</button>
      </form>
      <p v-if="registerationError">{{ registerationError }}</p>
      <router-link v-if="registerationSuccess" to="home">{{ registerationSuccess }}</router-link>
    </div>
  </template>

<script>
import axios from 'axios';

export default{
    name: "RegisterView",
    data(){
        return{
            formData:{
                account: '',
                password: '',
                comfirmPassword: '',
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
            }

            if(data.password != this.formData.comfirmPassword){
                this.registerationError = "密碼與驗證密碼不一樣";
                return;
            } else{
                this.registerationError = null;
            }
            
            try{
                const res = axios.post(data)
                if(!(await res).status){
                    this.registerationSuccess = '註冊成功重新回至頁面';
                }
            }
            catch(error){
                this.registerationError = "註冊時發生了未知錯誤"
            }
            
        }
    }
}

</script>