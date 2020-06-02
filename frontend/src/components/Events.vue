<template>
  <div>
    <div id="events">
      <button class="btn-primary" type="button" name="button" @click="viewCart()">
            VIEW CART
      </button>
      <button class="btn-primary" type="button" name="button" @click="logIn()">
            LOG IN
      </button>
      <button id="addEventBtn" class="btn-primary" type="button" name="button" @click="viewAddEvent()">
            ADD EVENT
      </button>
      <button id="editEventBtn" class="btn-primary" type="button" name="button" @click="viewEditEvent()">
            EDIT EVENT
      </button>
      <h1>EVENTS</h1>
      <h2>AVAILABLE MONEY: {{ this.available_money }} </h2>
      <h2>TOTAL TICKETS : {{ this.tickets_added }}</h2>
      <div class="container-fluid">
        <div class="row">
          <div class="col-lg-4 col-md-6 mb-4" v-for="e in events" :key="e.id">
            <div class="card" style="width: 18rem;">
              <img class="card-img-top" src="../assets/logo.png" alt="Card image cap">
              <div class="card-body">
                <h5 class="card-title">{{ e.name }}</h5>
                <h6 class="card-subtitle"> Invited artists :</h6>
                <h6 class="card-subtitle" v-for="a in e.artists" :key="a.id">{{ a.name }} , </h6>
                <p class="card-text">City : {{ e.city }}</p>
                <p class="card-text">Address : {{ e.place }}</p>
                <p class="card-text">Date : {{ e.date }}</p>
                <p class="card-text">Price : {{ e.price  }}$</p>
                <p class="card-text">Tickets available : {{ e.total_available_tickets  }}</p>
                <a href="#" class="btn btn-primary" @click="addToCart(e)">Add to cart</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="carts" style="display: none"><!--https://designmodo.com/demo/shopping-cart/-->
      <button class="btn-primary" type="button" name="button" @click="viewEvents()">
              VIEW EVENTS
      </button>
      <h1>CART</h1>
      <link rel="stylesheet" type="text/css" href="/static/cart.css">
      <div class="shopping-cart">
        <!-- Title -->
        <div class="title">
          Shopping Bag | Total price : {{ this.total_price }} $
          <button type="button" name="button" @click="finalizePucharse()" :disabled="cartItems.length == 0">
              Finalize pucharse
          </button>
        </div>
        <!-- Product -->
        <div class="item" v-for="item in cartItems" :key="item.name">
          <div class="buttons">
            <span class="delete-btn" @click="deleteCart(item)">X</span>
          </div>

          <div class="image">
            <img class="card-img-top" src="../assets/logo.png" alt="Card image cap" width="50" height="50">
            {{ item.event_name }}
          </div>
          <div class="quantity">
            <button class="plus-btn" type="button" name="button" @click="plusCart(item)">
              +
            </button>
            <span> {{ item.quantity }} </span>
            <button class="minus-btn" type="button" name="button" @click="minusCart(item)">
              -
            </button>
          </div>
          <div class="total-price"> ${{item.price}} </div>
        </div>
      </div>
    </div>
    <div id="addEvent" style="display: none">
      <h1> SIGN UP </h1>
      <div class="form-label-group">
        <label for="eventName">Name</label>
        <input type="addEventForm.name" id="eventName" class="form-control" placeholder="Name" required autofocus v-model="addEventForm.name">
      </div>
      <div class="form-label-group">
        <label for="eventPlace">Place</label>
        <input type="addEventForm.place" id="eventPlace" class="form-control" placeholder="Place" required autofocus v-model="addEventForm.place">
      </div>
      <div class="form-label-group">
        <label for="eventCity">City</label>
        <input type="addEventForm.city" id="eventCity" class="form-control" placeholder="City" required autofocus v-model="addEventForm.city">
      </div>
      <div class="form-label-group">
        <label for="eventDate">Date</label>
        <input type="addEventForm.date" id="eventDate" class="form-control" placeholder="Date" required autofocus v-model="addEventForm.date">
      </div>
      <div class="form-label-group">
        <label for="eventPrice">Price</label>
        <input type="addEventForm.price" id="eventPrice" class="form-control" placeholder="Price" required autofocus v-model="addEventForm.price">
      </div>
      <div class="form-label-group">
        <label for="eventTickets">Total available tickets</label>
        <input type="addEventForm.available_tickets" id="eventTickets" class="form-control" placeholder="Total available tickets" required autofocus v-model="addEventForm.available_tickets">
      </div>
      <button class="btn btn-primary" @click="onSubmit()">Submit</button>
      <button class="btn btn-danger" @click="onReset(addEventForm)">Reset</button>
      <button class="btn btn-secondary" @click="viewEvents()">Cancel</button>
    </div>
    <div id="editEvent" style="display: none">
      <h1> SIGN UP </h1>
      <div class="form-label-group">
        <label for="editEventId">ID</label>
        <input type="editEventForm.id" id="editEventId" class="form-control" placeholder="ID" required autofocus v-model="editEventForm.id">
      </div>
      <div class="form-label-group">
        <label for="editEventName">Name</label>
        <input type="editEventForm.name" id="editEventName" class="form-control" placeholder="Name" required autofocus v-model="editEventForm.name">
      </div>
      <div class="form-label-group">
        <label for="editEventPlace">Place</label>
        <input type="editEventForm.place" id="editEventPlace" class="form-control" placeholder="Place" required autofocus v-model="editEventForm.place">
      </div>
      <div class="form-label-group">
        <label for="editEventCity">City</label>
        <input type="editEventForm.city" id="editEventCity" class="form-control" placeholder="City" required autofocus v-model="editEventForm.city">
      </div>
      <div class="form-label-group">
        <label for="editEventDate">Date</label>
        <input type="editEventForm.date" id="editEventDate" class="form-control" placeholder="Date" required autofocus v-model="editEventForm.date">
      </div>
      <div class="form-label-group">
        <label for="editEventPrice">Price</label>
        <input type="editEventForm.price" id="editEventPrice" class="form-control" placeholder="Price" required autofocus v-model="editEventForm.price">
      </div>
      <div class="form-label-group">
        <label for="editEventTickets">Total available tickets</label>
        <input type="editEventForm.available_tickets" id="editEventTickets" class="form-control" placeholder="Total available tickets" required autofocus v-model="editEventForm.available_tickets">
      </div>
      <button class="btn btn-primary" @click="onSubmitUpdate()">Submit</button>
      <button class="btn btn-danger" @click="onReset(editEventForm)">Reset</button>
      <button class="btn btn-secondary" @click="viewEvents()">Cancel</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      events: [{
        id: 0,
        name: '',
        artists: [{artist: { name: '', id: 1, country: '', genre: 'cap' }}],
        city: '',
        place: '',
        date: '',
        price: 0,
        total_available_tickets: 100
      }
      ],
      tickets_added: 0,
      cartItems: [{
        event_name: String,
        event_id: 0,
        quantity: 0,
        price: 0}],
      total_price: 0,
      show: 'disabled',
      available_money: 0,
      addEventForm: {
        place: '',
        name: '',
        city: '',
        date: '',
        price: '',
        available_tickets: ''
      },
      editEventForm: {
        id: '',
        place: '',
        name: '',
        city: '',
        date: '',
        price: '',
        available_tickets: ''
      }
    }
  },
  methods: {
    getEvents () {
      const path = 'http://localhost:5000/events'
      axios.get(path)
        .then((res) => {
          this.events = res.data.events
        })
        .catch((error) => {
          console.error(error)
        })
    },
    addToCart (e) {
      this.cartItems.push({event_name: e.name, event_id: e.id, quantity: 1, price: e.price})
      console.log(e.name)
      this.total_price += e.price
      console.log(this.cartItems.length)
      this.tickets_added++
    },
    plusCart (item) {
      console.log('plus')
      item.quantity += 1
      this.total_price += item.price
      this.tickets_added++
    },
    minusCart (item) {
      console.log('minus')
      item.quantity -= 1
      this.total_price -= item.price
      if (item.quantity === 0) {
        this.cartItems.splice(this.cartItems.indexOf(item), 1)
      }
      this.tickets_added--
      console.log(this.cartItems)
    },
    deleteCart (item) {
      this.cartItems.splice(this.cartItems.indexOf(item), 1)
      this.tickets_added -= item.quantity
    },
    addPuchrase (parameters) {
      const path = `http://localhost:5000/orders/${this.username}`
      console.log('addPucharse username ' + this.username)
      console.log('addPucharse token ' + this.token)
      axios.post(path, parameters, {
        auth: {username: this.token}
      })
        .then(() => {
          console.log('Order done')
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
          this.getEvents()
        })
    },
    finalizePucharse () {
      for (let i = 0; i < this.cartItems.length; i++) {
        const parameters = {
          event_id: this.cartItems[i].event_id,
          tickets_bought: this.cartItems[i].quantity
        }
        console.log(parameters)
        this.addPuchrase(parameters)
      }
      this.cartItems.splice(0, this.cartItems.length)
      this.initEventsMoneyTickets()
    },
    viewEvents () {
      document.getElementById('carts').style.display = 'none'
      document.getElementById('addEvent').style.display = 'none'
      document.getElementById('editEvent').style.display = 'none'
      document.getElementById('events').style.display = 'block'
    },
    viewCart () {
      document.getElementById('events').style.display = 'none'
      document.getElementById('addEvent').style.display = 'none'
      document.getElementById('editEvent').style.display = 'none'
      document.getElementById('carts').style.display = 'block'
    },
    viewAddEvent () {
      document.getElementById('events').style.display = 'none'
      document.getElementById('carts').style.display = 'none'
      document.getElementById('editEvent').style.display = 'none'
      document.getElementById('addEvent').style.display = 'block'
    },
    viewEditEvent () {
      document.getElementById('events').style.display = 'none'
      document.getElementById('carts').style.display = 'none'
      document.getElementById('addEvent').style.display = 'none'
      document.getElementById('editEvent').style.display = 'block'
    },
    logIn () {
      this.$router.replace({path: '/userlogin'})
    },
    getAvailableMoney () {
      if (typeof this.username !== 'undefined') {
        const path = `http://localhost:5000/account/${this.username}`
        axios.get(path)
          .then((res) => {
            this.available_money = res.data.account.available_money
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error)
            this.user = ''
            console.log('available money error')
          })
      }
    },
    initEventsMoneyTickets () {
      this.getEvents()
      this.getAvailableMoney()
      this.tickets_added = 0
    },
    onSubmit () {
      const parameters = {
        name: this.addEventForm.name,
        place: this.addEventForm.place,
        city: this.addEventForm.city,
        date: this.addEventForm.date,
        price: this.addEventForm.price,
        available_tickets: this.addEventForm.available_tickets
      }
      console.log(parameters)
      this.addEvent(parameters)
      this.initEventForm()
      this.getEvents()
    },
    addEvent (parameters) {
      const path = `http://localhost:5000/event`
      axios.post(path, parameters, {
        auth: {username: this.token}
      })
        .then((res) => {
          console.log('AddEvent success')
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          console.log('AddEvent failure')
        })
    },
    onSubmitUpdate () {
      const parameters = {
        name: this.editEventForm.name,
        place: this.editEventForm.place,
        city: this.editEventForm.city,
        date: this.editEventForm.date,
        price: this.editEventForm.price,
        available_tickets: this.editEventForm.available_tickets
      }
      this.updateEvent(parameters)
      this.initEventForm()
      this.getEvents()
    },
    updateEvent (parameters) {
      const path = `http://localhost:5000/event/${this.editEventForm.id}`
      axios.put(path, parameters, {
        auth: {username: this.token}
      })
        .then((res) => {
          console.log('EditEvent success')
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.user = ''
          console.log('EditEvent failure')
        })
    },
    onReset (evt) {
      evt.preventDefault()
      this.initEventForm()
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
    },
    initEventForm () {
      this.addEventForm.name = ''
      this.addEventForm.place = ''
      this.addEventForm.city = ''
      this.addEventForm.date = ''
      this.addEventForm.price = ''
      this.addEventForm.total_available_tickets = ''

      this.editEventForm.id = ''
      this.editEventForm.name = ''
      this.editEventForm.place = ''
      this.editEventForm.city = ''
      this.editEventForm.date = ''
      this.editEventForm.price = ''
      this.editEventForm.total_available_tickets = ''
    },
    initAdminButtons () {
      console.log('isadmin ' + this.is_admin)
      console.log(typeof this.is_admin)
      if (this.is_admin === '1') {
        console.log('si entra')
        document.getElementById('addEventBtn').style.display = 'block'
      } else {
        document.getElementById('addEventBtn').style.display = 'none'
      }
    }
  },
  created () {
    console.log('CREATED: ' + JSON.stringify(this.events))
    this.cartItems = []
    this.logged = this.$route.query.logged
    this.username = this.$route.query.username
    this.is_admin = this.$route.query.is_admin
    this.token = this.$route.query.token
    this.initEventsMoneyTickets()
    this.initAdminButtons()
  }
}
</script>
