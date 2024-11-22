<template>
    <div class="w-full flex relative">
      <div class="w-screen flex-col">
        <!-- Horizontal Bar for the sheet -->
        <div
          class="w-full flex flex-row border border-gray-500"
          :width="sheetWidth"
        >
          <div class="px-2 basis-1/12 border-x-2 border-gray-500">
            {{ choosenCellKey }}
          </div>
          <div class="flex flex-row basis-5/6 gap-2 items-center">
            <FunctionSquare :size="24" />
            {{ currentFormula }}
          </div>
        </div>
        <!-- datatable -->
        <div ref="datatable" id="sheet"></div>
  
        <!-- footer with sheet names -->
        <div
          class="w-full flex items-center absolute bottom-0 left-0 right-0 border-2 border-grey bg-white z-10"
        >
          <Button
            :variant="'subtle'"
            :ref_for="true"
            theme="white"
            size="sm"
            label="Button"
            :loading="false"
            :loadingText="null"
            :disabled="false"
            :link="null"
            @click="createNewSheet()"
          >
            <Plus :size="20"></Plus>
          </Button>
          <!-- <Tabs v-model="tabIndex" v-slot="{ tab }" :tabs="tabs"/> -->
        </div>
      </div>
      <div
        class="sm:flex flex-col items-center overflow-hidden h-full min-w-[16px] gap-1 pt-3 px-0 border-l absolute right-0 bg-white"
      >
        <Button
          class="text-gray-600"
          :class="['text-black bg-whitete-200']"
          variant="minimal"
          @click="switchTab(1)"
        >
          Hello
        </Button>
        <Button
          class="text-gray-600"
          :class="['text-black bg-white-200']"
          variant="minimal"
          @click="switchTab(2)"
        >
        </Button>
        <Button
          class="text-gray-600"
          :class="['text-black bg-white-200']"
          variant="minimal"
          @click="switchTab(1)"
        >
        </Button>
        <Button
          class="text-gray-600"
          :class="['text-black bg-white-200']"
          variant="minimal"
          @click="switchTab(1)"
        >
        </Button>
        <Button
          class="text-gray-600"
          :class="['text-black bg-white-200']"
          variant="minimal"
          @click="switchTab(1)"
        >
        </Button>
        <Button
          class="text-gray-600"
          :class="['text-black bg-white-200']"
          variant="minimal"
          @click="clickHandler('Erase')"
        >
        </Button>
        <Button
          class="text-gray-600"
          :class="['text-black bg-white-200']"
          variant="minimal"
          @click="clickHandler('Clear')"
        >
        </Button>
      </div>
      <div class="formula-suggest">02</div>
    </div>
  </template>
  

<script>
import Tabs from "frappe-ui/src/components/Tabs.vue"
import { FunctionSquare, Plus } from "lucide-vue-next"
export default {
  name: "Datatable",
  components: {
    Tabs,
    Plus,
    FunctionSquare,
  },
  props: {
    sheet: Object
  },
  data() {
    return {
      sengine:null,
      workbook: null,
      dt_container: null,
      choosenCellKey: "A1",
      currentFormula: " ",
      sheets:[],
      sheetNames:[],
      activeSheetIndex:0,
      datatableObject:null,
      datatableContainer:null,  
      current:{
        sheet: 0,
        datatableObject:0,
        datatableContainer:0,
        sheetIndex: 0
      },   
      tabs: [
        {
          label: "Sheet 1",
        },
      ],
      isVisible: false,
      tabIndex: 0,
      tab: 0,
      sheetWidth: 100,
      currentSheet: null,
      cell:{
        editor:null,
        editorProps:null,
        formulas:null,
        cellChoosing: false,
        suggestion :[],
        selectedCells:[],
        cellContent:null,
        oldState:null,
      },
      currentSheetContent:null,
      formulaSuggest: this.$refs.formulaSuggest,
      formulaSuggestions: [],
      currentSheetIndex:0
    }
  },
  watch: {
    tabIndex(newValue, oldValue){
      console.log(newValue,oldValue)
    }
  },
  mounted() {
    this.sengine = new Engine()
    console.log(this.sengine)
    this.formulas = this.sengine.formulas
    this.workbook = this.sengine.createWorkbook("Untitled Spreadsheet")
    let sheetOne = this.workbook.addSheet()
    this.datatableContainer = this.$refs.datatable

    this.currentSheet = sheetOne
    this.sheets.push(sheetOne)
    this.sheetNames = this.workbook.getSheetNames()
    this.tabs = [],
    this.sheetNames.forEach(name =>{
      let temp = {
        label: name
      }
      this.tabs.push(temp)
    })
    this.currentSheetIndex = this.tabIndex
    let data = sheetOne.initSheet()
    let columns = this.createLetterHeadings()
    let datatable = new DataTable("#sheet", {
        columns: columns,
        data: data,
        fullHeight: true,
        inlineFilters: true,
        reactive: true,
        cellHeight: 25,
        pasteFromClipboard: true,
        formulas:this.sengine.formulas,
        argSuggestion: this.sengine.argSuggestions,
        scanner: sheetOne.scan,
    })

    this.datatableObject = datatable
    // this.createNewSheet()
    this.bindEventListners()
  },
  methods: {
    createNewSheet(){
      let sheetObj = this.workbook.addSheet()
      let temp = {
        index: this.sheetNames.length,
        sheet:sheetObj
      }
      this.sheets.push(temp)
      console.log(this.sheets)
      this.sheetNames = this.workbook.getSheetNames()
      console.log(this.$refs)
      console.log(this.$refs[`datatable${this.sheetNames.length}`])
     
      this.tabs = []
      this.sheetNames.forEach(name =>{
        let temp = {
          label: name
        }
        this.tabs.push(temp)
      })
  // boreder text formating, auto-range, copy-paste from gs
      
      let data = sheetObj.initSheet()
      let columns = this.createLetterHeadings()
      console.log(this.refs)
      this.datatableContainers.push(this.$refs[`datatable${this.sheetNames.length}`])
      console.log("#sheet"+ this.sheetNames.length)
      let datatable = new DataTable("#sheet"+ this.sheetNames.length, {
        columns: columns,
        data: data,
        fullHeight: true,
        inlineFilters: true,
        reactive: true,
        cellHeight: 25,
        pasteFromClipboard: true,
      })
      this.datatableObjects.push(datatable)

      this.tabIndex = this.sheetNames.length - 1

    },
    createLetterHeadings() {
      let columns = []
      for (let n = 0; n < 26; n++) {
        columns.push({
          name: String.fromCharCode(65 + n),
          width: 100,
          dropdown: false,
        })
      }
      return columns
    }, 
    rowcolToA1(row,col){
      row = parseInt(row)
      col = parseInt(col)
      return `${String.fromCharCode(64+col)}${row+1}`
    },
    toggleFormulaSuggest(show,settings){
      if (show) {
            this.isVisible = true
            let formulaSuggestBoxPos = {
                top: settings.top + settings.height,
                left: settings.left,
            };
            this.datatable.$.style(this.$refs.formulaSuggest, formulaSuggestBoxPos);
        } else {
            this.isVisible = false
            // datatable.$.style(formulaSuggest, { display: 'none'});
        }
    },
    getFormula(formulaName,formulaDesc){
        let div = document.createElement('div');
        div.setAttribute('class', 'formula');
        div.setAttribute('id', formulaName);
        let name = document.createTextNode(formulaName);
        div.appendChild(name);
        let inside_div = document.createElement('div');
        let para = document.createElement('p');
        para.setAttribute('class', 'formula-description');
        para.textContent = formulaDesc;
        inside_div.appendChild(para);

        let hr = document.createElement('hr');
        inside_div.appendChild(hr);
        div.appendChild(inside_div);
        return div;
    },
    suggestFormula(editor){

      let value = editor.value
      console.log(this.formulas)
    if (value.length > 1) {
        // display the ui for
        let formulaSuggest = document.getElementById("formulaSugggest")
        let parentElementPosition = editor.parentElement.getBoundingClientRect();
        let allAvalibleFormulas = Object.keys(this.formulas);
        let searchTerm = editor.value.replace('=', '').toLowerCase().split("(")[0];
        let searchRegex = new RegExp(`^${searchTerm}`,"i");
        const matches = allAvalibleFormulas.filter(value => searchRegex.test(value));
        // console.log(matches);
        if (matches.length > 0) {
            let tokens = this.currentSheet.scan(value.replace("=",""))
            console.log(tokens)
            let openBracket = tokens.find(token => token.type === 17)
            let closeBracket = tokens.find(token=> token.type === 18)
            if(closeBracket){
              this.toggleFormulaSuggest(false)
            }
            console.log(openBracket)
            if(openBracket){
              this.$refs.formulaSuggest.style.width = "500px"
              this.$refs.formulaSuggest.style.height = "20px"
                let options = suggestions.filter(el => {
                    return searchRegex.test(el.name)
                })
                console.log(options)
                if(options.length > 0){
                    console.log(value)
                    console.log(options[0])
                    createSuggestion(options[0])
                    let noofCommas = tokens.find(token => token.type === 22)
                    suggestArgs(value,noofCommas)
                }
            }else{
              if(this.cell.oldState){
                this.$refs.formulaSuggest.style.width = this.cell.oldState.width
                this.$refs.formulaSuggestt.style.height = this.cell.oldState.height
              }
              let settings = {
                  left: parentElementPosition.left,
                  top: parentElementPosition.top,
                  height: parentElementPosition.height
              };

              this.$refs.formulaSuggest.innerHTML = '';
              this.toggleFormulaSuggest(true, settings);
              matches.forEach(match =>{
                  let temp = {
                    name:match,
                    desc:this.formulas[match].desc
                  }
                  this.formulaSuggestions.push(temp)
                  let formulaList = this.getFormula(match, this.formulas[match].desc);
                  // add a click event listner for actaully choosing the suggestion
                  formulaList.addEventListener('click', event =>{
                      formulaChooser(event, editor);
                  });
                  this.formulaSuggest.appendChild(formulaList);
              });
              let style = getComputedStyle(this.$refs.formulaSuggest)
              this.cell.oldState = {
                width: style.width,
                height: style.height
              }
            }
        } else {
            this.formulaSuggestions = []
            this.formulaSuggest.innerHTML = '';
            this.toggleFormulaSuggest(false);
        }
    } else {
        this.formulaSuggestions = []
        this.$refs.formulaSuggest.innerHTML = '';
        this.toggleFormulaSuggest(false);
    }
    },
    bindEventListners(){
      const datatable_wrapper = this.$refs.datatable
      const that = this
      // focusCell event
      datatable_wrapper.addEventListener("focusCell", function(event){
        console.log("hello")
        let cellIndex =  event.detail
        let choosenKey = that.rowcolToA1(cellIndex.rowIndex,cellIndex.colIndex)
        let cell = that.currentSheet.getCell(choosenKey)
        console.log(choosenKey)
        that.choosenCellKey = choosenKey
        if(cell){
          console.log(cell)
          that.currentFormula = cell.rawFormulaText

        }
      })

      datatable_wrapper.addEventListener("cellEditing",function(event){
          that.cell.editor = event.detail
          let value = that.cell.editorProps.getValue()
          if(value.charAt(0) === "="){
              that.cell.cellContent = that.cell.editorProps.getValue()
              if(that.datatable.getCellChoosen()){
                that.suggestFormula(that.cell.editor)
              }else{
                that.datatable.startCellChoosing()
                that.suggestFormula(that.cell.editor)
              }
          }else{
              that.datatable.stopCellChoosing()
          }
      })

      datatable_wrapper.addEventListener("activateEditing", function(event){
          that.cell.editorProps = event.detail
      })

    }
  },
}
</script>
