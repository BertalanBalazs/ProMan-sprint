// Music player
var x = document.getElementById("myAudio");


function playAudio() {
    document.getElementById('play').style.display = 'none';
    document.getElementById('stop').style.display = 'block';
    x.play();
}


function pauseAudio() {
    document.getElementById('stop').style.display = 'none';
    document.getElementById('play').style.display = 'block';
    x.pause();
}

const socket = io.connect('http://localhost:8000');
socket.on('boardlist-change', async function () {
    await app.loadData()
});
socket.on('board-change', async function () {
    console.log("fos");
    for (let i = 0; i < app.allBoard.length; i++) {
        let board = app.allBoard[i];
        if (board.isActive) {
            await app.refreshBoard(board);
        }
    }
})

var app = new Vue({
    el: '#app',
    authenticated: false,
    components: {
        // draggable
    },
    data: {
        allBoard: [],
        list1: [],
        list2: [{name: "Juan", id: 5},
            {name: "Edgard", id: 6},
        ],
        newBoard: null,
        newColumn: null,
        newCard: {},
        isEdit: 0,
        editColumn: -1,
        editBoard: -1,
        editCard: -1,
        spans: document.getElementsByClassName("span1"),
        drag: false,
        authenticated: null,
        columnsBeforeDrag: null,
        // boards: sampleData.boards,

        // columns: ['El sem indult', 'Kicsit késik', 'Sokat késik', 'Eltűnt'],

        columns: [
            {title: 'El sem indult', cards: ['Thomas', 'Rosie', 'Edward', 'Henry', 'Gordon', 'James']},
        ],
        // cards: ['Thomas', 'Rosie', 'Edward', 'Henry', 'Gordon', 'James']
    },
    computed: {
        boards() {
            let boards = _.filter(this.allBoard, {user_id: 0})
            if (this.authenticated) {
                const user = document.getElementById('showusername')

                let userBoards = _.filter(this.allBoard, {user_id: _.toNumber(user.dataset.userid)})
                console.log(userBoards)
                return [...boards, ...userBoards]
            } else return boards
        }
    },
    methods: {

        async selectBoard(board) {

            if (board.isActive == false) await this.refreshBoard(board);

            board.isActive ? board.isActive = false : board.isActive = true;

        },
        async refreshBoard(board) {
            let columns = await fetch(`http://127.0.0.1:8000/statuses/${board.id}`)  // set the path; the method is GET by default, but can be modified with a second parameter
                .then((response) => response.json())
            columns = columns.result
            let cards = await fetch(`http://127.0.0.1:8000/cards?board_id=${board.id}`)  // set the path; the method is GET by default, but can be modified with a second parameter
                .then((response) => response.json())
            cards = cards.result
            if (columns.length > 0) {
                for (let column of columns) {
                    column.cards = _.filter(cards, {status_id: column.id})
                    if (_.isEmpty(column.cards)) column.cards = []
                }
            }
            board.columns = columns
        },
        closeModalWarning() {
            console.log('close')
            $('#modalWarning').modal('hide')
            this.newBoard = null
        },

        async addBoardPublic() {
            if (this.newBoard) {
                let data = await fetch(
                    'http://127.0.0.1:8000/boards/public',
                    {
                        method: 'POST',
                        body: JSON.stringify({userid: this.authenticated, title: this.newBoard}),
                        mode: "cors",
                        headers: {"Content-Type": "application/json"}
                    }
                )
                    .then((response) => response.json())

                this.boards.push({title: this.newBoard, id: data.result, columns: []})
                this.newBoard = null
            }

        },
        async addBoardPrivate() {
            if (this.newBoard) {
                let data = await fetch(
                    'http://127.0.0.1:8000/boards/private',
                    {
                        method: 'POST',
                        body: JSON.stringify({userid: this.authenticated, title: this.newBoard}),
                        mode: "cors",
                        headers: {"Content-Type": "application/json"}
                    }
                )
                    .then((response) => response.json())
                this.boards.push({title: this.newBoard, id: data.result, columns: []})
                this.newBoard = null
            }

        },
        rename(id, wichdata) {
            if (wichdata === 'card') {
                this.editCard = id
            } else if (wichdata === 'board') {
                this.editBoard = id
            } else {
                this.editColumn = id
            }
        },
        async deleteBoard(id) {
            await fetch(
                `http://127.0.0.1:8000/boards/${id}`,
                {
                    method: 'DELETE',
                    mode: "cors",
                    headers: {"Content-Type": "application/json"}
                }
            );
            await this.loadData()
        },
        handleEnter(event) {
            let key = event.key || event.keyCode;
            if (key === 'Enter' || key === 13) {
                this.editBoard = this.editCard = this.editColumn = 0;
            }
        },
        async addColumn(board) {
            if (this.newColumn === 'Arrived on time' || this.newColumn === 'Időben érkezett') {
                $('#modalWarning').modal('show')
                return
            } else if (this.newColumn) {
                let data = await fetch(
                    'http://127.0.0.1:8000/statuses',
                    {
                        method: 'POST',
                        body: JSON.stringify({boardId: board.id, title: this.newColumn}),
                        mode: "cors",
                        headers: {"Content-Type": "application/json"}
                    }
                );
                board.columns.unshift({title: this.newColumn, id: data.result, cards: []})
                this.newColumn = null
            }
        },
        async addCard(boardId, column) {
            if (this.newCard[column.id]) {
                let data = await fetch(
                    'http://127.0.0.1:8000/cards',
                    {
                        method: 'POST',
                        body: JSON.stringify({
                            board_id: boardId,
                            status_id: column.id,
                            user_id: this.authenticated ? parseInt(this.authenticated) : 0,
                            order_num: 0,
                            title: this.newCard[column.id]
                        }),
                        mode: "cors",
                        headers: {"Content-Type": "application/json"}
                    }
                );
                column.cards.unshift({title: this.newCard[column.id], id: column.cards + 1})
                this.newCard[column.id] = null
            }
        },
        async endDrag(cards, columns) {
            this.drag = false;

            function getdraggedcard(cards) {
                for (let card of app.columnsBeforeDrag) {

                    if (cards.includes(card) == false) return card
                }
                ;
                return false;
            }

            let draggedcard = getdraggedcard(cards);
            let newStatusId;
            for (column of columns) {
                if (column.cards.includes(draggedcard)) newStatusId = column.id;
            }
            let data = await fetch(
                `http://127.0.0.1:8000/cards/${draggedcard.id}`,
                {
                    method: 'PATCH',
                    body: JSON.stringify({statusId: newStatusId}),
                    mode: "cors",
                    headers: {"Content-Type": "application/json"}
                }
            );
            console.log(draggedcard);


        },
        async startDrag(cards) {
            this.drag = true;
            this.columnsBeforeDrag = cards
        },
        async loadData() {
            let data = await fetch('http://127.0.0.1:8000/boards')  // set the path; the method is GET by default, but can be modified with a second parameter
                .then((response) => response.json())
            let data2 = data.result
            for (const item of data2) {
                item.columns = []
                item.isActive = false;
            }
            this.allBoard = data2
            const user = document.getElementById('showusername')
            if (user && user.dataset) {
                this.authenticated = (user.dataset.userid)
            }
        }

    },
    async mounted() {
        await this.loadData()
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