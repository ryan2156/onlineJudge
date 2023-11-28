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
  import userRequest from 'axios'
  
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
      login () {

        // 驗證
        if(this.user_id === ''){
          this.showIdEmpty = true;
        } else{
          this.showIdEmpty = false;
        }
        if(this.password === ''){
          this.showPwEmpty = true;
        } else{
          this.showPwEmpty = false;
        }

        //  如果都不是空的則寄出
        if(this.user_id && this.password){
          userRequest.post(
              '/login',{
              username: this.user_id,
              password: this.password
            })
          .then(response => {
            if (response.data.success) {
              // 登入成功，導航到主頁面
              this.$router.push('/')
            } else {
              // 登入失敗，顯示錯誤消息
              alert('用戶名或密碼錯誤。')
            }
          })
          .catch(error => {
            // 請求失敗，顯示錯誤消息
            alert(error)
          })
        }
      }
    }
  }
  </script>
  