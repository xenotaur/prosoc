# P&G Paper Scenario Reference Data

Source: Francis et al. (2025), "Principles and Guidelines for Evaluating Social Robot Navigation
Algorithms", ACM THRI Vol. 14, No. 2, Article 34. Table 3 (p. 34:31) and Figure 7 (p. 34:34).

This file provides the canonical metadata for the 18 scenarios in Table 3. When a user requests
one of these by name, use this data to populate the scenario card fields. Do not invent values
not present here; leave fields blank if the paper does not specify them.

---

## Hallway Scenarios

### Frontal Approach
- **Description:** Pedestrian and robot approach head-on in a passable space
- **Physical Env:** Generic
- **Geometric Layout:** Passable space
- **Scientific Purpose:** Pedestrian interaction
- **Robot Task:** Navigate A to B
- **Human Behavior:** Navigate B to A
- **Ideal Outcome:** Robot/humans pass
- **Related Scenarios:** Ped. Obstruct
- **Cited In:** [50, 126, 167]
- **Implemented:** YES (`frontal_approach`)

### Pedestrian Overtaking
- **Description:** Pedestrian overtakes moving robot
- **Physical Env:** Generic
- **Geometric Layout:** Passable space
- **Scientific Purpose:** Pedestrian interaction
- **Robot Task:** Navigate A to B
- **Human Behavior:** Navigate A to B (faster)
- **Ideal Outcome:** Human passes robot
- **Related Scenarios:** Down Path
- **Cited In:** [26]
- **Implemented:** YES (`pedestrian_overtaking`)

### Robot Overtaking
- **Description:** Robot overtakes a moving pedestrian
- **Physical Env:** Generic
- **Geometric Layout:** Passable space
- **Scientific Purpose:** Pedestrian interaction
- **Robot Task:** Navigate A to B
- **Human Behavior:** Navigate A to B (slower)
- **Ideal Outcome:** Robot passes human
- **Cited In:** [50, 157]
- **Implemented:** YES (`robot_overtaking`)

### Intersection No Gesture
- **Description:** Robot and human cross at an indoor intersection without gesture
- **Physical Env:** Indoor
- **Geometric Layout:** Intersection
- **Scientific Purpose:** Pedestrian interaction
- **Robot Task:** Navigate A to B
- **Human Behavior:** Cross navigate
- **Ideal Outcome:** Both pass, no collision
- **Cited In:** [27, 50, 167]
- **Implemented:** YES (`intersection_no_gesture`)

### Intersection Gesture Wait
- **Description:** Robot told to wait at intersection
- **Physical Env:** Indoor
- **Geometric Layout:** Intersection
- **Scientific Purpose:** Pedestrian interaction
- **Robot Role:** Servant
- **Robot Task:** Navigate A to B
- **Human Behavior:** Cross navigate (gesture wait)
- **Ideal Outcome:** Human goes, then robot
- **Related Scenarios:** Gesture Proceed
- **Cited In:** [126]
- **Implemented:** YES (`intersection_gesture_wait`)

### Intersection Gesture Proceed
- **Description:** Robot told to proceed at intersection
- **Physical Env:** Indoor
- **Geometric Layout:** Intersection
- **Scientific Purpose:** Pedestrian interaction
- **Robot Role:** Servant
- **Robot Task:** Navigate A to B
- **Human Behavior:** Cross navigate (gesture proceed)
- **Ideal Outcome:** Robot goes first
- **Related Scenarios:** Gesture Wait
- **Cited In:** [126]
- **Implemented:** YES (`intersection_gesture_proceed`)

### Blind Corner
- **Description:** Robot and human meet at a blind corner
- **Physical Env:** Indoor
- **Geometric Layout:** Corner
- **Scientific Purpose:** Pedestrian interaction
- **Robot Task:** Navigate A to B
- **Human Behavior:** Navigate B to A
- **Ideal Outcome:** No collision / obstruction
- **Related Scenarios:** (none listed)
- **Cited In:** [126, 171]
- **Implemented:** YES (`blind_corner`)

---

## Doorway Scenarios

### Narrow Doorway
- **Description:** Robot and human at a narrow doorway (room and door)
- **Physical Env:** Indoor
- **Geometric Layout:** Room and door
- **Scientific Purpose:** Pedestrian interaction
- **Robot Task:** Navigate A to B
- **Human Behavior:** Navigate B to A
- **Ideal Outcome:** No collision / obstruction
- **Related Scenarios:** Narrow Arch
- **Cited In:** [126]
- **Implemented:** YES (`narrow_doorway`)

### Entering Room
- **Description:** Robot enters a room occupied by a human
- **Physical Env:** Indoor
- **Geometric Layout:** Room and door
- **Scientific Purpose:** Pedestrian interaction
- **Robot Task:** Navigate out to in
- **Human Behavior:** Navigate in to out
- **Ideal Outcome:** Robot lets human exit
- **Related Scenarios:** Entering Elevator (R@G)
- **Cited In:** R@G — Robotics at Google, an internal scenario reference (not a public citation index)
- **Implemented:** YES (`entering_room`)

### Exiting Room
- **Description:** Robot exits a room while a human enters
- **Physical Env:** Indoor
- **Geometric Layout:** Room and door
- **Scientific Purpose:** Pedestrian interaction
- **Robot Task:** Navigate in to out
- **Human Behavior:** Navigate in to out
- **Ideal Outcome:** Robot exits first
- **Related Scenarios:** Exiting Elevator (R@G)
- **Cited In:** R@G — Robotics at Google, an internal scenario reference (not a public citation index)
- **Implemented:** YES (`exiting_room`)

---

## Interpersonal Scenarios

### Join a Group
- **Description:** Robot joins a group of robots or people
- **Physical Env:** Generic
- **Geometric Layout:** Open space
- **Scientific Purpose:** Group interaction
- **Robot Task:** Navigate to group
- **Human Behavior:** Continue conversing
- **Ideal Outcome:** Robot joins group
- **Related Scenarios:** Leaving a Group
- **Cited In:** [50, 161]
- **Implemented:** YES (`join_a_group`)

### Following
- **Description:** A robot follows a person
- **Physical Env:** Generic
- **Geometric Layout:** Walking space
- **Scientific Purpose:** Joint navigation
- **Robot Role:** Servant
- **Robot Task:** Follow lead robot
- **Human Behavior:** Lead human
- **Ideal Outcome:** Robot follows person
- **Related Scenarios:** Accompany Peer
- **Cited In:** [50]
- **Implemented:** YES (`following`)

### Leading
- **Description:** A robot leads a person
- **Physical Env:** Generic
- **Geometric Layout:** Walking space
- **Scientific Purpose:** Joint navigation
- **Robot Role:** Leader
- **Robot Task:** Lead human
- **Human Behavior:** Follow robot
- **Ideal Outcome:** Person follows robot
- **Related Scenarios:** Tour Guide
- **Cited In:** [50]
- **Implemented:** YES (`leading`)

---

## Crowd Scenarios

### Crowd Navigation
- **Description:** A robot navigates through a crowd
- **Physical Env:** Generic
- **Geometric Layout:** Passable space
- **Scientific Purpose:** Crowd navigation
- **Robot Task:** Navigate thru
- **Human Behavior:** Mill about
- **Ideal Outcome:** No collision / obstruction
- **Related Scenarios:** Robot Crowding
- **Cited In:** Various
- **Implemented:** YES (`crowd_navigation`)

### Parallel Traffic
- **Description:** Crowd moves parallel to the robot
- **Physical Env:** Generic
- **Geometric Layout:** Passable space
- **Scientific Purpose:** Crowd navigation
- **Robot Task:** Navigate A to B
- **Human Behavior:** Mill from A to B
- **Ideal Outcome:** No collision / obstruction
- **Related Scenarios:** Circular Crossing
- **Cited In:** [167]
- **Implemented:** YES (`parallel_traffic`)

### Perpendicular Traffic
- **Description:** Crowd moves perpendicular to the robot
- **Physical Env:** Generic
- **Geometric Layout:** Intersection
- **Scientific Purpose:** Crowd navigation
- **Robot Task:** Cross navigate
- **Human Behavior:** Mill from A to B
- **Ideal Outcome:** No collision / obstruction
- **Related Scenarios:** Plaza Crossing
- **Cited In:** [167]
- **Implemented:** YES (`perpendicular_traffic`)

---

## Specialized Scenarios

### Object Handover
- **Description:** A robot hands an object to a human
- **Physical Env:** Generic
- **Geometric Layout:** Passable space
- **Scientific Purpose:** Interactive navigation
- **Robot Role:** Servant
- **Robot Task:** Deliver object
- **Human Behavior:** Receive object
- **Ideal Outcome:** Human takes object
- **Related Scenarios:** Robot Courier
- **Cited In:** [161]
- **Implemented:** YES (`object_handover`)

### Crash Cart
- **Description:** Robot delivering a medical product indoors
- **Physical Env:** Indoor
- **Geometric Layout:** Passable space
- **Scientific Purpose:** Interactive navigation
- **Robot Role:** Leader
- **Robot Task:** Deliver object
- **Human Behavior:** Receive object
- **Ideal Outcome:** Delivery of medicine
- **Related Scenarios:** Food Delivery
- **Cited In:** this article
- **Implemented:** YES (`crash_cart`)

---

## Additional Scenarios (Figure 7, not in Table 3)

Figure 7 illustrates several scenarios not listed as named entries in Table 3:
- **Narrow Hallway** — single-file passage in a narrow corridor
- **Entering Elevator / Exiting Elevator** — doorway variants for elevators
- **Leave Group** — inverse of Join a Group
- **Accompany Peer** — robot walks alongside a human peer
- **Circular Crossing** — pedestrians crossing in a circular pattern
- **Robot Crowding** — robot surrounded by stationary pedestrians

If implementing these, note that they do not have full Table 3 metadata and should be
extrapolated carefully from the paper's descriptions and Figure 7.

The `single_file_hallway` scenario in the repo corresponds to the Narrow Hallway figure.
The `movable_obstruction` scenario has no direct P&G Table 3 counterpart.
