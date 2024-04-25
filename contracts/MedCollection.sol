// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract MedGardens is ERC721URIStorage, Ownable(msg.sender) {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIdCounter;

    uint256 public constant MAX_SUPPLY = 1000;
    string public baseURI;
    string public initialBaseURI;

    // Struct to hold NFT data
    struct NFTData {
        string gpsCoordinates;
        uint256 sponsorshipLength;
        uint256 area;
        uint256 dueTime;
    }

    // Mapping from token ID to its data
    mapping(uint256 => NFTData) public nftData;

    constructor() ERC721("MedGardens", "MGR") {
        setBaseURI(initialBaseURI);
    }

    function mint(address to, string memory tokenURI, string memory gpsCoordinates, uint256 sponsorshipLength, uint256 area, uint256 dueTime) public onlyOwner {
        require(_tokenIdCounter.current() < MAX_SUPPLY, "Max supply reached");
        _tokenIdCounter.increment();
        uint256 tokenId = _tokenIdCounter.current();
        _mint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);
        // Store the mint timestamp along with other data
        nftData[tokenId] = NFTData(gpsCoordinates, sponsorshipLength, area, dueTime);
    }

    function setBaseURI(string memory newBaseURI) public onlyOwner {
        baseURI = newBaseURI;
    }

    function _baseURI() internal view override returns (string memory) {
        return baseURI;
    }

    // Function to get NFT data
    function getNFTData(uint256 tokenId) public view returns (string memory gpsCoordinates, uint256 sponsorshipLength, uint256 area, uint256 mintTimestamp) {
        NFTData storage data = nftData[tokenId];
        return (data.gpsCoordinates, data.sponsorshipLength, data.area, data.dueTime);
    }
}