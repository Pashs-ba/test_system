class Sorter{
    constructor(el, except){
        this.table = el;
        var header = table.children[0];
        for (var col_header of header.children[0].children){
            col_header.onclick = function(){sort_col(this, except)};
            // console.log(col_header.onclick, )
        }
    }
}
function clear_arrows(el, except){
    /** 
     Clear arrows from all thaed el's except current element and delete table
     */
    let parent = el.parentElement
    for (let th of parent.children){
        if (!(th==el || th==except)){
            for (let q of th.children){
                q.remove()
            }
        }
    }
}
function sort_table(el, reverse){
    let n = el.cellIndex
    let table = el.closest("table").children[1]
    switching = true;
    switchcount = 0
    dir = "asc";
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 0; i < (rows.length - 1); i++) {
        shouldSwitch = false;
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
        if (dir == "asc") {
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
            shouldSwitch = true;
            break;
            }
        } else if (dir == "desc") {
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
            shouldSwitch = true;
            break;
            }
        }
        }
        if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        switchcount ++;
        } else {
        if (switchcount == 0 && dir == "asc") {
            dir = "desc";
            switching = true;
        }
        }
    }
}
function sort_col(el, except, index){
    if (el == except){
        return;
    }
    clear_arrows(el, except)
    
    let i = document.createElement("i")
    i.classList.add("bi")

    if (el.children[0] && el.children[0].classList.contains("bi-arrow-down-short")){
        i.classList.add("bi-arrow-up-short")
    }else{
        i.classList.add("bi-arrow-down-short")
    }

    i.classList.add("animated")

    if (el.children.length){ // if arrow is already been, remove it and place new
        el.children[0].remove()
    }

    el.appendChild(i)
    sort_table(el, el.children[0].classList.contains("bi-arrow-down-short"))
        
}