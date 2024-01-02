<template>
    <div class="container">
        <div class="row">
            <div class="col text-start">
                <h2>題目</h2>
                <p>
                    學習所有程式語言的第一個練習題 
                    請寫一個程式，可以讀入指定的字串，並且輸出指定的字串。

                    比如：輸入字串 "world", 則請輸出 "Hello, world"
                </p>
                <div class="row">
                    <div class="col-md-6 ">
                        <h5>範例輸入 1</h5>
                        <p>C++</p>
                    </div>
                    <div class="col-md-6">
                        <h5>範例輸出 1</h5>
                        <p>Hello, C++</p>
                    </div>
                </div>
            </div>
            <div class="col">
                <h2>作答區</h2>
                <form class="mb-3" @submit.prevent="submit()">
                    <textarea class="form-control" id="exampleFormControlTextarea1" rows="8" v-model="code"></textarea>
                    <div class="col-auto">
                        <button type="submit" class="btn btn-primary mb-3">寄出</button>
                    </div>
                </form>
                <h3>回應</h3>
                <p>{{ result }}</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
 .container{
    margin-top: 2%;
 }
</style>

<script>
import axios from 'axios';

export default{
    name: "QuesTemplate",
    data() {
        return {
            code: '',
            result: ''
        }
    },
    methods: {
        submit(){
            const code = this.code;

            const blob = new Blob([code], {
                type: 'text/plain',
            });
            
            const token = window.localStorage.getItem('token');
            const account = window.localStorage.getItem('account')

            axios.post('http://localhost:5000/submit', blob, {
            headers: {
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': 'attachment; filename=response.txt',
                'Authorization': `Bearer ${token}`,
                'accoun': account,
                'ques_id': 1
            },
            })
            .then((response) => {
                this.result = response
            })
            .catch((error) => {
                this.result = error
            });
        }
    }
}

</script>