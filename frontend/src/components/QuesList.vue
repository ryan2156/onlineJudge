<template>
    <div>
        <h2>123</h2>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">Id</th>
                    <th scope="col">Title</th>
                    <th scope="col">Status</th>
                </tr>
            </thead>
            <tbody>
                <router-link>
                    <tr v-for="(item, index) in ques" :key="index">
                        <td>{{ item.id }}</td>
                        <td>{{ item.title }}</td>
                        <td>{{ item.last_name }}</td>
                    </tr>
                </router-link>   
            </tbody>
            
        </table>
    </div>
</template>

<script>
    import axios from 'axios';
    export default{
        name: 'QuesList',
        data(){
            return{
                ques: axios.get('http://localhost:5000')
            }
            
        }
    }

</script>