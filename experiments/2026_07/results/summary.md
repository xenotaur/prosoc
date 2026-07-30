# 2026_07 packet combinatorics — summary

One assembled packet per (task, context, scenario) combination. See `combinations.py` for the rationale behind each pick.

| id | task | context | scenario | emphasized | deprioritized |
|---|---|---|---|---|---|
| `lead_docent_leading` | navigate_lead_agent | guidance_docent | leading | P2, P3, P9 | P0 |
| `lead_docent_crowd_navigation` | navigate_lead_agent | guidance_docent | crowd_navigation | P2, P3, P9 | P0 |
| `lead_docent_join_a_group` | navigate_lead_agent | guidance_docent | join_a_group | P2, P3, P9 | P0 |
| `deliver_routine_pedestrian_overtaking` | deliver_object | routine_delivery | pedestrian_overtaking | P0, P1, P2, P3, P9 |  |
| `deliver_routine_object_handover` | deliver_object | routine_delivery | object_handover | P0, P1, P2, P3, P9 |  |
| `deliver_routine_movable_obstruction` | deliver_object | routine_delivery | movable_obstruction | P0, P1, P2, P3, P9 |  |
| `deliver_urgent_crash_cart` | deliver_object | high_urgency | crash_cart | P0, P1, P9 | P2, P3 |
| `deliver_urgent_pedestrian_overtaking` | deliver_object | high_urgency | pedestrian_overtaking | P0, P1, P9 | P2, P3 |
| `deliver_urgent_movable_obstruction` | deliver_object | high_urgency | movable_obstruction | P0, P1, P9 | P2, P3 |
| `follow_public_following` | navigate_follow_agent | public_navigation | following | P1, P2, P3 | P0 |
| `follow_public_object_handover` | navigate_follow_agent | public_navigation | object_handover | P1, P2, P3 | P0 |
| `follow_public_join_a_group` | navigate_follow_agent | public_navigation | join_a_group | P1, P2, P3 | P0 |
| `pointtopoint_public_frontal_approach` | navigate_point_to_point | public_navigation | frontal_approach | P1, P2, P3 | P0 |
| `pointtopoint_public_intersection_no_gesture` | navigate_point_to_point | public_navigation | intersection_no_gesture | P1, P2, P3 | P0 |
| `pointtopoint_public_single_file_hallway` | navigate_point_to_point | public_navigation | single_file_hallway | P1, P2, P3 | P0 |

## Highlighted diffs: same scenario + task, different context

### `deliver_object` × `pedestrian_overtaking`, varying context
- **routine_delivery**: emphasized=['P0', 'P1', 'P2', 'P3', 'P9'], deprioritized=[]
- **high_urgency**: emphasized=['P0', 'P1', 'P9'], deprioritized=['P2', 'P3']

### `deliver_object` × `movable_obstruction`, varying context
- **routine_delivery**: emphasized=['P0', 'P1', 'P2', 'P3', 'P9'], deprioritized=[]
- **high_urgency**: emphasized=['P0', 'P1', 'P9'], deprioritized=['P2', 'P3']

