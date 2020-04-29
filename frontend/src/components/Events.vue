<template>
  <div>
    <h1>Events</h1>
    <div class="container-fluid">
      <div class="row">
        <div class="col-lg-4 col-md-6 mb-4" v-for="(event) in events" :key="event.id">
          <div class="card" style="width: 18rem;">
            <img class="card-img-top" src="../assets/logo.png" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">{{ event.name }}</h5>
              <h6 class="card-subtitle">Invited artists : {{ event.artists.toString()}}</h6>
              <p class="card-text">City : {{ event.city }}</p>
              <p class="card-text">Address : {{ event.place }}</p>
              <p class="card-text">Date : {{ event.date }}</p>
            </div>
            <div class="card-body">
              <p class="card-text">{{ event.price  }}$</p>
              <p class="card-text">Tickets available : {{ event.total_available_tickets  }}</p>
              <a href="#" class="btn btn-primary" @click="addToCart(event)">Add to cart</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      events: [{
        name: '',
        artists: [{name: ''}],
        city: '',
        place: '',
        date: '',
        price: 5,
        total_available_tickets: 100
      }
      ],
      events_bought: []
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
      this.events_bought.push(e)
    }
  },
  created () {
    this.getEvents()
    console.log('CREATED: ' + JSON.stringify(this.events))
  }
}
</script>
