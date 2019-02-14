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

var
    app = new Vue({
        el: '#app',
        authenticated: false,
        components: {
            // draggable
        },
        data: {

            allBoard: [],
            list1:
                [],
            list2:
                [{name: "Juan", id: 5},
                    {name: "Edgard", id: 6},
                ],
            newBoard:
                null,
            newColumn:
                null,
            newCard:
                {}
            ,
            isEdit: 0,
            editColumn:
                -1,
            editBoard:
                -1,
            editCard:
                -1,
            spans:
                document.getElementsByClassName("span1"),
            drag:
                false,
            authenticated:
                null,
            columnsBeforeDrag:
                null,
            // boards: sampleData.boards,

            // columns: ['El sem indult', 'Kicsit késik', 'Sokat késik', 'Eltűnt'],

            columns:
                [
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
        }
        ,
        methods: {

            selectBoard(board) {

                if (board.isActive == false) socket.emit('refresh-request', [board.id]);

                board.isActive ? board.isActive = false : board.isActive = true;

            }
            ,
            refreshBoard(board) {
                /*   let columns = await fetch(`http://127.0.0.1:8000/statuses/${board.id}`)  // set the path; the method is GET by default, but can be modified with a second parameter
                       .then((response) => response.json())
                   let cards = await fetch(`http://127.0.0.1:8000/cards?board_id=${board.id}`)  // set the path; the method is GET by default, but can be modified with a second parameter
                       .then((response) => response.json())*/

            },
            saveSocketData(boardId, columns, cards) {
                let board;
                for (let i = 0; i < this.allBoard.length; i++) {
                    let item = this.allBoard[i];
                    if (item.id === boardId) {
                        board = item
                    }
                }
                if (columns.length > 0) {
                    for (let column of columns) {
                        column.cards = _.filter(cards, {status_id: column.id})
                        if (_.isEmpty(column.cards)) column.cards = []
                    }
                }

                if (columns) board.columns = columns
            },
            closeModalWarning() {
                console.log('close')
                $('#modalWarning').modal('hide')
                this.newBoard = null
            }
            ,

            addBoardPublic() {
                if (this.newBoard) {
                    socket.emit('add-board', {userid: 0, title: this.newBoard});
                    this.newBoard = null
                }

            }
            ,
            async addBoardPrivate() {
                if (this.newBoard) {
                    socket.emit('add-board', {userid: this.authenticated, title: this.newBoard});
                    this.newBoard = null
                }


            }
            ,
            rename(id, wichdata) {
                if (wichdata === 'card') {
                    this.editCard = id
                } else if (wichdata === 'board') {
                    this.editBoard = id
                } else {
                    this.editColumn = id
                }
            }
            ,
            async deleteBoard(id) {
                socket.emit('delete-board', {id: id});


            },
            async deleteColumn(board_id, column_id) {
                socket.emit('delete-column', {board_id: board_id, column_id: column_id});
            },
            async deleteCard(card_id) {
                socket.emit('delete-card', {card_id: card_id});

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
                    socket.emit('add-status', {boardId: board.id, title: this.newColumn});


                    this.newColumn = null
                }
            }
            ,
            async addCard(boardId, column) {
                if (this.newCard[column.id]) {
                    socket.emit('add-card', {
                        'board_id': boardId,
                        'status_id': column.id,
                        'user_id': this.authenticated ? parseInt(this.authenticated) : 0,
                        'order_num': 0,
                        'title': this.newCard[column.id]
                    });

                    column.cards.unshift({title: this.newCard[column.id], id: column.cards + 1})
                    this.newCard[column.id] = null
                }
            }
            ,
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
                socket.emit('change-status', {id: draggedcard.id, statusId: newStatusId});


            }
            ,
            async startDrag(cards) {
                this.drag = true;
                this.columnsBeforeDrag = cards
            }
            ,
            async loadData() {
                socket.emit('load-data')
                //let data = await fetch('http://127.0.0.1:8000/boards')  // set the path; the method is GET by default, but can be modified with a second parameter
                  //  .then((response) => response.json())
            },
            saveAllBoard(data) {
                for (const item of data) {
                    item.columns = []
                    item.isActive = false;
                }
                this.allBoard = data
                const user = document.getElementById('showusername')
                if (user && user.dataset) {
                    this.authenticated = (user.dataset.userid)
                }
            }

        }
        ,
        async mounted() {
            await this.loadData();
            socket.on('boardlist-change', async function () {
                await app.loadData()
            });
            socket.on('board-change', function () {
                let activeBoards = []
                for (let i = 0; i < app.allBoard.length; i++) {
                    let board = app.allBoard[i];
                    if (board.isActive) {
                        activeBoards.push(board.id)
                    }
                }
                socket.emit('refresh-request', activeBoards);

            });
            socket.on('load-data', function(data) {
                app.saveAllBoard(data)
            });

            socket.on('refresh-response', function (result) {
                let statuses = result.statuses;
                let cards = result.cards;
                let boards = [];
                for (let i = 0; i < result.board_ids; i++) {
                    boards.push({'boardId': result.board_ids[i], 'cards': [], 'statuses': []})
                    for (let j = 0; j < statuses.length; j++) {
                        let status = statuses[j];
                        if (status.boardid == result.board_ids[i]) {
                            boards[i].statuses.push(status);
                        }
                    }
                    for (card of cards) {
                        if (card.board_id == result.board_ids[i]) {
                            boards[i].cards.push(card)
                        }
                    }

                }
                for (board of boards) {


                    app.saveSocketData(board.boardId, board.statuses, board.cards)
                }
            });
        }
    })
;


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