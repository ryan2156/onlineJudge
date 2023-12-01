import axios from "axios"

async function login(userName, password){
    const result= {
        status: 1,
        token: ""
    }

    const url = "/api/login"
    const data = {
        username: userName,
        password: password
    }
    const res = await axios.post(url, data)
    if(res.data.status){
        result.status = 0
        result.token = res.data.token
        setLoginStore({
            isLogin: true,
            token: result.token,
            userName: res.data.username
        })
    }

    return result
}

async function authToken(token){
    const result = {
        status: "",
        token: "",
        userName: ""
    }
    const url = "/api/auth"
    const data = {
        token: token
    }
    const res = await axios.post(url, data)
    if(res.status){
        result.status = "jwt verify success"
        result.token = res.data.token
        result.userName = res.data.username
        setLoginStore({
            isLogin: true,
            token: result.token,
            userName: result.userName
        })
    }else{
        setLoginStore({
            isLogin: false,
            token: "",
            userName: ""
        })
    }

    return result
}


function setLoginStore(options){
    if(options.isLogin){
        window.localStorage.setItem("isLogin", options.isLogin)
    }
    if(options.token){
        window.localStorage.setItem("token", options.token)
    }
    if(options.userName){
        window.localStorage.setItem("username", options.username)
    }
}

export {login, authToken}