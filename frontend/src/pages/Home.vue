<template>

  <div
    class="sticky top-0 z-10 flex h-12 items-center justify-between border-b-[1px] border-outline-gray-1 bg-surface-white p-2 px-3 py-1"
    >
    Sheets
    <Button :variant="'solid'" :ref_for="true" theme="gray" size="sm" label="Button" :loading="false"
      :loadingText="null" :disabled="false" :link="null" @click="createSpreadsheet">
      + New
    </Button>
  </div>

  <ListView class="mx-10 my-10 w-50 items-center overflow-hidden" :columns="columns" :rows="rows" :options="options" row-key="name" />
</template>
<script>
import { Button , ListView} from "frappe-ui";
import FeatherIcon from "feather-icons";


export default {
  name: "Home",
  components: {
    Button,
    ListView
  },
  data() {
    return {
      columns: [
        {
          label: 'Title',
          key: 'title',
          width: '200px',       
        },
        {
          label: 'Created By',
          key: 'created_by',
          width: '200px',
        },
        {
          label: 'Size',
          key: 'size',
          width: '100px',
        },
        {
          label: 'Last Modified',
          key: 'last_modified',
          width: '250px',
        },
      ],
      rows: [{
          id: 1,
          created_by:"Administrator",
          last_modified: "2024-11-21 13:54:06.688854",
          size: "0 KB",
          title: "Untitled Spreadsheet",
      }],
      options: {
        selectable: false,
        showTooltip: false,
        resizeColumn: false,
      }
    }

  },
  methods: {
    async createSpreadsheet(){

      await this.$resources.createSpreadsheet.submit({
          title: "Untitled Spreadsheet",
          content: null
      })
    },
    humanDate(datestring){
      let dateObj = new Date(datestring)
      const humanReadableDate = dateObj.toLocaleString('en-US', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
      });
      return humanReadableDate
    }
  },

  resources:{
    get_columns(){
      return {
        url: "/api/method/sheets.api.get_ss_fields",
        auto: true,
        onSuccess(data){
          console.log(data)
        }
      }
    },
    fetchSheets(){
      return {
        url: '/api/method/sheets.api.list_spreadsheets',
        method: "GET",
        onSuccess(sheets){
          console.log(sheets)
          this.rows= []
          sheets.forEach((sheet,index) => {
            let temp_row = {
              id: index,
              name: sheet.name,
              title: sheet.title,
              size: `${sheet.size} KB`,
              created_by: sheet.created_by,
              last_modified: this.humanDate(sheet.last_modified)
            }
            console.log(temp_row)
            this.rows.push(temp_row)
          });
        },
        auto: true,
    }
    },
    createSpreadsheet(){
      return {
        url: "/api/method/sheets.api.create_spreadsheet",
        auto: false,
        onSuccess(data){
          console.log(data)
          // router push will happen here
        },
        beforeSubmit(params) {
          console.log("Before sending", params)
        }
      }
    }
  }
};
</script>
