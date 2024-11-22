<template>
    <div class="flex w-full">
      <Datatable></Datatable>
    </div>
  </template>

<script>
import Datatable from '@/components/Datatable.vue';
export default {
    name: "Spreasheet",
    components: {
        Datatable
    },
    props:{
        sheetId: String
    }

}
</script>

