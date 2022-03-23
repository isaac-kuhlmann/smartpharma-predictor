## Weekly State
- In Stock Amount
- Amount used this week
    ### Action : Reward Structure
    - Agent Makes an Order : depends on how much ordered (more negative when a larger order is made)
    - Agent Does Nothing : 0

    ### Rewards Resulting After Action (Trouble?)
    - Each patient treated this week : +2
    - Each patient not treated: -50

### How to form the Q Table?
- State (rows) : only needs to be the current stock
    - suggest - can be divided into 100's or 1000s
- Action (cols) : the number of units to order (0, 1, 2, ...)