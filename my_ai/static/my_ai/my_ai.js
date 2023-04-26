


function copy_text(i) {
    navigator.clipboard.writeText(document.getElementById(i).innerText).then(r => console.log(r));
    Swal.fire({
        title: 'Copié!',
        showConfirmButton: false,
        timer: 1000
    });


}

const copy_all_btn = document.getElementById("copy_all")
const all_cards = document.getElementById("all_cards")

function copy_all_card() {
    console.log(copy_all_btn)

}


let user_description = document.getElementById('user_description');

user_description.addEventListener('input', autoResize, false);

function autoResize() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
}

testbtn = document.getElementById("test")
testbtn.addEventListener('click', () => {
    alert("test")

})




