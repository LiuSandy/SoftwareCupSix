<template>
  <Row>
    <Col span="8"><div class="grid-content"></div>
    </Col>
    <Col span="8">
      <div class="grid-content login">
        <h1 style="text-align:center; color:#FFF">民航机票代理市场的预测及可视化</h1>
        <br>
        <h3 style="text-align:center; color:#FFF">系统登录</h3>
        <br><br>
        <Input class="login-input" type="text" v-model="loginForm.username" placeholder="请输入你的用户名" style="opacity: .3"></Input>
        <Input class="login-input" type="password" v-model="loginForm.password" placeholder="请输入你的密码" style="opacity: .3"></Input>
        <Button type="primary" long @click="AuthLogin">登陆</Button>
      </div>
    </Col>
  </Row>
</template>
<script>
export default {
  data () {
    return {
      loginForm: {
        username: '',
        password: ''
      }
    }
  },

  methods: {
    AuthLogin () {
      let user = 'admin'
      let pwd = '123456'
      if (this.loginForm.username === '') {
        this.$Message.error('请输入用户名')
        return
      }

      if (this.loginForm.password === '') {
        this.$Message.error('请输入密码')
        return
      }

      if (this.loginForm.username !== user) {
        this.$Message.error('用户名输入错误')
        return
      }

      if (this.loginForm.password !== pwd) {
        this.$Message.error('密码输入错误')
        return
      }

      localStorage.setItem('login', '1')
      this.$router.push('/')
    }
  }
}
</script>
<style>
body {
 background-image: url('../../assets/bg.jpg');
}
.login {
  padding-top: 15%;
}

.loginTitle {
  text-align: center;
  color: #504b4b;
  margin-bottom: 4%;
  font-weight: 200;
}

.login-input {
  margin-bottom: 20px;
}
.grid-content {
  min-height: 36px;
}

</style>

