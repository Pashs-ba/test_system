class Sorter{
    constructor(el){
        this.table = el;
        var header = table.children[0];
        for (var col_header of header.children[0].children){
            col_header.onclick = function(){sort_col(this);};
            // console.log(col_header.onclick, )
        }
    }
}
function sort_col(el){
    let i = document.createElement("i")
    i.classList.add("bi")
    i.classList.add("bi-arrow-down-short")
    i.classList.add("animated")
    el.appendChild(i)
    console.log(el.children)
}