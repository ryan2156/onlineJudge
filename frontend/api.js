import axios from 'axios';

// 創建一個 Axios 實例並設置基本 URL
const userRequest = axios.create({
    baseURL: 'http://127.0.0.1:5000/'
});

// 使用 Axios 實例發送 GET 請求
userRequest.get('/login')
    .then(response => {
        // 處理響應
        console.log('Users:', response.data);
    })
    .catch(error => {
        // 處理錯誤
        console.error('Error fetching users:', error);
    });

// 使用 Axios 實例發送 POST 請求
userRequest.post('/login', {
    username: '',
    password: ''
})
    .then(response => {
        // 處理響應
        console.log('User created:', response.data);
    })
    .catch(error => {
        // 處理錯誤
        console.error('Error creating user:', error);
    });

export { userRequest }
