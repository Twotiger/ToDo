import axios from "axios"
// import { MessageBox, Message } from 'element-ui'
import User from "../domain/user"

const service = axios.create({
  // baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    const user = new User()
    if (user.getToken()) {
      config.headers['Authorization'] = user.getToken()
    }
    return config
  },
  error => {
    // do something with request error
    // console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor                                                                                                                                                                                   [0/691]service.interceptors.response.use(
service.interceptors.response.use(
  response => {
    const res = response.data
    if (response.status >= 400) {
      // Message({
      //     message: response.data.errMsg || 'Error',
      //     type: 'error',
      //     duration: 5 * 1000
      // })

      return Promise.reject(new Error(res.message || 'Error'))
    } else {
      return res
    }
  },
  error => {
    console.log('[E] ' + error) // for debug
    const res = error.response.data
    if (error.code === 401) {

      location.reload()
    }
    const message = res.errMsg || error.message
    // Message({
    //     message: message,
    //     type: 'error',
    //     duration: 5 * 1000
    // })
    return Promise.reject(res)
  }
)



class Request {

  get(url, data) {

    if (data && Object.prototype.hasOwnProperty.call(data, "filter_data")) {
      let filterData = data["filter_data"]
      filterData = JSON.stringify(filterData)
      data["filter_data"] = encodeURI(filterData)
    }
    return service.get(url, { params: data })
  }
  post(url, data) {
    return service.post(url, data)
  }
  put(url, data) {
    return service.put(url, data)
  }
  delete(url, data) {
    return service.delete(url, { data: data })
  }
  patch(url, data) {
    return service.patch(url, data)
  }
}


let request = new Request()
export default request