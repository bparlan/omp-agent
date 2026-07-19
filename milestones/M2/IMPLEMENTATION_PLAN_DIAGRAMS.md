# Implementation Plan Diagrams

## Session Flow Diagram

```mermaid
flowchart TD
    subgraph UserSession["User Session"]
        A[Edit Framework Files] --> B[No milestone > development]
    end

    subgraph sessionAudit["session-audit Skill"]
        B --> C[Detect Milestone]
        C --> D{Milestone Exists?}
        D -->|Yes| E[Create M{X}SA{Y}.md]
        D -->|No| F[Create TEMP M{N}SA{Y}.md]
        E --> G[Analyze Changes]
        F --> G
        G --> H[Generate Outputs]
    end

    subgraph Outputs["Generated Outputs"]
        H --> I[M{X}SA{Y}.md]
        H --> J[SESSION_CHANGES.md]
        H --> K[CHANGELOG_ENTRIES.md]
        H --> L[MILESTONE_UPDATES.md]
        H --> M[INGEST_ENTRIES.md]
    end

    subgraph Documentation["Documentation Updates"]
        K --> N[docs/CHANGELOG.md]
        L --> O[docs/MILESTONES.md]
        K --> P[docs/EXPERIENCES.md]
        L --> Q[docs/ROADMAP.md]
    end

    subgraph Ingestion["Ingestion Process"]
        M --> R[Check /docs/ingest/]
        R --> S{Files Found?}
        S -->|Yes| T[Ask Permission]
        S -->|No| U[Skip Ingestion]
        T --> V{Approved?}
        V -->|Yes| W[Delegate to Skill]
        V -->|No| X[Archive Later]
        W --> Y[Archive Original]
    end

    subgraph evolveSkills["evolve-skills Skill"]
        I --> Z[Process Multiple SAs]
        I --> AA[Handle TEMP Milestones]
        I --> AB[Apply Improvements]
        AA --> AC[Promote TEMP to Formal]
        AB --> AD[Document in EVOLUTION.md]
    end

    subgraph Final["Final State"]
        N --> AE[Updated docs]
        O --> AE
        P --> AE
        Q --> AE
        I --> AF[SA Documents Tracked]
        F --> AF
        Y --> AG[Archived Files]
        AD --> AH[Framework Consistent]
    end

    I -.->|references| J
    J -.->|changes| K
    K -.->|changelog entries| N
    L -.->|milestone updates| O
    M -.->|ingest entries| R
```

## TEMP > Milestone Flow

```mermaid
flowchart LR
    subgraph Decision["Decision Tree"]
        A[Start] --> B{Milestone Exists?}
        B -->|Yes| C[Use Existing Milestone]
        B -->|No| D{TEMP Milestone Exists?}
        D -->|Yes| E[Use Existing TEMP]
        D -->|No| F[Create New TEMP]
    end

    subgraph Processing["Processing"]
        C --> G[Create SA1.md]
        E --> G
        F --> G
        G --> H[Process Changes]
    end

    subgraph Output["Output"]
        H --> I[M{X}SA{Y}.md]
        H --> J[Recommended Actions]
    end

    subgraph evolveSkills["evolve-skills"]
        I --> K[Process SA Documents]
        J --> K
        K --> L{Any TEMP Milestones?}
        L -->|Yes| M[Promote TEMP to Formal]
        L -->|No| N[Continue]
    end

    subgraph Final["Final State"]
        M --> O[Formal Milestone]
        N --> P[Continue with Current]
    end
```

## Ingestion Directory Structure

```mermaid
flowchart TD
    subgraph Ingest["docs/ingest/"]
        subgraph M2["M2/"]
            A1[sa1.md]
            A2[sa2.md]
        end
        subgraph TEMP["TEMP/"]
            B1[M1SA1.md]
            B2[M2SA1.md]
        end
        subgraph Archive["archive/"]
            C1[sa1.md]
            C2[sa2.md]
            C3[M1SA1.md]
        end
    end

    A1 -.->|archived| C1
    A2 -.->|archived| C2
    B1 -.->|archived| C3

    subgraph manageRoadmap["manage-roadmap Skill"]
        D{Check Directory}
        D -->|Files Found| E{Ask Permission}
        D -->|No Files| F[Skip]
        E -->|Approved| G[Delegate Skill]
        G --> H[Process Files]
        H --> I[Archive Original]
        E -->|Rejected| J[Keep in Directory]
    end

    I --> Archive
```

## SA Document Numbering Strategy

```mermaid
graph LR
    subgraph Normal["Normal Milestone"]
        M2[M2]
        SA1[SA1.md]
        SA2[SA2.md]
        SA3[SA3.md]
        SA4[SA4.md]

        M2 --> SA1
        SA1 --> SA2
        SA2 --> SA3
        SA3 --> SA4
    end

    subgraph TEMP["Without Milestone"]
        TEMP[TEMP/]
        M1SA1[M1SA1.md]
        M2SA1[M2SA1.md]
        M3SA1[M3SA1.md]

        TEMP --> M1SA1
        M1SA1 --> M2SA1
        M2SA1 --> M3SA1
    end

    subgraph Promotion["Promotion Flow"]
        P1[Start with TEMP]
        P2[Prompt for Permission]
        P3[Promote to Formal]
        P4[Move SA Document]

        M1SA1 --> P1
        P1 --> P2
        P2 --> P3
        P3 --> P4
        P4 --> M1
    end

    M1 -.->|promoted from| TEMP
    SA1 -.->|moved from| TEMP
```

## Code-Search Integration Flow

```mermaid
flowchart TD
    subgraph sessionAudit["session-audit"]
        A[Scan Session Changes]
        B[Detect Modified Files]
        C[Use Code-Search]
        D[Find OMP AEF Documents]
        E[Analyze Framework Changes]
        F[Verify Infrastructure Skills]
        G[Track Milestone Progress]
    end

    subgraph CodeSearch["code-search"]
        H[Semantic Search]
        I[Tree-sitter Skeletons]
        J[Pattern Matching]
        K[Repository Analysis]
    end

    C --> H
    C --> I
    C --> J
    C --> K
    D --> H
    E --> J
    F --> K
    G --> D
```

## Output File Dependencies

```mermaid
graph LR
    subgraph SA["M{X}SA{Y}.md"]
        SA1[Session Metadata]
        SA2[Files Modified]
        SA3[Classification]
        SA4[Code-Search Analysis]
        SA5[Recommended Actions]
        SA6[Dependencies]
    end

    subgraph Outputs["Generated Outputs"]
        SA1 --> O1[SESSION_CHANGES.md]
        SA2 --> O2[CHANGELOG_ENTRIES.md]
        SA2 --> O3[MILESTONE_UPDATES.md]
        SA3 --> O2
        SA3 --> O3
        SA4 --> O1
        SA4 --> O2
        SA4 --> O3
        SA5 --> O1
        SA5 --> O2
        SA5 --> O3
        SA6 --> O1
    end

    subgraph Documentation["Documentation"]
        O2 --> N1[docs/CHANGELOG.md]
        O3 --> N2[docs/MILESTONES.md]
        O1 --> N3[docs/EXPERIENCES.md]
    end

    subgraph Ingestion["Ingestion"]
        SA5 --> O4[INGEST_ENTRIES.md]
    end

    subgraph evolveSkills["evolve-skills"]
        SA5 --> A1[Apply Actions]
    end

    O4 -.->|trigger| M
```

## Testing Matrix

```mermaid
mindmap
  root((Testing))
    sessionAudit["session-audit Tests"]
      multipleSA["Multiple SA Documents"]
        test1[Create SA1 in M2/]
        test2[Create SA2 in M2/]
        test3[Verify SA2 references SA1]
        test4[Verify cumulative actions]
      tempMilestone["TEMP Milestone"]
        test5[Run without milestone]
        test6[Verify M1SA1 created]
        test7[Check temp marker]
      ingestion["Ingestion Generation"]
        test8[Generate INGEST_ENTRIES.md]
        test9[Verify all relevant files listed]
      codeSearch["Code-Search Integration"]
        test10[Find OMP AEF docs]
        test11[Analyze framework changes]
        test12[Verify infrastructure skills]
    evolveSkills["evolve-skills Tests"]
      processSA["Process Multiple SAs"]
        test13[Process SA1 and SA2]
        test14[Verify cumulative actions]
        test15[Document in EVOLUTION.md]
      tempMilestone2["Handle TEMP"]
        test16[Process M1SA1]
        test17[Mark temp in EVOLUTION.md]
      promotion["Promotion Flow"]
        test18[Prompt for promotion]
        test19[Move TEMP to formal]
        test20[Update framework references]
    manageRoadmap["manage-roadmap Tests"]
      checkIngest["Check Ingestion"]
        test21[Create docs/ingest/ files]
        test22[Run manage-roadmap]
        test23[Verify permission prompt]
        test24[Verify context prompt]
      processIngest["Process Ingestion"]
        test25[Approve ingestion]
        test26[Delegate to skill]
        test27[Archive original file]
      noIngest["No Ingestion"]
        test28[Remove ingest files]
        test29[Verify skip behavior]
    integration["Integration Tests"]
      endToEnd["End-to-End"]
        test30[User session → SA → evolve-skills → docs updated]
      rollback["Rollback"]
        test31[Restore from EVOLUTION.md]
```

## Decision Flow

```mermaid
flowchart TD
    subgraph Input["Input"]
        A[User Session Work]
        B[Modified Files]
    end

    subgraph Decision["Decisions"]
        C{Milestone Exists?}
        D{File is Cosmetic?}
        E{Files in /docs/ingest/?}
    end

    subgraph Actions["Actions"]
        F[Create SA Document]
        G[Skip Documentation]
        H{User Approved?}
        I[Delegate Skill]
        J[Archive File]
        K{Temp to Formal?}
    end

    subgraph Output["Output"]
        L[M{X}SA{Y}.md]
        M[SKIP]
        N[Change Applied]
        O[File Archived]
        P[Promoted to Formal]
    end

    A --> B
    B --> C
    C -->|Yes| F
    C -->|No| G
    B --> D
    D -->|Yes| G
    D -->|No| H
    B --> E
    E -->|Yes| H
    E -->|No| I
    H -->|Yes| I
    H -->|No| M
    I --> J
    I --> K
    K -->|Yes| P
    K -->|No| N

    F --> L
    G --> M
    I --> O
```

## Timeline

```mermaid
gantt
    title Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Day 1
    Core SA Document Format      :a1, 2026-07-18, 8h
    Comprehensive Documentation   :a2, after a1, 8h
    TEMP > Milestone Reverse Order :a3, after a2, 8h
    section Day 2
    /docs/ingest/ Folder          :b1, after a3, 8h
    evolve-skills Enhancement     :b2, after b1, 8h
    Testing and Validation        :b3, after b2, 8h
    Documentation Updates         :b4, after b3, 4h
    Final Review                  :b5, after b4, 4h
```

---

All diagrams provided for implementation visualization and testing strategy.
