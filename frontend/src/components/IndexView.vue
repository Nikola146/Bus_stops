<template>
  <div class="container mx-auto w-80 mb-5 shadow-lg  bg-body rounded-5 overflow-hidden">
    <div class="row no-gutters">
      <div class="col-6 p-3 mt-3 mb-3">
        <h1><b>🗓️ Bus timetable</b></h1>
        <div class="col mt-2 text-end">
          <button v-if="selectedBus || selectedStop || selectedRegion" class="btn btn-outline-secondary ms-2 me-2"
                  @click="clearForm">🧹 Clear
          </button>
          <button class="btn btn-outline-secondary"
                 @click="getNearestRegionStops" :disabled="nearestStopLoading">
            <span v-if="nearestStopLoading" class="spinner-grow spinner-grow-sm"></span>
            {{ nearestStopLoading ? 'Looking for stops' : '📍 Get nearest stop' }}
          </button>
        </div>

        <div class="col mt-5">
          <label class="form-label" for="exampleDataList">🌍 Regions</label>
          <v-select v-model="selectedRegion" :filter="sortList"
                    :options="regionSuggestions" class="mb-2">
            <!-- eslint-disable-next-line vue/no-unused-vars  -->
            <template #no-options="{ search, searching, loading }">
              Start enter a region
            </template>
          </v-select>
          <button :disabled="selectedRegion === null" class="btn btn-primary"
                  @click="getStopsByCity(selectedRegion)">
            Show stops for this region
          </button>
        </div>

        <div v-if="stopSuggestionLoading" class="col mt-5 progress">
          <div aria-valuemax="100" aria-valuemin="0" aria-valuenow="100"
               class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
               style="width: 100%"></div>
        </div>

        <div v-if="stopSuggestions.length !== 0 && selectedRegion" class="col mt-5">
          <label class="form-label" for="exampleDataList">🚏 Stops</label>
          <v-select v-model="selectedStop" :filter="sortStops" :get-option-label="getStopSuggestionLabel"
                    :options="stopSuggestions" class="mb-2">
            <!-- eslint-disable-next-line vue/no-unused-vars  -->
            <template #no-options="{ search, searching, loading }">
              Start enter a stop 🚏
            </template>
          </v-select>
          <button :disabled="selectedStop === null" class="btn btn-primary" @click="getRoutes(selectedStop.id)">
            Submit selected stop
          </button>
        </div>

        <div v-show="busSuggestionLoading" class="col mt-5 progress">
          <div aria-valuemax="100" aria-valuemin="0" aria-valuenow="100"
               class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
               style="width: 100%"></div>
        </div>

        <div v-if="busSuggestions.length > 0 && selectedStop" class="col mt-5">
          <div>
            <label class="form-label" for="exampleDataList">🚌 Busses</label>
          </div>
          <template v-for="busSug of busSuggestions" :key="busSug.id">
            <button :class="getClassByColorHash(busSug.route_color, busSug.id)" class="btn m-1"
                    @click="getNextStopTimes(selectedStop.id, busSug.id)">🚍 {{
                busSug.route_short_name
              }}
            </button>
          </template>
        </div>

      </div>


      <div class="col-6 p-0 shadow">
        <div v-if="stopTimes.length === 0" class="vh-100 position-relative">
          <div v-show="stopTimesLoading" class="spinner-grow text-white position-absolute top-50 left-50"
               role="status" style="width: 3rem; height: 3rem; z-index: 2">
            <span class="visually-hidden">Loading...</span>
          </div>
          <div :class="{'opacity-25': !stopTimesLoading, 'opacity-75': stopTimesLoading}"
               class="vh-100 vw-100 position-absolute bg-dark" style="z-index: 1"></div>
          <div class="image-container"></div>
        </div>
        <div v-else class="container p-0">
          <div class="row">
            <route-stop-times :stop-times="stopTimes"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>


import axios from "axios";
import vSelect from "vue-select";
import RouteStopTimes from "@/components/RouteStopTimes";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

export default {
  name: "IndexView",

  components: {
    vSelect,
    RouteStopTimes
  },
  data() {
    return {
      nearestStopLoading: false,
      selectedRegion: null,
      regionSuggestions: [],
      stopSuggestionLoading: false,
      selectedStop: null,
      stopSuggestions: [],
      busSuggestionLoading: false,
      selectedBus: null,
      busSuggestions: [],
      stopTimesLoading: false,
      stopTimes: []
    }
  },
  async mounted() {
    await this.getCity();
  },
  watch: {
    selectedRegion() {
      console.log(this.stopSuggestions.length)
      if (!this.nearestStopLoading)
      {
        this.stopSuggestions = []
        this.selectedStop = null
      }
      this.busSuggestions = []
      this.stopTimes = []
      this.selectedBus = null
    },
    selectedStop() {
      this.busSuggestions = []
      this.stopTimes = []
      this.selectedBus = null
    },
    stop() {
      console.log(this.stop)
    }
  },
  methods: {
    getGeolocation() {
      const geolocationOptions = {
        enableHighAccuracy: true,
        maximumAge: 10000,
        timeout: 10000,
      };
      if (navigator.geolocation) {
        return new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(function (position) {
            resolve({
              latitude: position.coords.latitude,
              longitude: position.coords.longitude
            });
          }, function (error) {
            reject(error);
          }, geolocationOptions);
        });
      } else {
        return Promise.reject('Geolocation is not supported by this browser.');
      }
    },
    async getNearestRegionStops(){
      this.nearestStopLoading = true
      const location = await this.getGeolocation()
      axios.post('api/coordinates/', {
        latitude: location.latitude,
        longitude: location.longitude
      }).then((response) => {
        if (response.data.region && response.data.stops)
        {
          this.selectedRegion = response.data.region
          this.stopSuggestions = response.data.stops
          this.selectedStop = response.data.nearest_stop
        }
      }).finally(() => this.nearestStopLoading = false)
    },
    clearForm() {
      this.selectedRegion = null
      this.selectedStop = null
      this.selectedBus = null
      this.busSuggestions = []
      this.stopSuggestions = []
      this.stopTimes = []
    },
    sortList(arr, startWith) {
      // Convert the startWith string to lowercase
      startWith = startWith.toLowerCase();

      // Filter the array by those that start with the given string (case-insensitive)
      let filtered = arr.filter(function (str) {
        return str.toLowerCase().startsWith(startWith);
      });

      // Sort the resulting array alphabetically
      filtered.sort();

      // Return the sorted array
      return filtered;
    },
    sortStops(arr, startWith) {
      // Convert the startWith string to lowercase
      startWith = startWith.toLowerCase();

      // Filter the array by those that start with the given string (case-insensitive)
      let filtered = arr.filter(function (str) {
        return str.stop_name.toLowerCase().startsWith(startWith);
      });

      // Sort the resulting array alphabetically
      filtered.sort();

      // Return the sorted array
      return filtered;
    },
    async getCity() {
      try {
        const response = await axios.get(`api/stops/list/`);
        this.regionSuggestions = response.data;
      } catch (error) {
        this.errorMessage = 'An error occurred while retrieving the regions';
      }

    },
    async getStopsByCity(selectedRegion) {
      this.stopSuggestionLoading = true;
      this.stopSuggestions = []
      try {
        const response = await axios.get(`api/stops/area/${selectedRegion}/`);
        this.stopSuggestions = response.data;
      } catch (error) {
        this.errorMessage = 'An error occurred while retrieving the regions';
      } finally {
        this.stopSuggestionLoading = false;
      }

    },
    getStopSuggestionLabel(stop) {
      let label = `${stop.stop_name}`
      if (stop.stop_desc) {
        label += `, ${stop.stop_desc}`
      }
      label += `, ${stop.stop_code}`
      return label
    },
    async getRoutes(stop_id) {
      this.busSuggestionLoading = true;
      this.busSuggestions = []
      try {
        const response = await axios.get(`api/routes/${stop_id}/`);
        this.busSuggestions = response.data;
        this.busSuggestions.sort((a, b) => {
            if (a.route_short_name < b.route_short_name) {
              return -1;
            }
            if (a.route_short_name > b.route_short_name) {
              return 1;
            }
            return 0;
          })
      } catch (error) {
        this.errorMessage = 'An error occurred while retrieving the regions';
      } finally {
        this.busSuggestionLoading = false;
      }
    },
    getClassByColorHash(color_hash, bus_id = 0) {
      let value = "btn-outline-secondary"
      if (color_hash === '3bb5db') {
        value = "btn-outline-info"
      } else if (color_hash === '660000') {
        value = "btn-outline-danger"
      } else if (color_hash === 'de2c42') {
        value = "btn-outline-warning"
      } else {
        console.log(color_hash)
        value = "btn-outline-secondary"
      }
      if (bus_id === this.selectedBus) {
        value = value.replace('-outline-', '-')
      }
      return value
    },
    // eslint-disable-next-line no-unused-vars
    async getNextStopTimes(stop_id, route_id) {
      this.selectedBus = route_id
      this.stopTimes = []
      try {
        this.stopTimesLoading = true;
        const response = await axios.get(`api/next-stoptimes/${stop_id}/${route_id}/`);
        this.stopTimes = response.data;
      } catch (error) {
        this.errorMessage = 'An error occurred while retrieving the regions';
      } finally {
        this.stopTimesLoading = false;
      }
    }

  },
}
</script>

<style>
@import "vue-select/dist/vue-select.css";

.image-container {
  background-image: url("../assets/image_2024-01-23_19-05-04.png");
  width: 100%;
  height: 100%;
  background-size: repeat;
}
</style>