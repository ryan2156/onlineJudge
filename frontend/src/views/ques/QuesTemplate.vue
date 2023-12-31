<template>
    <div class="container">
        <h2>題目</h2>
        <p>文字描述</p>
    </div>
</template>

<script>
export default{
    name: "QuesTemplate",
    data(){
        return{
            quesDesc:{
                title: '',
                describe: '',
            },
            ans: ''
        }
    }
}

</script>