document.addEventListener('DOMContentLoaded', function() {
    const queryParams = new URLSearchParams(window.location.search);
    const amount = queryParams.get('amount');  // Get the amount from the URL

    if (amount) {
        document.getElementById('payment-amount').textContent = `Amount Due: €${amount}`;
    }
});


function convertEuroToEther(euros) {
    // Placeholder conversion, you will need real-time data or a fixed conversion rate
    const euroToEtherRate = 0.1; // Example rate: 1 Euro = 0.00045 Ether
    return euros * euroToEtherRate;
}

let web3;
let userAccount;
// Send transaction from the connected wallet
async function launchMetaMask() {



    if (window.ethereum) {
        try {
            // Request account access if needed
            web3 = new Web3(window.ethereum);
            const accounts = await web3.eth.requestAccounts();
            userAccount = accounts[0];
            
            console.log('Connected', userAccount);
        } catch (error) {
            console.error('User denied account access');
        }
    } else {
        alert('Please install MetaMask!');
    }
    const recipientAddress = '0x8C9aAF3cBD98969c71D771e3DeF47c27F6750Da7'; // Smart contract for payment distribution
    const amountToSend = web3.utils.toWei('0.00000000001', 'ether'); // Set the amount to send


    try {
        const params = {
            from: userAccount,
            to: recipientAddress,
            value: web3.utils.toHex(amountToSend),
            gasPrice: '200000000000', // Use appropriate gas price
            gas: '210000', // Set appropriate gas limit
        };
        console.log('Transaction to be executed: ');

        // Sending the transaction
        const txHash = await web3.eth.sendTransaction(params);
        console.log('Transaction successful: ', txHash);
        // Navigate back to the app after a successful transaction
        linkBackToApp() 
            window.location.href = 'https://t.me/mallorca_beaches_bot?start='+userAccount;
        
    } catch (error) {
        console.error('Transaction failed: ', error);
        linkBackToApp()
            window.location.href = 'https://t.me/mallorca_beaches_bot?start='+error;
    }
    }
    function linkBackToApp() {
        window.location.href = 'https://t.me/mallorca_beaches_bot';
    }




