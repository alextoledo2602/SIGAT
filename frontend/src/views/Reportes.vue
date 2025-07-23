<template>
  <div class="reportes">
    <Reports />
  </div>
</template>

<script>
import Reports from '@/components/reports/Reports.vue'
import DashboardLayout from '@/layouts/Layout.vue'
export default {
  name: 'Reportes',
  components: {
    DashboardLayout,
    Reports
  }
}
</script>

<style scoped>
.reportes {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}
</style>