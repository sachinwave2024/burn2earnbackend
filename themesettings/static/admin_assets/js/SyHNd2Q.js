const m_contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}];
const m_contract_address  = '0x410E60B8A662FAafD79D323ed117A0d9A9ECC65f';

const admin_address 		=	'0x36ee7371c5d0fa379428321b9d531a1cf0a5cae6';



const b_contract_abi= [{"inputs":[{"internalType":"address","name":"_token","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"string","name":"name","type":"string"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"addBidEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"bidCancelEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"bidEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"claimEvent","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"winner","type":"address"},{"indexed":false,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"winingAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"time","type":"uint256"}],"name":"drawEvent","type":"event"},{"inputs":[{"components":[{"internalType":"uint256","name":"pid","type":"uint256"},{"internalType":"address","name":"winner","type":"address"},{"internalType":"uint256","name":"winningAmount","type":"uint256"}],"internalType":"struct HotBigDealBetting.multiDrawVars[]","name":"vars","type":"tuple[]"}],"name":"MultiDraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_description","type":"string"},{"internalType":"uint256","name":"_startTime","type":"uint256"},{"internalType":"uint256","name":"_endTime","type":"uint256"}],"name":"addbids","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"bidCancel","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"bidDetails","outputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_description","type":"string"},{"internalType":"address","name":"_winner","type":"address"},{"internalType":"uint256","name":"_winningAmount","type":"uint256"},{"internalType":"uint256","name":"_startTime","type":"uint256"},{"internalType":"uint256","name":"_endTime","type":"uint256"},{"internalType":"uint256","name":"_totalDeposit","type":"uint256"},{"internalType":"bool","name":"_active","type":"bool"},{"internalType":"bool","name":"_cancel","type":"bool"},{"internalType":"address[]","name":"_totalMembers","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"bidPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"bids","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"bidsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_winner","type":"address"},{"internalType":"uint256","name":"_winningAmount","type":"uint256"}],"name":"draw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"isMembers","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"token","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"deposit","type":"uint256"},{"internalType":"uint256","name":"winningAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}];
const b_contract_address ='0x7C58b635E4156ACB63E47ffBa2ECEA396E2bFaE5';

 
var currentpage = window.location.pathname;

function start_loader()
   {
    $('#myLoad').show();
   }

  function stop_loader()
  {
    $('#myLoad').hide();
  }


$(document).ready(function(){
	$('#id_winningamount').keyup(function(event){
        var get_winning_amount =  parseFloat($(this).val());
        

        var get_amount =  parseFloat($("#id_amount").val());

        var get_fee = parseFloat($("#id_percentage").val());
        var check = 0;
        if (get_winning_amount > parseFloat(check)){

          var cal_winning = (get_winning_amount * get_amount);

          var cal_amout = parseFloat(cal_winning * get_fee);

          var remaing_amount  =parseFloat(cal_amout/100);

          var totalamount = (parseFloat(cal_winning) + parseFloat(remaing_amount));

          $("#id_fees").val(remaing_amount.toFixed(2));
          $("#id_total").val(totalamount.toFixed(2));
          
        }else if (get_winning_amount == parseFloat(check)){
          var lala_total = 0;
          var receive_lala = 0;
          $("#id_fees").val(0);
          $("#id_total").val(0);
        }
        else if (get_winning_amount == '' || isNaN(get_winning_amount)){
         
          $("#id_fees").val(0);
          $("#id_total").val(0);
        }

  });

	$("#id_pair_id").on('change',function(){
          var pairid =   $(this).find(":selected").val();
          ajaxPost('/auctions/getmarketpriceajax', {
            'pairid':pairid}, function(content){
             
              var json_obj = JSON.parse(content);
              if (json_obj.status == 'Success'){
                var marketprice = parseFloat(json_obj.type);

                $('#id_amount').val(marketprice.toFixed(2));
                var feespercentage =  parseFloat($('#id_percentage').val());
                var amount =  parseFloat($('#id_amount').val());
                var cal_amout = (amount * feespercentage );
                var winning_amount =  parseFloat($("#id_winningamount").val()) || 0;
               
                var check=0;
                if((winning_amount == check) )  {
                  
                }else{
                 var remaing_amount  =parseFloat(cal_amout/100);
                 $('#id_fees').val(remaing_amount);
                 var totalamount = (parseFloat(amount) + parseFloat(remaing_amount));
                 $('#id_total').val(totalamount);
                }
               
              }else{
                var marketprice = 0.00;
                var remaing_amount =0.00;
                var totalamount = 0.0000;
                $('#id_amount').val(marketprice);
                
              }
          }); 
    
    });
   
    function validateAuctionForm(){
        var check = 0;
        var pair=$('#id_pair_id').val();
        var auctionname=$('#id_auction_name').val();
        var content = $('#id_content').val();
        var amount = parseFloat($('#id_amount').val());
        var feespercentage = parseFloat($('#id_percentage').val());
        var fees= parseFloat($('#id_fees').val());
        var total= parseFloat($('#id_total').val());
        var startdate= $('#id_startdate').val();
        var duration= $('#id_duration').val();
        var winningcurrency =  $('#id_winning_currency_id').val()
        var winningamount = $('#id_winningamount').val();
        
        var token = 0.0
        
        if(pair == '' ){
          msg = 'Pair field is required.'
          validate_msg('error',msg);
        }else if(winningcurrency == ''){
          msg = 'Winning Currency  field is required.'
          validate_msg('error',msg);
        }else if(isNaN(winningamount)){
          msg = 'Winning Amount field is required.'
          validate_msg('error',msg);
        }else if(winningamount == 0.0){
          msg = 'Enter Valid Winning Amount'
          validate_msg('error',msg);
        }else if(auctionname == ''){
          msg = 'Name field is required.'
          validate_msg('error',msg);
        }else if(content == ''){
          msg = 'Description field is required.'
          validate_msg('error',msg);
        }else if(isNaN(amount)){
          msg = 'Amount field is required.'
          validate_msg('error',msg);
        }else if(isNaN(feespercentage)){
        	msg = 'Fees Percentage field is required.'
        	validate_msg('error',msg);
        }else if(isNaN(fees)){
        	msg = 'Fees  field is required.'
        	validate_msg('error',msg);
        }else if(isNaN(total)){
        	msg = 'Total  field is required.'
        	validate_msg('error',msg);
        }else if(startdate == ''){
        	msg = 'Start Date  field is required.'
        	validate_msg('error',msg);
        }else if(duration == ''){
        	msg = 'Duration  field is required.'
        	validate_msg('error',msg);
        }
        else{
          if (typeof web3 !== "undefined" ) {
			window.web3 = new Web3(web3.currentProvider);
			var BcontractInfo = (b_contract_abi);
			b_contract 	= 	new web3.eth.Contract(BcontractInfo,b_contract_address);
			
			(async function(){
					
					if (currentpage == '/auctions/addauctions/'){
							enableAccount()
							const accounts = await ethereum.request({
					            method: 'eth_accounts'
					        })
					        .then()
					        .catch((accounts) => {
					            if (error.code === 4001) {
					                
					            } else {
					            	
					            }
					        });
					        
					        if (accounts.length == 0) {
					        	msg ='Your metamask account is locked please unlock.';
								    type ='error';
								    enableAccount()
								    validate_msg(type,msg)
					        }
					        else{
					        	
					        	
					        	var auction_name=auctionname;
					        	var auction_description = content;

					        	var auction_saleprice =total * 10 ** 18;
					        	auction_saleprice =BigInt(auction_saleprice)
					        	var auction_startdateunixtime= toTimestamp(startdate);
					        	var auction_durationdateunixtime = toTimestamp(duration);

					        	function toTimestamp(strDate){ var datum = Date.parse(strDate); return datum/1000;}

					        	
					        	start_loader();
                    b_contract.methods.bidsLength().call().then(function(past_id) {

                          var past_auction_id = past_id
         
                          b_contract.methods.addbids(auction_name,auction_description,auction_startdateunixtime,auction_durationdateunixtime).send({from:admin_address}).on('transactionHash', (hash) => {}).on('receipt', (receipt) => {
                                          type ='success';
                                          msg='Auction Amount Success !!!';
                                          
                                          stop_loader();
                          getreceipt(receipt['transactionHash'])
                          }).on('confirmation', (confirmationNumber, receipt) => {}).on('error', (error) => {
                            type ='error';
                              msg ='Auction transaction failed.';
                              stop_loader();
                              validate_msg(type,msg)
                        });
                      
                        function getreceipt(perdictionhashtxt){
                              web3.eth.getTransactionReceipt(perdictionhashtxt, function(err, data) {
                                if(data==null){
                                  
                                  getreceipt(perdictionhashtxt);
                                  
                                }else{
                                  if(data.status=="0x1"){
                                    
                                    var transaction_id = perdictionhashtxt;
                                    var values= {
                                      'pair':pair,
                                      'auctionname':auctionname,
                                      'content':content,
                                      'amount':amount,
                                      'feespercentage':feespercentage,
                                      'fees':fees,
                                      'total':total,
                                      'startdate':startdate,
                                      'duration':duration,
                                      'winningcurrency':winningcurrency,
                                      'winningamount':winningamount,
                                      'transaction_id':transaction_id,
                                      'token':token,
                                      'past_auction_id':past_auction_id
                                    }
                                    $.ajax({
                                      url: '/auctions/ajaxauctionspost/',
                                      csrfmiddlewaretoken: "{{ csrf_token }}",
                                      headers: {
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json'
                                        },
                                          type: 'post',
                                          data:JSON.stringify(values),
                                          success: function(content){ 
                                            var json_obj = JSON.parse(content.content);           
                                            if (json_obj.status == 'successprediction'){
                                              type ='success';
                                              msg ='Auction created successfully.';
                                              validate_msg(type,msg)
                                              setTimeout(function () {
                                              window.location.href = '/auctions/auctionslist/';
                                          }, 6000);
                                            }
                                            else{
                                              type ='error';
                                              msg ='Metamask not connected';
                                              validate_msg(type,msg)
                                            }
                                          },
                                        });
                                      }
                                    } 
                              })
                        }
                  });

					        	
							}
				    	}
				}) ();
		   }else{
			msg ='Your metamask account is locked please unlock.';
			type ='error';
			validate_msg(type,msg)
		}


        }
    }
    $(function () {

        $('form#auctionform').on('submit', function (e) {
          e.preventDefault();
          validateAuctionForm()

        });
    });
});
 
$(document).ready(function(){

	function validateAuctionCancelForm(){
		var auctionid= $('#auctionid').val();
		
		if(auctionid == ''){
          msg = 'aution id  field is required.'
          validate_msg('error',msg);
        }else{
        	if (typeof web3 !== "undefined" ) {

				window.web3 = new Web3(web3.currentProvider);
				var BcontractInfo = (b_contract_abi);
				var McontractInfo 	= 	(m_contract_abi);
				b_contract 	= 	new web3.eth.Contract(BcontractInfo,b_contract_address);
				m_contract 		= 	new web3.eth.Contract(McontractInfo,m_contract_address);
				
				(async function(){
						var viewpage=0
						if (viewpage == 0){

								const accounts = await ethereum.request({
						            method: 'eth_accounts'
						        })
						        .then()
						        .catch((accounts) => {
						            if (error.code === 4001) {
						               
						            } else {
						            	
						            }
						        });
						       
						        if (accounts.length == 0) {
						        	msg ='Your metamask account is locked please unlock.';
									type ='error';
									enableAccount()
									validate_msg(type,msg)
						        }
						        else{
						        	var autionid = $('#auctionid').val();
						        	var past_auctionid =$('#past_auction_id').val();
                      
                      start_loader()
		        					
						        		b_contract.methods.bidCancel(past_auctionid).send({from:admin_address}).on('transactionHash', (hash) => {}).on('receipt', (receipt) => {
							        				
											 		type ='success';
		                                            msg='Auction Cancelled Success !!!';
		                                            validate_msg(type,msg)
		                                            
		                                            stop_loader();
		        									getreceipt(receipt['transactionHash'])
												}).on('confirmation', (confirmationNumber, receipt) => {}).on('error', (error) => {
												 	type ='error';
												    msg ='Auction transaction failed.';
												    stop_loader();
												    validate_msg(type,msg)
										  });
							        	function getreceipt(perdictionhashtxt){
						        					web3.eth.getTransactionReceipt(perdictionhashtxt, function(err, data) {
						        						if(data==null){
						        							
						        							getreceipt(perdictionhashtxt);
						        							
						        						}else{
						        							if(data.status=="0x1"){
							        							
							        							var transaction_id = '';
										        				var values= {
																'auctionid':auctionid,
																'past_auctionid':past_auctionid,
																}
																$.ajax({
																	url: '/auctions/ajaxcancelauction/',
																	csrfmiddlewaretoken: "{{ csrf_token }}",
																	headers: {
														  			'Accept': 'application/json',
														  			'Content-Type': 'application/json'
														     		},
															        type: 'post',
															        data:JSON.stringify(values),
															        success: function(content){ 
														            var json_obj = JSON.parse(content.content);           
														            if (json_obj.status == 'successprediction'){
														              type ='success';
														              msg ='Auction created successfully.';
														              validate_msg(type,msg)
														              setTimeout(function () {
														              window.location.href = '/auctions/auctionslist/';
														          }, 6000);
														            }
														            else{
														              type ='error';
														              msg ='Metamask not connected';
														              validate_msg(type,msg)
														            }
															        },
							        							});
						        							}
						        						}	
						        					})
						        		}
								}
					    	}
					}) ();
			   }else{
				msg ='Your metamask account is locked please unlock.';
				type ='error';
				validate_msg(type,msg)
				}

        }
	}
	$(function () {

        $('form#formcancelorder').on('submit', function (e) {

        e.preventDefault();
        validateAuctionCancelForm()

        });
    });
	
});





async function enableAccount() {
	const accounts 	= 	await ethereum.enable();
	accounts1 		= 	accounts;
}
if(window.ethereum) {
	window.ethereum.on('accountsChanged', function () {
		web3.eth.getAccounts(function(error, accounts) {
			accounts1 = accounts;
			var address = accounts1[0];

		});
	});

}
function validate_msg(type,message){

  if (type =='success'){
    var success_text =  message;
    Lobibox.notify('success', {
    title:'Success',
    continueDelayOnInactiveTab: false,
    pauseDelayOnHover: true,
    sound: false,
    position: 'right top',
    msg: success_text
    });

  }
  if (type =='error'){
    var error_text = message
    Lobibox.notify('error', {
    title:'Error',
    continueDelayOnInactiveTab: false,
    pauseDelayOnHover: true,
    sound: false,
    position: 'right top',
    msg: error_text
    });
  }
}