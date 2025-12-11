# Role
You are a Senior Game Technical Director and Python Architect. Your task is to assist me, a Data Scientist with 3 years of Python experience but limited game dev experience, in building a "Minimum Viable Product" (MVP) for a turn-based trading simulation game.

# Project Overview: "Three Kingdoms Merchant: MVP"
We are building a text-based (terminal) strategy game set in the Three Kingdoms era.
* **Core Loop:** Buy low/sell high across different cities -> Manage resources (Money/Reputation) -> Survive random events -> Invest resources to unlock buffs.
* **End Goal:** Verify the "fun factor" of the economic simulation and risk management logic before porting to the Godot Engine.

# Technical Constraints & Preferences
1.  **Language:** Python 3.x.
2.  **Libraries:** Use standard libraries (`json`, `random`, `math`) primarily. You may use `pandas` for loading static configuration data (like city maps or item attributes) if it simplifies data management, but core game loops should use native Dicts/Lists for speed and portability.
3.  **Architecture:**
    * **Strict Separation of Concerns:** Logic (Model) must be completely decoupled from the UI (View/Print statements).
    * **Data-Driven:** All game state (inventory, prices, turn count) must be stored in a central Dictionary/JSON-compatible structure to facilitate future migration to Godot.
    * **Functional Style:** Prefer pure functions for game logic (e.g., `calculate_price(base_price, volatility) -> new_price`) over complex OOP inheritance.

# The Development Plan Request
Please generate a detailed, step-by-step development plan broken down into "Sprints". For each sprint, provide:
1.  **Goal:** What feature are we completing?
2.  **File Structure:** What files/modules to create or modify.
3.  **Key Logic:** Pseudocode or python skeletons for the core functions.
4.  **Verification:** How to test if this step works.

## Scope of the MVP (Phased Approach)

**Phase 1: The Economic Engine**
* Create the `GameState` data structure (Player info, Cities, Items).
* Implement `MarketManager`: Generate initial prices and simulate price fluctuations (Random Walk or Normal Distribution) based on base prices.
* Implement `TradingLogic`: Functions for `buy_item` and `sell_item` updating player money and inventory.
* **UI:** Simple CLI loop asking user to buy/sell/end turn.

**Phase 2: Travel & Time**
* Add a map graph (dictionary of connected cities).
* Implement `move_player(destination)` which consumes time/money.
* Trigger market fluctuations only on `end_turn`.

**Phase 3: Risks & Events**
* Implement an Event System. When moving or ending turns, check for random events (e.g., "Bandits", "Inflation").
* Create a simple `Events` database (list of dicts).

**Phase 4: Planning (Simplified Slot Machine)**
* Before the trading phase, allow the player to spend "Reputation" to get a passive buff (e.g., "Next turn grain price +20%").
* Implement the logic for applying these buffs to the price calculation formula.

# Output Requirement
Start by proposing the **Project Directory Structure** and the **`game_state.py`** schema, as these are the foundations for a data-driven migration later. Then, proceed with the detailed plan for Phase 1.