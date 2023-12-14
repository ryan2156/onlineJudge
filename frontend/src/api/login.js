import axios from "axios"

async function login(Account, password){
    const result= {
        status: 1,
        token: ""
    }

    const url = "/api/login"
    const data = {
        account: Account,
        password: password
    }
    const res = await axios.post(url, data)
    if(!res.data.status){
        console.log('a');
        result.status = 0;
        result.token = res.data.access_token;
        setLoginStore({
            isLogin: true,
            token: result.token,
            Account: res.data.account
        })
    }
    return result
}

async function authToken(token){
    const result = {
        status: "",
        token: "",
        Account: ""
    }
    const url = "/api/auth"
    const data = {
        token: token
    }
    const res = await axios.post(url, data)
    if(!res.status){
        result.status = "jwt verify success"
        result.token = res.data.access_token
        result.Account = res.data.account
        setLoginStore({
            isLogin: true,
            token: result.token,
            Account: result.account
        })
    }else{
        setLoginStore({
            isLogin: false,
            token: "",
            Account: ""
        })
    }
    console.log(result);
    return result
}


function setLoginStore(options){
    if(options.isLogin){
        window.localStorage.setItem("isLogin", options.isLogin)
    }
    if(options.token){
        window.localStorage.setItem("token", options.token)
    }
    if(options.Account){
        window.localStorage.setItem("account", options.Account)
    }
}

export {login, authToken}