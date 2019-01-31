
// Music player
var x = document.getElementById("myAudio");

function playAudio() {
    document.getElementById('play').style.display='none';
    document.getElementById('stop').style.display='block';
    x.play();
}

function pauseAudio() {
    document.getElementById('stop').style.display='none';
    document.getElementById('play').style.display='block';
    x.pause();
}

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
        editColumn: -1,
        editBoard: -1,
        editCard: -1,
        spans: document.getElementsByClassName("span1"),
        drag: false,
        // boards: sampleData.boards,

        // columns: ['El sem indult', 'Kicsit késik', 'Sokat késik', 'Eltűnt'],
        boards: [
            {id: 1, title: 'MÁV' , columns: [
                {id: 1, title: 'El sem indult', cards: [
                    {title:"John", id:1},
                    {title:"Joao", id:2},
                    {title:"Jean", id:3},
                    {title:"Gerard", id:4} ]},
                {id: 2, title: 'Kicsit késik', cards: [
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
             if (this.newBoard) {
                this.boards.unshift({ title: this.newBoard, id:this.boards.length + 1, columns:[]})
                this.newBoard = null
            }

        },
        rename(id,wichdata) {
            if (wichdata === 'card') {
                this.editCard = id
            } else if (wichdata === 'board') {
                this.editBoard = id
            } else {
                this.editColumn = id
            }
        },
        deleteBoard(id) {
            this.boards = _.filter(this.boards,item => item.id !== id)
          },
        handleEnter(event) {
            let key = event.key || event.keyCode;
            if (key === 'Enter' || key === 13) {
                this.editBoard = this.editCard = this.editColumn = 0;
            }
          },
        addColumn(board) {
            if (this.newColumn === 'Arrived on time' || this.newColumn === 'Időben érkezett' ) {
               $('#modalWarning').modal('show')
               return
            }else if (this.newColumn) {
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