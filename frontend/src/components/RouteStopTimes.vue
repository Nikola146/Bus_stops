<template>
  <div class="col p-3">
    <h2 v-if="sortedStopTimes.length > 1">{{ sortedStopTimes.length }} lähimat saabumisaega</h2>
    <h2 v-else>Saabumisaeg</h2>
  </div>
  <div class="accordion" id="timeAccordion">
    <div v-for="stopTime of sortedStopTimes" :key="stopTime.id" class="accordion-item">
      <h2 :id="`heading-${stopTime.id}`" class="accordion-header">
        <button v-if="isNextDay(stopTime.arrival_time)" :aria-controls="`time-${stopTime.id}`" :data-bs-target="`#time-${stopTime.id}`"
                aria-expanded="false"
                class="accordion-button collapsed" data-bs-toggle="collapse" type="button">
          <span class="text-danger">{{ normalizeTime(stopTime.arrival_time) }} <span
              class="badge bg-danger">Next day</span></span>
        </button>
        <button v-else :aria-controls="`time-${stopTime.id}`" :data-bs-target="`#time-${stopTime.id}`" aria-expanded="false"
                class="accordion-button collapsed" data-bs-toggle="collapse" type="button">
          {{ normalizeTime(stopTime.arrival_time) }}
        </button>
      </h2>
      <div :id="`time-${stopTime.id}`" :aria-labelledby="`time-${stopTime.id}`" class="accordion-collapse collapse"
           data-bs-parent="#timeAccordion">
        <div class="accordion-body">
          <table class="table table-hover">
            <thead>
            <th class="col-1">#</th>
            <th class="col-8 text-start">Stop Name</th>
            <th class="col-3">Time</th>
            </thead>
            <tbody>
            <template v-for="relatedTime of sortByStopSequence(stopTime.related_times)" :key="relatedTime.id">
              <tr :class="{'table-active': relatedTime.id === stopTime.id, 'opacity-50': (relatedTime.id !== stopTime.id && relatedTime.stop_sequence < stopTime.stop_sequence), 'fw-bold': relatedTime.id === stopTime.id}">
                <th scope="row"> {{ relatedTime.stop_sequence }}</th>
                <td class="text-start">{{ relatedTime.stop.stop_name }}</td>
                <td :class="{'text-danger': isNextDay(relatedTime.arrival_time)}">
                  {{ normalizeTime(relatedTime.arrival_time) }}
                </td>
              </tr>
            </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'RouteStopTimes',
  props: {
    stopTimes: {}
  },
  computed: {
    sortedStopTimes() {
      return this.stopTimes.slice().sort((a, b) => {
        // Split the arrival time strings into hours, minutes and seconds
        const [aHours, aMinutes, aSeconds] = a.arrival_time.split(':');
        const [bHours, bMinutes, bSeconds] = b.arrival_time.split(':');

        // Compare the hours
        if (aHours !== bHours) {
          return aHours - bHours;
        }

        // If the hours are the same, compare the minutes
        if (aMinutes !== bMinutes) {
          return aMinutes - bMinutes;
        }

        // If the hours and minutes are the same, compare the seconds
        return aSeconds - bSeconds;
      });
    },
  },
  methods: {
    sortByStopSequence(arr) {
      return arr.sort((a, b) => a.stop_sequence - b.stop_sequence);
    },
    isNextDay(time) {
      return Number(time.slice(0, -6)) >= 24;
    },
    normalizeTime(timeString) {
      // Split the time string into hours, minutes, and seconds
      // eslint-disable-next-line no-unused-vars
      let [hours, minutes, seconds] = timeString.split(":");

      // Convert the hours, minutes, and seconds to integers
      hours = parseInt(hours, 10);

      // If the hours are greater than 24, reduce them by 24
      if (hours >= 24) {
        hours -= 24;
      }
      if (hours >= 24) {
        hours -= 24;
      }

      // Return the normalized time string
      return `${hours.toString().padStart(2, "0")}:${minutes}`;
    }

  }

}
</script>
