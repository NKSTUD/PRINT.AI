const test_btn = document.getElementById("test")
test_btn.addEventListener('click', () => {
    Swal.fire({
        position: 'top-end',
        icon: false,
        title: 'Copie',
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true,
        toast: false,
        heightAuto: false,
        customClass: {
            title: 'my-swal-title',
            popup: 'my-swal-popup'
        }
    })
        .then(r => console.log(r));
})