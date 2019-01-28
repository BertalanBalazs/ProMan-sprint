

var app = new Vue({
    el: '#app',
    components:{
      // draggable
    },
    data: {
        drag: false,
        boards: sampleData.boards,
        columns: ['El sem indult', 'Kicsit késik', 'Sokat késik', 'Eltűnt']
    },
    methods: {
        addBoard() {
            this.boards.push({ title: 'Board ' + (this.boards.length + 1), id:this.boards.length + 1})
        }
    }
})


// This function is to initialize the application
/*
function init() {
    // init data
    dataHandler.init();
    // loads the boards to the screen
    dom.loadBoards();

}

init();
*/