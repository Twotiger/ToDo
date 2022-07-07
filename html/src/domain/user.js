class User {
  isLogin() {
    return this.getToken() !== null
  }
  setToken(token) {
    localStorage.setItem("token", token)
  }
  getToken() {
    return localStorage.getItem("token")
  }
  logout() {
    localStorage.removeItem("token");
  }
}

export default User