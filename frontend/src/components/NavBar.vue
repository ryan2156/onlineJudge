
<style scoped>
  nav {
    padding: 15px;
  }
  
  nav a {
    font-weight: bold;
    color: #2c3e50;
  }
  
  nav a.router-link-exact-active {
    color: #42b983;
  }
</style>

<template>
  <nav class="navbar navbar-expand-sm navbar-light bg-light">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">Cobreak</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
        
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/about" class="nav-link">About</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/test" class="nav-link">Test</router-link>
          </li>
          <li class="nav-item" v-if="!isLogin">
            <router-link to="/login" class="nav-link">Login</router-link>
          </li>
          <div v-text="account"></div>
        </ul>
      </div>
    </div>
  </nav>
</template>





<script>
    export default{
    name: "NavBar",
    data(){
      return {
        isLogin: window.localStorage.getItem("isLogin") === true,
        account: window.localStorage.getItem("account")
      };
    },
}

</script>