<template>
  <div>
    <div id="login">
      <div style="height: 30px"></div>
      <div>
        <h1 style="text-align: center;  font-family: 'Oswald', Helvetica, sans-serif;  font-size: 80px;  transform: skewY(-10deg);  letter-spacing: 4px;  word-spacing: -8px;  color: #ff6347;  text-shadow:     -1px -1px 0 firebrick,    -2px -2px 0 firebrick,    -3px -3px 0 firebrick,    -4px -4px 0 firebrick,    -5px -5px 0 firebrick,    -6px -6px 0 firebrick,    -7px -7px 0 firebrick,    -8px -8px 0 firebrick,    -30px 20px 40px dimgrey">
          LOGIN
        </h1>
      </div>
      <div style="height: 20px"></div>
      <div style="background-color: #ff6347; height: 35px">
        <div style="display: inline-block; float:right">
          <button class="btn btn-primary btn-sm mr-1" @click="backToEvents()">Back to events</button>
        </div>
      </div>
      <div class="form-label-group">
        <label for="inputUsername">Username</label>
        <input type="username" id="inputUsername" class="form-control" placeholder="Username" required autofocus v-model="username">
      </div>
      <div class="form-label-group">
        <br>
        <label for="inputPassword">Password</label>
        <input type="password" id="inputPassword" class="form-control" placeholder="Password" required v-model="password">
      </div>
      <button class="btn btn-primary btn-sm" @click="checkLogin()">Sign in</button>
      <button class="btn btn-primary btn-sm" @click="viewSignup()">Create Account</button>
    </div>
    <div id="signup" style="display: none">
      <div style="height: 30px"></div>
      <div>
        <h1 style="text-align: center;  font-family: 'Oswald', Helvetica, sans-serif;  font-size: 80px;  transform: skewY(-10deg);  letter-spacing: 4px;  word-spacing: -8px;  color: #ff6347;  text-shadow:     -1px -1px 0 firebrick,    -2px -2px 0 firebrick,    -3px -3px 0 firebrick,    -4px -4px 0 firebrick,    -5px -5px 0 firebrick,    -6px -6px 0 firebrick,    -7px -7px 0 firebrick,    -8px -8px 0 firebrick,    -30px 20px 40px dimgrey">
          SIGNUP
        </h1>
      </div>
      <div style="height: 20px"></div>
      <div style="background-color: #ff6347; height: 35px">
      </div>
      <div class="form-label-group">
        <label for="signupUsername">Username</label>
        <input type="addUserForm.username" id="signupUsername" class="form-control" placeholder="Username" required autofocus v-model="addUserForm.username">
      </div>
      <div class="form-label-group">
        <br>
        <label for="signupPassword">Password</label>
        <input type="password" id="signupPassword" class="form-control" placeholder="Password" required v-model="addUserForm.password">
      </div>
      <button class="btn btn-primary btn-sm" @click="checkSignup()">Submit</button>
      <button class="btn btn-danger btn-sm"  @click="initForm()">Reset</button>
      <button class="btn btn-secondary btn-sm" @click="viewLogin()">Cancel</button>
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
