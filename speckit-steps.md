# SDD Overview
## Attempts
4 attempts (you can delete the spec folder unders /specs if you want to start over)

## Approval Fatigue
Each step requires approval before proceeding to the next step.
## Sequence 
specify → clarify → plan → tasks → checklist → analyze → implement

## Prompts 
in my case have the prompts
.windsurf/rules/specify.md
.windsurf/workflows/

## Constitution 
constitution files are in
.specify/memory/
.specify/templates/
.specify/scripts/



## Steps

**/speckit.specify** 
/speckit.specify visualize daily wisdom feature helps user view the daily wisdom on the landing page of the application. Use UTC time respresentation, do not show the same wisdom in 365 days, rotate the wisdom daily, display the wisdom in a card with a title and description, and a button to copy the wisdom to the clipboard.

**/speckit.clarify** 
/speckit.clarify to remove [NEEDS CLARIFICATION] markers

**/speckit.plan** 
/speckit.plan Reactjs SPA application with Fast API python backend. Database is postgres and is already deployed and running in local docker. Connection string is in the database.md constitution file. Strictly do not attempt to create tables, or database or brew to install database locally.

**/speckit.tasks** 
/speckit.tasks 

**/speckit.checklist** 
/speckit.checklist 

**/speckit.analyze** 
/speckit.analyze 

**/speckit.implement** 
/speckit.implement 





# checklist output
UI/UX Checklist Complete
I've successfully generated a lightweight UI/UX requirements checklist for the daily wisdom display feature. Here's what was accomplished:

Checklist Generated
File: ux.md

Checklist Focus
Purpose: Lightweight sanity check for UI/UX requirement quality
Audience: Feature author self-validation during spec writing
Scope: Visual design, interaction patterns, and user experience specifications
Coverage Areas (40 total checks)
Requirement Completeness (7 checks)

Visual specifications for wisdom card
Card layout and positioning
Loading/error/empty state requirements
Responsive design specifications
Requirement Clarity (6 checks)

Quantified "attractive card format" criteria
Visual feedback specifications
Typography and spacing requirements
Requirement Consistency (4 checks)

Consistent visual patterns across states
Alignment with existing UI patterns
Acceptance Criteria Quality (4 checks)

Measurable visual acceptance criteria
Objective verification methods
Scenario Coverage (4 checks)

Midnight rollover scenarios
Consecutive day visits
Clipboard fallback scenarios
Edge Case Coverage (4 checks)

Long content handling
Permission denied scenarios
Network timeout scenarios
Non-Functional Requirements (4 checks)

Accessibility requirements
Performance specifications
Low-bandwidth considerations
Dependencies & Assumptions (3 checks)

Component library dependencies
Browser capability assumptions
Ambiguities & Conflicts (3 checks)

Visual hierarchy clarity
Requirement conflict detection
Usage
This checklist serves as "unit tests for requirements" - validating that the UI/UX specifications are complete, clear, and ready for implementation. Each item tests the quality of the written requirements rather than the implementation itself.

The checklist is now ready for the author to use during spec refinement or for peers during review. You can proceed to /speckit.analyze for cross-artifact analysis or /speckit.implement to begin development.

Feedback submitted




Command Awaiting Approval








Drop to add to agent



