import request from "@/utils/request"


export default {
    login(data){
        return request.post("/api/login", data)
    },

    getCode(){
        return request.get("/api/verification_code")
    },

    getAccount() {
        return request.get('/api/account/account')
    }
}