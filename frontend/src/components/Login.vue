<template>
  <div>
    <div id="login">
      <h1> LOGIN </h1>
      <div class="form-label-group">
        <label for="inputUsername">Username</label>
        <input type="username" id="inputUsername" class="form-control" placeholder="Username" required autofocus v-model="username">
      </div>
      <div class="form-label-group">
        <br>
        <label for="inputPassword">Password</label>
        <input type="password" id="inputPassword" class="form-control" placeholder="Password" required v-model="password">
      </div>
      <button class="btn btn-primary" @click="checkLogin()">Sign in</button>
      <button class="btn btn-primary" @click="viewSignup()">Create Account</button>
      <button class="btn btn-primary" @click="backToEvents()">Back to events</button>
    </div>
    <div id="signup" style="display: none">
      <h1> SIGN UP </h1>
      <div class="form-label-group">
        <label for="signupUsername">Username</label>
        <input type="addUserForm.username" id="signupUsername" class="form-control" placeholder="Username" required autofocus v-model="addUserForm.username">
      </div>
      <div class="form-label-group">
        <br>
        <label for="signupPassword">Password</label>
        <input type="password" id="signupPassword" class="form-control" placeholder="Password" required v-model="addUserForm.password">
      </div>
      <button class="btn btn-primary" @click="checkSignup()">Submit</button>
      <button class="btn btn-danger" @click="initForm()">Reset</button>
      <button class="btn btn-secondary" @click="viewLogin()">Cancel</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      username: '',
      password: '',
      addUserForm: {
        username: '',
        password: ''
      },
      fromLogin: 0
    }
  },
  methods: {
    checkLogin () {
      const parameters = {
        username: this.username,
        password: this.password
      }
      const path = `https://f02-eventright.herokuapp.com/login`
      axios.post(path, parameters)
        .then((res) => {
          this.logged = true
          this.token = res.data.token
          this.find_match = true
          this.getAccount()
          console.log(res.data)
          this.fromLogin = 1
          alert('Successful log in! Welcome back ' + parameters.username)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          alert('Username or Password incorrect')
        })
    },
    getAccount () {
      const path = `https://f02-eventright.herokuapp.com/account/` + this.username
      axios.get(path)
        .then((res) => {
          this.is_admin = res.data.account.is_admin
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          alert('Role error')
        })
    },
    viewLogin () {
      document.getElementById('login').style.display = 'block'
      document.getElementById('signup').style.display = 'none'
    },
    viewSignup () {
      document.getElementById('login').style.display = 'none'
      document.getElementById('signup').style.display = 'block'
    },
    backToEvents () {
      if (this.fromLogin === 1) {
        this.$router.replace({
          path: '/',
          query: {username: this.username, logged: this.logged, token: this.token, is_admin: this.is_admin}
        })
      } else {
        this.logged = false
        this.$router.replace({ path: '/', query: { logged: this.logged } })
      }
    },
    initForm () {
      this.addUserForm.username = ''
      this.addUserForm.password = ''
    },
    checkSignup () {
      const parameters = {
        username: this.addUserForm.username,
        password: this.addUserForm.password
      }
      const path = `https://f02-eventright.herokuapp.com/account/${parameters.username}`
      axios.post(path, parameters)
        .then((res) => {
          // this.username = parameters.username //to login instantly after signup
          // this.password = parameters.password
          alert('Successful sign up! Welcome abroad ' + this.username)
          this.fromLogin = 0
          this.viewLogin() // To go back to login
          // this.checkLogin() // Al crear un usuari fas el login amb l'usuari
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          alert('Username already exists')
        })
    }
  }
}
</script>

<style scoped>

</style>
