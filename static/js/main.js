var app = new Vue({
    el: '#app',
    components: {
        // draggable
    },
    data: {
        drag: false,
        boards: sampleData.boards,
        columns: ['El sem indult', 'Kicsit késik', 'Sokat késik', 'Eltűnt']
    },
    methods: {
        async addBoard() {
            //const userelement = document.getElementById('showusername');
          //  const userid = userelement.dataset.userid;
            console.log(await $.ajax({
                url: 'http://127.0.0.1:8000/boards/public',
                    data: {title: 'afsjldfjaélsdjfk',userid : 0},
                type: 'POST'
            })
)
}
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