$(function(){
	$('.update-cart').on('click', function(){
		if (user=='AnonymousUser'){
			alert('Please login to add a product to your cart!');
			window.location.href = '/authenticate/login';
		}else{
			var productId = $(this).attr('data-product');
			var action = $(this).attr('data-action');
			var url = $(this).attr('data-url');
			var csrf_token = $(this).attr('data-csrftoken');
			var data = {csrfmiddlewaretoken: csrf_token, 'productId':productId, 'action':action};
			$.ajax({
				type:'POST',
				url: url,
				data:data,
				success: function(response){
					location.reload();
				},
				error: function (error){
					console.log('Xayr');
				}
			});	
		}
		
	});
});