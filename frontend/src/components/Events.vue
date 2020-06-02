<template>
  <div>
    <div id="events">
      <button class="btn-primary" type="button" name="button" @click="viewCart()" v-if="!is_admin">
            VIEW CART
      </button>
      <button class="btn-primary" type="button" name="button" @click="logIn()">
            LOG IN
      </button>
      <button class="btn-primary" type="button" name="button" @click="logOut()">
            LOG OUT
      </button>
      <button id="addEventBtn" class="btn-primary" type="button" name="button" @click="viewAddEvent()" v-if="is_admin">
            ADD EVENT
      </button>
      <button id="addNewArtistBtn" class="btn-primary" type="button" name="button" @click="viewArtist()" v-if="is_admin">
            GO TO ARTIST
      </button>
      <h1>EVENTS</h1>
      <h2>AVAILABLE MONEY: {{ this.available_money }} </h2>
      <h2>TOTAL TICKETS : {{ this.tickets_added }}</h2>
      <div class="container-fluid">
        <div class="row">
          <div v-for="e in events" :key="e.id">
            <div id="eventCard" class="card ml-3 mt-3 mb-3 mr-3" style="width: 20rem;">
              <img class="card-img-top" src="../assets/logo.png" alt="Card image cap">
              <div class="card-body">
                <h5 class="card-title">{{ e.name }}</h5>
                <h6 class="card-subtitle"> Invited artists :</h6>
                <h6 class="card-subtitle" v-for="a in e.artists" :key="a.id">{{ a.name }}, </h6>
                <p class="card-text">City : {{ e.city }}</p>
                <p class="card-text">Address : {{ e.place }}</p>
                <p class="card-text">Date : {{ e.date }}</p>
                <p class="card-text">Price : {{ e.price }}$</p>
                <p class="card-text">Tickets available : {{ e.total_available_tickets  }}</p>
                <a href="#" class="btn btn-primary" @click="addToCart(e)" v-if="!is_admin">Add to cart</a>
                <button id="submitArtist" class="btn-success" type="button" name="button" @click="openAddArtist(e)" v-if="is_admin">
                      Add Artist to Event
                </button>
                <button id="submitDeleteArtist" class="btn-secondary" type="button" name="button" @click="openDeleteArtist(e)" v-if="is_admin">
                      Delete Artist in Event
                </button>
                <button id="editEventBtn" class="btn-primary" type="button" name="button" @click="viewEditEvent(e)" v-if="is_admin">
                      EDIT EVENT
                </button>
                <button id="submitDeleteEvent" class="btn-danger" type="button" name="button" @click="deleteEvent(e)" v-if="is_admin">
                      Delete Event
                </button>
              </div>
              <div id="addArtist" v-if="e.showAdd">
                <div class="form-label-group">
                  <label for="artistName">Name</label>
                  <input type="e.artistForm.name" id="artistName" class="form-control" placeholder="Name" required autofocus v-model="e.artistForm.name">
                </div>
                <div class="form-label-group">
                  <label for="artistCountry">Country</label>
                  <input type="e.artistForm.country" id="artistCountry" class="form-control" placeholder="Country" required autofocus v-model="e.artistForm.country">
                </div><div class="form-label-group">
                  <label for="artistGenre">Genre</label>
                  <input type="e.artistForm.genre" id="artistGenre" class="form-control" placeholder="Genre" required autofocus v-model="e.artistForm.genre">
                </div>
                <button class="btn btn-primary" @click="submitArtist(e)">Submit</button>
                <button class="btn btn-danger" @click="initArtistForm(e)">Reset</button>
                <button class="btn btn-secondary" @click="closeAdminArtist(e)">Cancel</button>
              </div>
              <div id="deleteArtist" v-if="e.showDelete">
                <div class="form-label-group">
                  <label for="deleteName">Name</label>
                  <input type="e.deleteForm.name" id="deleteName" class="form-control" placeholder="Name" required autofocus v-model="e.deleteForm.name">
                </div>
                <button class="btn btn-primary" @click="submitDeleteArtist(e)">Submit</button>
                <button class="btn btn-danger" @click="initDeleteForm(e)">Reset</button>
                <button class="btn btn-secondary" @click="closeAdminArtist(e)">Cancel</button>
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
      <button class="btn btn-danger" @click="initEventForm(addEventForm)">Reset</button>
      <button class="btn btn-secondary" @click="viewEvents()">Cancel</button>
    </div>
    <div id="editEvent" style="display: none">
      <h1> SIGN UP </h1>
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
      <button class="btn btn-danger" @click="initEventForm(editEventForm)">Reset</button>
      <button class="btn btn-secondary" @click="viewEvents()">Cancel</button>
    </div>
    <div id="artists" style="display: none">
      <div id="artistCatalog">

        <button id="goToEvents" class="btn-primary" type="button" name="button" @click="viewEvents()">
              GO TO EVENTS
        </button>
        <button id="editNewArtistBtn" class="btn-primary" type="button" name="button" @click="viewAddNewArtist()">
              EDIT ARTIST
        </button>
        <div class="container-fluid d-flex flex-wrap pt-2 pb-3">
          <div class="row">
            <div v-for="a in artists" :key="a.id">
              <div id="aCard" class="card ml-3 mt-3 mb-3 mr-3" style="width: 20rem;">
                <img class="card-img-top" src="../assets/logo.png" alt="Card image cap">
                <div class="card-body">
                  <h5 class="card-title">{{ a.name }}</h5>
                  <p class="card-text">Country : {{ a.country }}</p>
                  <p class="card-text">Genre : {{ a.genre }}</p>
                  <button id="openEditArtist" class="btn-success" type="button" name="button" @click="openEditArtist(a)">
                        Edit artist
                  </button>
                  <button id="deleteGlobalArtist" class="btn-danger" type="button" name="button" @click="deleteGlobalArtist(a)">
                        Delete artist
                  </button>
                </div>
                <div id="editArtist" v-if="a.showEdit">
                  <div class="form-label-group">
                    <label for="editArtistName">Name</label>
                    <input type="e.artistForm.name" id="editArtistName" class="form-control" placeholder="Name" required autofocus v-model="a.globalArtistForm.name">
                  </div>
                  <div class="form-label-group">
                    <label for="editArtistCountry">Country</label>
                    <input type="e.artistForm.country" id="editArtistCountry" class="form-control" placeholder="Country" required autofocus v-model="a.globalArtistForm.country">
                  </div><div class="form-label-group">
                    <label for="editArtistGenre">Genre</label>
                    <input type="e.artistForm.genre" id="editArtistGenre" class="form-control" placeholder="Genre" required autofocus v-model="a.globalArtistForm.genre">
                  </div>
                  <button class="btn btn-primary" @click="submitEditNewArtist(a)">Submit</button>
                  <button class="btn btn-danger" @click="initGlobalArtistForm(a)">Reset</button>
                  <button class="btn btn-secondary" @click="closeAdminGlobalArtist(a)">Cancel</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div id="newArtist" style="display: block">
        <div class="form-label-group">
          <label for="newArtistName">Name</label>
          <input type="newArtist.name" id="newArtistName" class="form-control" placeholder="Name" required autofocus v-model="newArtist.name">
        </div>
        <div class="form-label-group">
          <label for="newArtistCountry">Country</label>
          <input type="newArtist.country" id="newArtistCountry" class="form-control" placeholder="Country" required autofocus v-model="newArtist.country">
        </div>
        <div class="form-label-group">
          <label for="newArtistGenre">Genre</label>
          <input type="newArtist.genre" id="newArtistGenre" class="form-control" placeholder="Genre" required autofocus v-model="newArtist.genre">
        </div>
        <button class="btn btn-primary" @click="submitNewGlobalArtist()">Submit</button>
        <button class="btn btn-danger" @click="initNewArtistForm()">Reset</button>
        <button class="btn btn-secondary" @click="viewArtist()">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      artists: [{
        id: 0,
        name: '',
        country: '',
        genre: '',
        globalArtistForm: {
          name: '',
          country: '',
          genre: ''
        },
        showEdit: 0
      }],
      events: [{
        id: 0,
        name: '',
        artists: [{artist: { name: '', id: 1, country: '', genre: 'cap' }}],
        city: '',
        place: '',
        date: '',
        price: 0,
        total_available_tickets: 0,
        artistForm: {
          name: '',
          country: '',
          genre: ''
        },
        deleteForm: {
          name: ''
        },
        showAdd: 0,
        showDelete: 0
      }],
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
      },
      newArtist: {
        name: '',
        country: '',
        genre: ''
      },
      is_admin: 0
    }
  },
  methods: {
    getArtists () {
      const path = 'http://localhost:5000/artists'
      axios.get(path)
        .then((res) => {
          this.artists.splice(0, this.artists.length)
          let a
          for (a of res.data.artists) {
            this.artists.push({id: a.id, name: a.name, country: a.country, genre: a.genre, globalArtistForm: {name: '', country: '', genre: ''}, showEdit: 0})
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getEvents () {
      const path = 'http://localhost:5000/events'
      axios.get(path)
        .then((res) => {
          this.events.splice(0, this.events.length)
          let ev
          for (ev of res.data.events) {
            this.events.push({id: ev.id, name: ev.name, artists: ev.artists, city: ev.city, place: ev.place, date: ev.date, price: ev.price, total_available_tickets: ev.total_available_tickets, artistForm: {name: '', country: '', genre: ''}, deleteForm: {name: ''}, showAdd: 0, showDelete: 0})
          }
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
          this.getEvents()
          this.getAvailableMoney()
          alert('Order Done')
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error)
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
      this.getTotalTickets()
    },
    viewEvents () {
      document.getElementById('carts').style.display = 'none'
      document.getElementById('addEvent').style.display = 'none'
      document.getElementById('editEvent').style.display = 'none'
      document.getElementById('events').style.display = 'block'
      document.getElementById('artists').style.display = 'none'
      document.getElementById('newArtist').style.display = 'none'
    },
    viewCart () {
      document.getElementById('events').style.display = 'none'
      document.getElementById('addEvent').style.display = 'none'
      document.getElementById('editEvent').style.display = 'none'
      document.getElementById('carts').style.display = 'block'
      document.getElementById('artists').style.display = 'none'
      document.getElementById('newArtist').style.display = 'none'
    },
    viewAddEvent () {
      document.getElementById('events').style.display = 'none'
      document.getElementById('carts').style.display = 'none'
      document.getElementById('editEvent').style.display = 'none'
      document.getElementById('addEvent').style.display = 'block'
      document.getElementById('artists').style.display = 'none'
      document.getElementById('newArtist').style.display = 'none'
    },
    viewAddNewArtist () {
      document.getElementById('events').style.display = 'none'
      document.getElementById('carts').style.display = 'none'
      document.getElementById('editEvent').style.display = 'none'
      document.getElementById('addEvent').style.display = 'none'
      document.getElementById('artists').style.display = 'block'
      document.getElementById('artistCatalog').style.display = 'none'
      document.getElementById('newArtist').style.display = 'block'
    },
    viewArtist () {
      document.getElementById('events').style.display = 'none'
      document.getElementById('carts').style.display = 'none'
      document.getElementById('editEvent').style.display = 'none'
      document.getElementById('addEvent').style.display = 'none'
      document.getElementById('newArtist').style.display = 'none'
      document.getElementById('artistCatalog').style.display = 'block'
      document.getElementById('artists').style.display = 'block'
    },
    viewEditEvent (e) {
      document.getElementById('events').style.display = 'none'
      document.getElementById('carts').style.display = 'none'
      document.getElementById('addEvent').style.display = 'none'
      document.getElementById('editEvent').style.display = 'block'
      document.getElementById('newArtist').style.display = 'none'
      document.getElementById('artists').style.display = 'none'

      this.editEventForm.id = e.id
    },
    logIn () {
      this.$router.replace({path: '/userlogin'})
    },
    logOut () {
      this.user = ''
      this.token = ''
      this.logged = false
      this.is_admin = 0
      this.$router.replace({ path: '/', query: { logged: this.logged } })
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
    openAddArtist (e) {
      e.showAdd = 1
      e.showDelete = 0
    },
    closeAdminArtist (e) {
      e.showAdd = 0
      e.showDelete = 0
    },
    initArtistForm (e) {
      e.artistForm = {
        name: '',
        country: '',
        genre: ''
      }
    },
    submitArtist (e) {
      const parameters = {
        name: e.artistForm.name,
        country: e.artistForm.country,
        genre: e.artistForm.genre
      }
      this.addArtistInEvent(e, parameters)
    },
    addArtistInEvent (e, parameters) {
      const path = `http://localhost:5000/event/` + e.id + '/artist'
      axios.post(path, parameters, {
        auth: {username: this.token}
      })
        .then((res) => {
          console.log('AddArtist success')
          this.getEvents()
          this.getArtists()
          alert('Success')
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          console.log('AddArtist failure')
          alert('Failure')
        })
    },
    initDeleteForm (e) {
      e.deleteForm = {
        name: '',
        id: ''
      }
    },
    openDeleteArtist (e) {
      e.showAdd = 0
      e.showDelete = 1
    },
    submitDeleteArtist (e) {
      var id = 'default'
      let artist
      for (artist of e.artists) {
        if (artist.name === e.deleteForm.name) {
          id = artist.id
        }
      }
      if (id !== 'default') {
        const parameters = {
          name: e.deleteForm.name,
          id: id
        }
        this.deleteArtist(e, parameters)
      } else {
        alert('This artist is not in this event')
      }
      this.initDeleteForm(e)
    },
    deleteArtist (e, parameters) {
      const path = `http://localhost:5000/event/` + e.id + '/artist/' + parameters.id
      axios.delete(path, {
        auth: {username: this.token}
      })
        .then((res) => {
          console.log('DeleteArtist success')
          this.getEvents()
          alert('DeleteArtist Success')
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          console.log('DeleteArtist failure')
          alert('DeleteArtist Failure')
        })
    },
    addEvent (parameters) {
      const path = `http://localhost:5000/event`
      axios.post(path, parameters, {
        auth: {username: this.token}
      })
        .then((res) => {
          console.log('AddEvent success')
          this.getEvents()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
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
    },
    deleteEvent (e) {
      const path = `http://localhost:5000/event/${e.id}`
      axios.delete(path, {
        auth: {username: this.token}
      })
        .then((res) => {
          console.log('deleteEvent success')
          this.getEvents()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          console.log('deleteEvent failure')
        })
    },
    updateEvent (parameters) {
      const path = `http://localhost:5000/event/${this.editEventForm.id}`
      axios.put(path, parameters, {
        auth: {username: this.token}
      })
        .then((res) => {
          console.log('EditEvent success')
          alert('EditEvent success')
          this.getEvents()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          console.log('EditEvent failure')
          alert('EditEvent failure')
        })
    },
    initEventForm () {
      this.addEventForm.name = ''
      this.addEventForm.place = ''
      this.addEventForm.city = ''
      this.addEventForm.date = ''
      this.addEventForm.price = ''
      this.addEventForm.available_tickets = ''
      this.editEventForm.id = ''
      this.editEventForm.name = ''
      this.editEventForm.place = ''
      this.editEventForm.city = ''
      this.editEventForm.date = ''
      this.editEventForm.price = ''
      this.editEventForm.available_tickets = ''
    },
    initGlobalArtistForm (a) {
      a.globalArtistForm.name = ''
      a.globalArtistForm.country = ''
      a.globalArtistForm.genre = ''
    },
    deleteGlobalArtist (a) {
      const path = `http://localhost:5000/artist/` + a.id
      axios.delete(path, {
        auth: {username: this.token}
      })
        .then((res) => {
          console.log('global delete artist success')
          this.getArtists()
          this.getEvents()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          console.log('global delete artist failure')
        })
    },
    closeAdminGlobalArtist (a) {
      a.showEdit = 0
    },
    openEditArtist (a) {
      a.showEdit = 1
    },
    submitEditNewArtist (a) {
      const parameters = {
        name: a.globalArtistForm.name,
        country: a.globalArtistForm.country,
        genre: a.globalArtistForm.genre
      }
      this.editGlobalArtist(a, parameters)
      this.initGlobalArtistForm(a)
    },
    editGlobalArtist (a, parameters) {
      const path = `http://localhost:5000/artist/` + a.id
      axios.put(path, parameters, {
        auth: {username: this.token}
      })
        .then((res) => {
          console.log('editGlobalArtist success')
          this.getArtists()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          console.log('editGlobalArtist failure')
        })
    },
    submitNewGlobalArtist () {
      const parameters = {
        name: this.newArtist.name,
        country: this.newArtist.country,
        genre: this.newArtist.genre
      }
      this.newGlobalArtist(parameters)
      this.initNewArtistForm()
    },
    newGlobalArtist (parameters) {
      const path = `http://localhost:5000/artist`
      axios.post(path, parameters, {
        auth: {username: this.token}
      })
        .then((res) => {
          console.log('AddArtist success')
          this.getArtists()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          console.log('AddArtist failure')
        })
    },
    initNewArtistForm () {
      this.newArtist.name = ''
      this.newArtist.country = ''
      this.newArtist.genre = ''
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
    getTotalTickets () {
      this.tickets_added = 0
      let order
      for (order of this.cartItems) {
        this.tickets_added += order.quantity
      }
    }
  },
  created () {
    console.log('CREATED: ' + JSON.stringify(this.events))
    this.getEvents()
    this.getArtists()
    this.cartItems = []
    this.logged = this.$route.query.logged
    this.username = this.$route.query.username
    this.is_admin = this.$route.query.is_admin
    this.token = this.$route.query.token
    this.getAvailableMoney()
  }
}
</script>
