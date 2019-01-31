
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
        newCard: {},
        isEdit: 0,
        spans: document.getElementsByClassName("span1"),
        drag: false,
        // boards: sampleData.boards,

        // columns: ['El sem indult', 'Kicsit késik', 'Sokat késik', 'Eltűnt'],
        boards: [
            {id: 1, title: 'MÁV' , columns: [
                {id: 1, title: 'El sem indult', cards: [
                    {title:"Thomas", id:1, image:"https://d2eixtdner5dzd.cloudfront.net/cache/cf/08/cf0811580c772f9c26e34cbaca3ab78b.png"},
                    {title:"James", id:2, image:"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScAC8xZf1wlij4vruLWlsLMb50UfRZf2ES2CRQmwymh4Z3b2tyWQ"},
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
        async selectBoard(board) {
            let newBoard = _.cloneDeep(board)
            console.log('board')
            const data = await fetch('http://127.0.0.1:8000/statuses')  // set the path; the method is GET by default, but can be modified with a second parameter
            .then((response) => response.json())
            console.log(data)
            board.columns = data.result
        },
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
        deleteBoard(id) {
            this.boards = _.filter(this.boards,item => item.id !== id)
          },
        rename(id) {
            this.isEdit = id;
        },
        handleEnter(event) {
            let key = event.key || event.keyCode;
            if (key === 'Enter' || key === 13) {
                this.isEdit = 0;
            }
          },
        addColumn(board) {
            if (this.newColumn === 'Arrived on time' || this.newColumn === 'Időben érkezett' ) {
               $('#modalWarning').modal('show')
               return
            }else if (this.newColumn) {
                board.columns.unshift({ title: this.newColumn, id:board.columns.length + 1, cards:[]})
                this.newColumn = null
            }
        },
        addCard(column) {
            if (this.newCard[column.id]) {
                column.cards.unshift({ title: this.newCard[column.id], id:column.cards + 1})
                this.newCard[column.id]= null
            }
        }
    },
    async mounted () {
        let data = await fetch('http://127.0.0.1:8000/boards')  // set the path; the method is GET by default, but can be modified with a second parameter
        .then((response) => response.json())
        let data2 = data.result
         for (const item of data2) {
            item.columns = []
        }
        this.boards = data2

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