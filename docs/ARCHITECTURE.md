\# Career Memory Architecture



```

&#x20;                 Career Memory



&#x20;                    main.py

&#x20;                       │

&#x20;                       ▼

&#x20;              Connector Manager

&#x20;                       │

&#x20;       ┌───────────────┼───────────────┐

&#x20;       ▼               ▼               ▼

&#x20;    Gmail         LinkedIn          Dice

&#x20;       │               │               │

&#x20;       └───────────────┼───────────────┘

&#x20;                       ▼

&#x20;                 CareerEvent

&#x20;                       ▼

&#x20;               Entity Extraction

&#x20;                       ▼

&#x20;                  Classification

&#x20;                       ▼

&#x20;                   Analytics

&#x20;                       ▼

&#x20;                   AI Assistant

```



\## Core Components



\### Connectors



Responsible for loading career data from external systems.



\### CareerEvent



The canonical model representing every professional interaction.



\### Classifier



Determines interaction types such as:



\* Outreach

\* RTR Request

\* Interview

\* Assessment

\* Offer

\* Rejection



\### Analytics



Aggregates interactions into recruiter, agency, client, and timeline metrics.



\### AI Layer



Allows natural-language queries across a user's career history.



