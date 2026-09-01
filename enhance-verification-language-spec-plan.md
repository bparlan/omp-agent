Enhance generate-verification skill with explicit language specification

## Context
The generate-verification skill transforms implementation specifications into deterministic verification protocols but lacks explicit language specification for verification items. Verification items currently contain structured fields without enforced language consistency requirements.

## Approach
1. **Enhanced Verification Item Contract**: Add mandatory `language` field to every verification item
2. **Language Validation**: Enforce ISO 639-1 language code validation
3. **Language Consistency**: Ensure all content within each verification item is expressed in the specified language
4. **Enhanced Quality Gates**: Add language-specific validation checkpoints
5. **Failure Conditions**: Block verification items missing language specification

## Implementation Steps

### Step 1: Update Verification Item Contract
- Add `language` field to verification item structure
- Validate ISO 639-1 language code format
- Ensure language field presence in all verification items

### Step 2: Language Validation Gate
- Validate every verification item contains `language` field
- Check language codes against ISO 639-1 standard
- Enforce language consistency across all item content

### Step 3: Enhanced Quality Gates
- Add language validation to mechanical validation
- Include language-specific failure conditions
- Ensure system awareness respects language boundaries

### Step 4: Output Generation
- Generate verification protocol with validated language fields
- Include language consistency checks in output validation
- Add language validation to system validation

## Critical Files & Anchors
- `skill://generate-verification` - Primary skill definition
- `milestones/M{X}/M{X}S{Y}/M{X}S{Y}.md` - Specification source files
- `milestones/M{X}/M{X}S{Y}V.md` - Generated verification protocol files

## Verification
- Test language field presence in verification items
- Validate ISO 639-1 language codes
- Test language consistency across verification item content
- Verify language validation gates block items without language specification

## Assumptions & Contingencies
- ISO 639-1 language codes are standardized and available
- Specification content can be validated for language consistency
- Generated verification items maintain language consistency

## Next Steps
Upon approval:
1. Update generate-verification skill implementation
2. Add language validation gates and quality checks
3. Test with existing specification verification generation
4. Deploy enhanced verification protocol with language specification