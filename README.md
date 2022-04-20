# PoolChain-Blockchain-Consensus-Protocol
PoolChain is a new consensus protocol for blockchain that is a hybrid of Proof-of-Work and
Proof-of-stake that inherits the robustness of the former while still saving few resources like
the latter without compromising with the mining rewards and security of the system. <br />
It uses the stake to reduce the difficulty of Proof-of-Work mining thus making the protocol energy efficient
and scalable. <br />
Our protocol tries to address the issues that are present in PoW and PoS like
Energy wastage, Long Range Attack, Stubborn Mining, Selfish Mining and Initial Distribution
Problem. Our main objective is to come up with a protocol which is energy efficient while
keeping the mining rewards similarly competitive as with PoW while also addressing major
attacks on pure PoS. <br />
We introduce a new concept of blockchain miners bidding to create the
next block in the blockchain and test its effectiveness as an alternative for the existing protocols.
# PoolChain - High Level
*Reduce Difficulty of POW on the basis of stakes
*These stakes aren’t on the basis of total stakes but calculated on the basis of bids per block. Otherwise who have large stakes will get inaccessible lead in cornering more blocks forever creating a reinforcing loop.
*Bids for a block is made before some N blocks ( say 1000 )  earlier.
*Bid ratio or stake for a block is decided by bid/ total bids for a block. 
*More Bid Ratio -> Lower difficulty -> Easier to Mine
*Less Bid Ratio -> Higher Difficulty -> Harder to Mine
*After Block Creation Bids and rewards blocked for S blocks( say 1000) .
*Any tampering leads to confiscation of bids and rewards.

