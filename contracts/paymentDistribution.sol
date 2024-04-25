// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PaymentDistributor {
    address payable public walletA; //Universal 0xF9DB7E9F0E70D1fb52607f31865E5E5D810F2F69
    address payable public walletB; //MedGardens 0xfd9001f42c77c7cb29383469e7fbfdd9258344b8

    uint public percentageForWalletA; // Percentage of the total payment that walletA will receive

    constructor(address payable _walletA, address payable _walletB, uint _percentageForWalletA) {
        require(_percentageForWalletA <= 100, "Percentage must be between 0 and 100.");
        walletA = _walletA;
        walletB = _walletB;
        percentageForWalletA = _percentageForWalletA;
    }

    receive() external payable {
        require(msg.value > 0, "No payment was sent.");

        uint paymentForA = msg.value * percentageForWalletA / 100;
        uint paymentForB = msg.value - paymentForA; // Remaining amount goes to walletB

        walletA.transfer(paymentForA);
        walletB.transfer(paymentForB);
    }
}
