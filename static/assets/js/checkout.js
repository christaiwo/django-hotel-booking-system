let checkIn = document.getElementById('check-in').value;
let checkOut = document.getElementById('check-out').value;
let room = document.getElementById('room').value;
let guest = document.getElementById('guest').value;
let total = document.getElementById('total');
let price = document.getElementById('price').value;

document.getElementById("check-in").value = "2022-11-09";
document.getElementById("check-out").value = "2022-11-10";


// calculate total
const calTotal = () => {
    checkIn = document.getElementById('check-in').value;
    checkOut = document.getElementById('check-out').value;
    room = document.getElementById('room').value;

    // alert(room)
    const oneDay = 24 * 60 * 60 * 1000;
    var firstDate = new Date(checkIn); 
    var secondDate = new Date(checkOut); 
    var diffDays = Math.round(Math.abs((firstDate.getTime() - secondDate.getTime()) / (oneDay)));


    
    let totalWithDays = price * diffDays;
    let totalWithRoom = totalWithDays * room;



    total.innerHTML = `${totalWithRoom}`;

    document.getElementById('amount').value = totalWithRoom;

    
}



// plus room
value = 0;
const plusRoom = () => {
    value += 1; 
    document.getElementById('room').value = value ;

    calTotal();

}
const minusRoom = () => {
    if (value <= 1 ){
        value = 1
    }
    else{
        value -= 1; 
    }
    document.getElementById('room').value = value ;
    calTotal();
}