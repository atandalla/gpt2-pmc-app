function getId(param) {

    const id = param;
    var x = document.getElementById(id);
    var loadcard = document.getElementsByClassName(id)[0];

    if (x.style.display === "none") {
        loadcard.style.display = "block";
        //Mandar post 
        fetch('/ajax', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({
                id: id
            })
        })
            .then(res => res.text())
            .then(data => {
                loadcard.style.display = "none";
                x.style.display = "block";
                load(id);


            })

    } else {
        loadcard.style.display = "none";
        x.style.display = "none";

    }
}


function load(id) {

    $.ajax({
        url: '/booksPro',
        success: function (products) {

            let tbody = $("div[id='" + id + "']");
            tbody.html('');
            products.forEach(product => {
                console.log("productos")
                tbody.append(`

                        <div class="row justify-content-center mt-4 ">
                        <div class="col-6 col-md-3 ">
                            <blockquote class="blockquote mb-0">
                                <div class="card text-white ">
                                    <img class="card-img img-responsive card-img-main " src="/assets/img/carta.PNG" alt="Card image" style="max-width: 13rem;">
                                    <div class="card-img-overlay justify-content-center">
                                        <h6 class="card-title" style="color: black; padding-top: 0.1rem; font-size: 6px;">
                                        ${product.title}
                                        </h6>
                                    </div>
                                </div>
                            </blockquote>

                        </div>
                        <div class="col-12 col-sm-6 col-md-9">

                            <div class="card">
                                <div class="card-header">
                                    <h5 style="color:rgb(5, 77, 145); font-size: 10px;">
                                    ${product.title}
                                    </h5>
                                    <blockquote class="blockquote mb-0">
                                        <h5 style="color:rgb(0, 0, 0); font-size: 9px;">Year
                                            <a href="" style="color:rgb(4, 106, 201)">
                                            ${product.pubyear}
                                            </a>
                                        </h5>
                                        <h6 style="color:rgb(36, 36, 36);font-size: 9px;">By
                                        ${product.author}
                                        </h6>
                                        <footer class="blockquote">
                                            <a class="btn" style="color: #fff; background-color: #ad5401; font-size:9px" href=" ${product.url}">Get PDF</a>

                                        </footer>
                                    </blockquote>
                                </div>
                            </div>

                        </div>
                    </div>

                        `)
            })


        }
    });



    // $('.getBooks').on('click', function(e) {
    //     var n = $('#nameSimil').val();
    //     console.log(n);
    //     e.preventDefault();
    //     $.ajax({
    //         url: '/ajax',
    //         type: 'POST',
    //         cache: false,
    //         data: { field1: 1, field2: 2 },
    //         success: function(data) {
    //             alert('Success!')
    //             console.log(data)
    //         },

    //     })
    // });


    // $("#addClass").click(function() {
    //     $('#qnimate').addClass('popup-box-on');
    // });

    // $("#removeClass").click(function() {
    //     $('#qnimate').removeClass('popup-box-on');
    // });


}