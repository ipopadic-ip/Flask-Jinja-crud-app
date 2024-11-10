function validacija() {
    let brojIndeksa = document.querySelector("#brojIndeksaPolje").value;
    // const regex = new RegExp("^[0-9]{4}/[0-9]{6}$");
    // const regex = /^[0-9]{4}\/[0-9]{6}$/;
    const regex = /^\d{4}\/\d{6}$/;
    let rezultat = regex.test(brojIndeksa);
    window.alert(rezultat);
    return rezultat;
}