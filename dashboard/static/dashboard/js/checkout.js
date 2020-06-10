document.addEventListener('DOMContentLoaded', function(){
    // Render the PayPal button into #paypal-button-container
    paypal.Buttons({
        createOrder: function(data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        amount: {
                            value: parseFloat(total).toFixed(2)
                        }
                    }]
                });
            },

            // Finalize the transaction
            onApprove: function(data, actions) {
                return actions.order.capture().then(function(details) {
                    submitformdata();
                });
            }
    }).render('#paypal-button-container');

	if(shipping == false){
		document.querySelector('#address-form').style.display = 'none';
		document.querySelector('#paypal-button-container').style.display = 'block';
	}

	var form = document.querySelector('#address');
	form.addEventListener('submit', function(e){
		e.preventDefault();
		document.querySelector('#paypal-button-container').style.display = 'block';
		document.querySelector('#continue').style.display = 'none';
	});

	function submitformdata(){
		var shipping_info = {
			'street':null,
			'city':null,
			'zipcode':null,
			'country':null,
		}
		let userformdata = {
			'shipping': shipping,
			'total' : total
		}

		if (shipping != false){
			shipping_info.street = form.street.value;
			shipping_info.city = form.city.value;
			shipping_info.zipcode = form.zipcode.value;
			shipping_info.country = form.country.value;
		}

		fetch(url, {
			method:'POST',
			headers : {
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({'csrfmiddlewaretoken': csrftoken, 'form':userformdata, 'shipping': shipping_info})
		})
		.then((response) => response.json())
		.then((data) => {
			alert(data);
			window.location.href = premise_url;
		})
	}
});