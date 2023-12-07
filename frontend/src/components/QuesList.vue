<template>
    <div>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">Id</th>
                    <th scope="col">Title</th>
                    <th scope="col">Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in ques" :key="index">
                    <td>{{ item.id }}</td>
                    <td>{{ item.title }}</td>
                    <td>{{ item.last_name }}</td>
                </tr>
            </tbody>
            
        </table>
    </div>
</template>

<script>
    export default{
        name: 'QuesList',
        data(){
            return{
                ques: [
                    { id: 40, title: 'Dickerson', last_name: 'Macdonald' },
                    { id: 21, title: 'Larsen', last_name: 'Shaw' },
                    { id: 89, title: 'Geneva', last_name: 'Wilson' },
                    { id: 38, title: 'Jami', last_name: 'Carney' }
                ]
            }
            
        }
    }

</script>