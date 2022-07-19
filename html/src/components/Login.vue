<template>
  <div class="loginPage">
    <!-- <svg-icon name="todo_list"></svg-icon> -->
    <div class="login">
      <div class="loginForm">
        <div class="title">登录你的账户</div>
        <div class="input">
          <div class="label">账号</div>
          <input v-model="form.username" />
        </div>
        <div class="input">
          <div class="label">密码</div>
          <input
            type="password"
            v-model="form.password"
            @keyup.enter.native="submit"
          />
        </div>

        <div class="input" v-if="showCode">
          <div class="label">验证码</div>
          <div class="code-box">
            <input v-model="form.code" placeholder="" class="code" />
            <img
              class="img"
              :src="base64Img"
              @click="changeCode"
              title="验证码"
            />
          </div>
        </div>
        <div class="input submit">
          <button type="primary" @click="submit" style="width: 100%">
            登录
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import accountApi from "@/api/account";
import User from "@/domain/user";
import SvgIcon from "@/components/SvgIcon.vue";

export default {
  data() {
    return {
      showCode: false,
      form: {
        username: "",
        password: "",
        code: "",
        token: "",
      },
      base64Img: "",
    };
  },
  methods: {
    async submit() {
      try {
        if (!this.form.username) {
          this.$message.error("请输入用户名");
          // this.$message({ type: "success", str: "登录成功" });
          return;
        }
        if (!this.form.password) {
          this.$message.error("请输入密码");
          return;
        }
        if (this.showCode & !this.form.code) {
          this.$message.error("请输入验证码");
          return;
        }
        let data = await accountApi.login(this.form);
        let user = new User();
        user.setToken(data.token);
        // await this.getUserInfo();
        this.$message.success("登陆成功");
        window.location.href = "/";
      } catch (err) {
        this.$message.error(err.errMsg);
        // this.showVerificationCode();
      }
    },
    async getUserInfo() {
      let data = await accountApi.userInfo();
      let user = new User();
      user.setUserInfo(data.data);
      window.location.href = "/";
    },
    async getCode() {
      let data = await accountApi.getCode();
      return data;
    },
    async showVerificationCode() {
      this.changeCode();
      this.showCode = true;
    },
    async changeCode() {
      let data = await this.getCode();
      const base64ImgData = data["img"];
      this.form.token = data["token"];
      this.base64Img = "data:image/png;base64," + base64ImgData;
    },
    async beforeLogin() {
      let data = await accountApi.loginInfo();
      if (data.errMsg) {
        this.showVerificationCode();
      }
    },
  },
  mounted() {
    // this.beforeLogin();
    let user = new User();
    user.logout()
  },
};
</script>

<style scoped>
body {
  background-image: "";
}

.loginPage {
  height: 100%;
  /* background-image: url("../assets/y-so-serious-white.png"); */
  background-repeat: no-repeat;
  background-position:50% 50% ;
  background-image: url("../assets/todo_list_bg.svg");
}

.login {
  height: 100%;
  display: flex;
  align-content: center;
  align-items: center;
  justify-content: center;
}

.loginForm {
  width: 300px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
  border-radius: 4px;
  padding: 50px;
  backdrop-filter: blur(1px);
}

.loginForm:hover {
  box-shadow: 3px 3px 6px 3px rgba(0, 0, 0, 0.3);
}

.title {
  font-size: 25px;
}

.input {
  padding-top: 15px;
}

.input.submit {
  padding-top: 35px;
}

.label {
  font-size: 18px;
  font-weight: 500;
  padding-bottom: 5px;
}

.form {
  padding: 15px;
  padding-right: 80px;
}

.code {
  width: 100px;
}

.img {
  display: inline-block;
  height: 40px;
  margin-left: 10px;
}

.code-box {
  display: flex;
}

input {
  background-color: #fff;
  background-image: none;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  box-sizing: border-box;
  color: #606266;
  display: inline-block;
  font-size: inherit;
  height: 40px;
  line-height: 40px;
  outline: none;
  padding: 0 15px;
  transition: border-color 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
  width: 100%;
}

button {
  background: #409eff;
  border-color: #409eff;
  display: inline-block;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  border: 1px solid #dcdfe6;
  color: #fff;
  -webkit-appearance: none;
  text-align: center;
  box-sizing: border-box;
  outline: none;
  margin: 0;
  transition: 0.1s;
  font-weight: 500;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  padding: 12px 20px;
  font-size: 14px;
  border-radius: 4px;
}
</style>