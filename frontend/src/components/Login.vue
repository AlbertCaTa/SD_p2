<template>
  <div>
    <div class="form-label-group">
      <label for="inputEmail">Username</label>
      <input type="username" id="inputUsername" class="form-control" placeholder="Username" required autofocus v-model="username">
    </div>
    <div class="form-label-group">
      <br>
      <label for="inputPassword">Password</label>
      <input type="password" id="inputPassword" class="form-control" placeholder="Password" required v-model="password">
    </div>
    <button class="btn btn-primary" @click="checkLogin()">Sign in</button>
    <button class="btn btn-primary">Create Account</button>
    <button class="btn btn-primary" @click="backToEvents()">Back to events</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    checkLogin () {
      const parameters = {
        username: this.username,
        password: this.password
      }
      const path = `http://localhost:5000/login`
      axios.post(path, parameters)
        .then((res) => {
          this.logged = true
          this.token = res.data.token
          this.find_match = true
          this.getAccount()
          console.log(res.data)
          alert('Successful log in! Welcome back ' + this.username)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          alert('Username or Password incorrect')
        })
    },
    getAccount () {
      const path = `http://localhost:5000/accounts`
      axios.get(path)
        .then((res) => {
          for (let acc of res.data.accounts.values()) {
            if (acc.username === this.username) {
              this.is_admin = acc.is_admin
            }
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          alert('Role error')
        })
    },
    backToEvents () {
      this.$router.replace({ path: '/', query: { username: this.username, logged: this.logged, token: this.token, is_admin: this.is_admin } })
    }
  }
}
</script>

<style scoped>

</style>
