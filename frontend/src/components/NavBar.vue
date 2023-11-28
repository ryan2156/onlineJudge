
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
    <div class="container-fluid">

    </div>
    <nav class="navbar navbar-light bg-light">
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> |
        <router-link to="/login">Log in</router-link>
    </nav>
</template>

<script>
    export default{
    name: "NavBar",
    props: {
        username: String,
    },
}

</script>