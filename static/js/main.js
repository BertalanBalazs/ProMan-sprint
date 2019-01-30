

var app = new Vue({
    el: '#app',
    components:{
      // draggable
    },
    data: {
        list1:[],
		list2:[{name:"Juan", id:5},
				{name:"Edgard", id:6},
        ],
        newBoard: null,
        newColumn: null,
        drag: false,
        // boards: sampleData.boards,

        // columns: ['El sem indult', 'Kicsit késik', 'Sokat késik', 'Eltűnt'],
        boards: [
            { title: 'MÁV' , columns: [
                {title: 'El sem indult', cards: [
                    {title:"John", id:1},
                    {title:"Joao", id:2},
                    {title:"Jean", id:3},
                    {title:"Gerard", id:4} ]},
                {title: 'Kicsit késik', cards: [
                    {title:"Juan", id:5},
				    {title:"Edgard", id:6},
                    ]},

                ]
            }
        ],
        columns: [
            {title: 'El sem indult', cards: ['Thomas', 'Rosie', 'Edward', 'Henry', 'Gordon', 'James']},
        ],
        // cards: ['Thomas', 'Rosie', 'Edward', 'Henry', 'Gordon', 'James']
    },
    methods: {
        closeModalWarning() {
            console.log('close')
            $('#modalWarning').modal('hide')
            this.newBoard = null
        },
        addBoard() {
            if (this.newBoard === 'Arrived on time' || this.newBoard === 'Időben érkezett' ) {
               $('#modalWarning').modal('show')
               return
            } else if (this.newBoard) {
                this.boards.unshift({ title: this.newBoard, id:this.boards.length + 1, columns:[]})
                this.newBoard = null
            }

        },
        addColumn(board) {
            if (this.newColumn) {
                board.columns.unshift({ title: this.newColumn, id:board.length + 1, cards:[]})
                this.newColumn = null
            }
        }
    },
    async mounted () {
        const data = await fetch('/boards')  // set the path; the method is GET by default, but can be modified with a second parameter
        .then((response) => response.json())
        // this.boards = data.result

        /*// parse JSON format into JS object
        .then((data) => {
            this.boards = data.result;
        })*/
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