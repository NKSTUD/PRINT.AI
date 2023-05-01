function copy_text(i) {
    navigator.clipboard.writeText(document.getElementById(i).innerText).then(r => console.log(r));
    Swal.fire({
        title: 'Copié!',
        showConfirmButton: false,
        timer: 1000
    });


}


function autoResize() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
}







