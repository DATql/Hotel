function addToCart(id, name, price,sokhachtoida,loaiphong) {
    alert(" Đã Thêm Phòng")
    fetch('/cart', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price,
            "sokhachtoida":sokhachtoida,
            "loaiphong":loaiphong
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    }).catch(err => console.error(err))
}

const get_day_of_time = (d1,d2)=>{
    let ms1 = d1.getTime();
    let ms2 = d2.getTime();
    return Math.ceil((ms2-ms1)/(24*60*60*1000))
}

