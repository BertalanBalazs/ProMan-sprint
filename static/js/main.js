

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
        async addBoard() {
            console.log(await $.ajax({
                url: 'http://127.0.0.1:5000/cards/4',
                type: 'DELETE'
            }))
        }
    }
});


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