
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
        isEdit: 0,
        spans: document.getElementsByClassName("span1"),
        drag: false,
        boards: sampleData.boards,
        columns: ['El sem indult', 'Kicsit késik', 'Sokat késik', 'Eltűnt']
    },
    methods: {
        addBoard() {
            this.boards.push({ title: 'Board ' + (this.boards.length + 1), id:this.boards.length + 1})
        },
        rename(id) {
            this.isEdit = id;
        },
        handleEnter(event) {
            let key = event.key || event.keyCode;
            if (key === 'Enter' || key === 13) {
                this.isEdit = 0;
            }
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