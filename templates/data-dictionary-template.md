# 🟢 SKILL-11: DATA DICTIONARY TEMPLATE
## Template Skill - Data Dictionary & Glossary

---

## 📌 SKILL METADATA

| Attribute | Value |
|-----------|-------|
| **Template ID** | TMPL-DD |
| **Category** | 🟢 Template |
| **Load When** | Documenting data elements, entities, and business terminology |
| **Dependencies** | @ba-writing, @ba-process |
| **Output** | Complete Data Dictionary document |

---

## 🎯 WHEN TO USE DATA DICTIONARY

| Use Data Dictionary When | Don't Use When |
|--------------------------|----------------|
| ✓ Defining data elements across systems | ✗ High-level process flows (use Use Case) |
| ✓ Aligning business and technical teams on data | ✗ UI layout documentation (use wireframes) |
| ✓ Integrating multiple data sources | ✗ Only one team owns the data |
| ✓ Establishing data governance standards | ✗ Volatile early-discovery phase |
| ✓ Onboarding new analysts or developers | ✗ Non-data requirements (use BRD/FRD) |

---

## 📋 DATA DICTIONARY TEMPLATE

```
═══════════════════════════════════════════════════════════════
                       DATA DICTIONARY
                      [Project / System Name]
═══════════════════════════════════════════════════════════════

Document Control
────────────────────────────────────────────────────────────────
Version: [X.Y]
Date: [YYYY-MM-DD]
Author: [Name]
Status: [Draft/Review/Approved]

Version History
┌─────────┬────────────┬──────────┬─────────────────────────────┐
│ Version │ Date       │ Author   │ Changes                     │
├─────────┼────────────┼──────────┼─────────────────────────────┤
│ 0.1     │ YYYY-MM-DD │ [Name]   │ Initial draft               │
│ 1.0     │ YYYY-MM-DD │ [Name]   │ Approved version            │
└─────────┴────────────┴──────────┴─────────────────────────────┘

═══════════════════════════════════════════════════════════════
SECTION 1: DATA FIELD ENTRIES
═══════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────
FIELD: [field_name]          Entity: [EntityName]
────────────────────────────────────────────────────────────────
┌─────────────────────┬──────────────────────────────────────┐
│ Attribute           │ Value                                │
├─────────────────────┼──────────────────────────────────────┤
│ Field Name          │ [snake_case or camelCase field name] │
│ Display Label       │ [Human-readable label]               │
│ Data Type           │ [VARCHAR/INT/DECIMAL/DATE/BOOLEAN]   │
│ Length / Precision  │ [e.g., VARCHAR(255) / DECIMAL(10,2)] │
│ Format              │ [e.g., YYYY-MM-DD / ###-##-####]     │
│ Nullable            │ [Yes / No]                           │
│ Default Value       │ [Value or NULL]                      │
├─────────────────────┼──────────────────────────────────────┤
│ Description         │ [Technical description of the field] │
│ Business Definition │ [Plain-English meaning for business] │
├─────────────────────┼──────────────────────────────────────┤
│ Source System       │ [Which system originates this data]  │
│ Source Field        │ [Original field name in source]      │
├─────────────────────┼──────────────────────────────────────┤
│ Constraints         │                                      │
│  - Required         │ [Yes / No / Conditional on ...]      │
│  - Unique           │ [Yes / No / Unique within ...]       │
│  - Min / Max        │ [e.g., 0 to 999999.99]               │
│  - Pattern          │ [Regex or format rule]               │
├─────────────────────┼──────────────────────────────────────┤
│ Valid Values        │ [Enumeration or "See lookup table"]  │
│ Invalid Examples    │ [Common invalid inputs to reject]    │
├─────────────────────┼──────────────────────────────────────┤
│ Related Fields      │ [FK → EntityName.field_name]         │
│ Business Rules      │ [BR-XXX: Rule that governs this]     │
└─────────────────────┴──────────────────────────────────────┘

Valid Values / Enumeration (if applicable):
┌────────────────┬───────────────────────────────────────────┐
│ Code / Value   │ Business Meaning                          │
├────────────────┼───────────────────────────────────────────┤
│ [A]            │ [What A means]                            │
│ [B]            │ [What B means]                            │
│ [C]            │ [What C means]                            │
└────────────────┴───────────────────────────────────────────┘

Change History:
┌────────────┬───────────────────────────────┬──────────────┐
│ Date       │ Change                        │ Changed By   │
├────────────┼───────────────────────────────┼──────────────┤
│ YYYY-MM-DD │ [What was changed and why]    │ [Name]       │
└────────────┴───────────────────────────────┴──────────────┘

[Repeat field block above for each field in the entity]

═══════════════════════════════════════════════════════════════
SECTION 2: ENTITY SUMMARY
═══════════════════════════════════════════════════════════════

┌──────────────────┬───────────────────────────────────────────┐
│ Entity Name      │ [EntityName]                              │
│ Description      │ [What this entity represents]             │
│ Source System    │ [Originating system or database]          │
│ Table / Object   │ [Physical table or object name]           │
│ Attribute Count  │ [Total number of fields]                  │
│ Primary Key      │ [PK field name(s)]                        │
│ Natural Key      │ [Business-meaningful unique identifier]   │
└──────────────────┴───────────────────────────────────────────┘

Entity Relationships:
┌─────────────────┬──────────────┬──────────────────────────────┐
│ Related Entity  │ Relationship │ Description                  │
├─────────────────┼──────────────┼──────────────────────────────┤
│ [EntityName]    │ 1:N          │ [How they relate]            │
│ [EntityName]    │ N:M          │ [Via junction table: ...]    │
└─────────────────┴──────────────┴──────────────────────────────┘

Attribute Overview:
┌────────────────────┬─────────────┬──────────┬────────────────┐
│ Field Name         │ Type        │ Required │ Notes          │
├────────────────────┼─────────────┼──────────┼────────────────┤
│ [field_name]       │ [Type]      │ Yes      │ PK             │
│ [field_name]       │ [Type]      │ Yes      │                │
│ [field_name]       │ [Type]      │ No       │ FK → Entity    │
└────────────────────┴─────────────┴──────────┴────────────────┘

═══════════════════════════════════════════════════════════════
SECTION 3: GLOSSARY
═══════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────
TERM: [Business Term]
────────────────────────────────────────────────────────────────
┌──────────────────┬─────────────────────────────────────────┐
│ Term             │ [Exact term as used in the business]    │
│ Definition       │ [Clear, unambiguous definition]         │
│ Synonyms         │ [Other names used in the organization]  │
│ Abbreviation     │ [e.g., ROI, NPS, SKU]                   │
│ Context          │ [Domain or department where used]       │
│ Related Terms    │ [Linked glossary entries]               │
│ Do NOT Confuse   │ [Similar terms with different meanings] │
└──────────────────┴─────────────────────────────────────────┘

[Repeat glossary block for each business term]
```

---

## ✅ DATA DICTIONARY QUALITY CHECKLIST

```
☐ Every field has both technical and business definition
☐ Data types and lengths specified for all fields
☐ Nullable and required constraints documented
☐ Valid value enumerations listed for coded fields
☐ Source system and source field name captured
☐ Foreign key relationships identified
☐ Business rules referenced by ID
☐ Change history maintained
☐ Entity relationships documented
☐ Glossary terms cover all domain-specific language
☐ No field left with "TBD" in required attributes
☐ Approved by data steward / business owner
```

---

## 🔗 RELATED SKILLS

| After Data Dictionary... | Load |
|--------------------------|------|
| Map to API payloads | @ba-writing (API Contract Template) |
| Write data validation rules | @ba-process |
| Create ERD / data model | @ba-writing |

---

*Use this template to create a single source of truth for all data elements across systems.*
