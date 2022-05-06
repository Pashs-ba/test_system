class Sorter{
    constructor(el, except){
        this.table = el;
        var header = table.children[0];
        for (var col_header of header.children[0].children){
            col_header.onclick = function(){sort_col(this, except)};
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
    let tbody = el.closest("table").children[1]
    let rows = Array.from(tbody.rows)
    let old_f = rows[0]
    let old_last = rows[rows.length-1]
    let sorted_rows = rows.sort(function(a,b){
        if (a.getElementsByTagName("TH")[n].innerHTML<b.getElementsByTagName("TH")[n].innerHTML){
            return -1
        }
        if (a.getElementsByTagName("TH")[n].innerHTML>b.getElementsByTagName("TH")[n].innerHTML){
            return 1
        }
        return 0
    })
    tbody.innerHTML = ''
    if(old_f===sorted_rows[0] && old_last === sorted_rows[rows.length-1]){
        sorted_rows = sorted_rows.reverse()
    }
    for (i of sorted_rows){
        tbody.appendChild(i)
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