<template>
  <div class="ingredients-page">
    <h1>Find ingredients</h1>
    <SearchBar
      @input="search"
      @send="search"
    />
    <DataTable
      v-if="ingredients"
      :columns="columns"
      :items="ingredients"
      :actions="actions"
    />
  </div>
</template>

<script>
import SearchBar from '@/components/inputs/SearchBar'
import DataTable from '@/components/lists/DataTable'
import { API } from '@/js/api/api'
import { mapGetters, mapActions } from 'vuex'

export default {

  name: 'Ingredients',

  components: {
    SearchBar,
    DataTable
  },

  computed: mapGetters('user', ['cartContains']),

  data () {
    return {
      searching: false,
      searchTimeout: null,
      columns: [
        { name: 'name', text: 'Name', sortable: true, initiallySorted: true },
        { name: 'quantity', text: 'Quantity' },
        { name: 'price', text: 'Price ($)', sortable: true }
      ],
      ingredients: null,
      actions: {
        isSelected: (ingredient) => this.cartContains(ingredient.id),
        onSelection: (ingredient) => this.addCartItem(ingredient.id),
        onDeselection: (ingredient) => this.removeCartItem(ingredient.id)
      }
    }
  },

  created () {
    this.fetchData()
  },

  watch: {
    '$route': 'fetchData'
  },

  methods: {
    async fetchData () {
      this.ingredients = null
      this.ingredients = await API.getIngredients()
    },
    async search (search) {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(async () => {
        this.ingredients = await API.getIngredientsByName(search)
      }, 300)
    },
    ...mapActions('user', ['addCartItem', 'removeCartItem'])
  }

}
</script>
