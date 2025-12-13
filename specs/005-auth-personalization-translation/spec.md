# Feature Specification: User Authentication, Personalization & Urdu Translation

**Feature Branch**: `005-auth-personalization-translation`
**Created**: 2025-12-13
**Status**: Draft
**Input**: User description: "Implement user signup/signin with Better-Auth, background questionnaire, personalized chapter content, and Urdu translation for logged-in users"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Account Registration (Priority: P1)

A new visitor to the Physical AI & Humanoid Robotics book wants to create an account so they can access personalized content. They navigate to the signup page, enter their email, password, and name, then complete a brief background questionnaire about their software and hardware experience.

**Why this priority**: Authentication is the foundational feature that enables all personalization and translation features. Without user accounts, no user-specific features can function.

**Independent Test**: Can be fully tested by navigating to /signup, filling out the form with valid credentials, completing the background questionnaire, and verifying the user can subsequently log in.

**Acceptance Scenarios**:

1. **Given** a visitor on the signup page, **When** they enter a valid email, password (min 8 characters), and name, **Then** they proceed to the background questionnaire step
2. **Given** a user in the questionnaire step, **When** they answer all required background questions, **Then** their account is created and they are automatically signed in
3. **Given** a user attempting signup, **When** they enter an email that already exists, **Then** they see an error message indicating the email is already registered
4. **Given** a user with incomplete password, **When** they submit the form with less than 8 characters, **Then** they see a validation error

---

### User Story 2 - User Sign In and Sign Out (Priority: P1)

A returning user wants to sign in to their existing account to access personalized content. They enter their credentials, sign in successfully, and can later sign out when finished.

**Why this priority**: Sign-in is essential for users to access their personalized experience across sessions.

**Independent Test**: Can be tested by navigating to /signin, entering valid credentials, verifying the user is authenticated and can access protected features, then signing out.

**Acceptance Scenarios**:

1. **Given** a registered user on the signin page, **When** they enter valid email and password, **Then** they are signed in and redirected to the homepage with their session active
2. **Given** an authenticated user, **When** they click the sign out button in the navbar, **Then** their session is terminated and they see the guest navigation options
3. **Given** a user attempting signin, **When** they enter an incorrect password, **Then** they see an error message without revealing which field was incorrect
4. **Given** an authenticated user, **When** they close the browser and return later, **Then** their session is restored if the session token hasn't expired

---

### User Story 3 - Content Personalization (Priority: P2)

A logged-in user reading a chapter wants to personalize the content based on their background. They click the "Personalize Content" button, and the chapter text is adapted to their experience level and domain expertise.

**Why this priority**: Personalization is the primary value proposition for registered users, transforming generic content into tailored learning material.

**Independent Test**: Can be tested by logging in as a user with a defined background, navigating to any chapter, clicking "Personalize Content", and verifying the content changes to match their background.

**Acceptance Scenarios**:

1. **Given** a logged-in user with hardware background on a chapter page, **When** they click "Personalize Content", **Then** the chapter content includes additional robotics explanations and hardware-focused examples
2. **Given** a logged-in user with software background on a chapter page, **When** they click "Personalize Content", **Then** the chapter content includes more ROS 2 and AI-focused explanations
3. **Given** a logged-in beginner user, **When** they click "Personalize Content", **Then** the content is simplified with more foundational explanations
4. **Given** a logged-in advanced user, **When** they click "Personalize Content", **Then** the content includes deeper technical details and advanced concepts
5. **Given** a user viewing personalized content, **When** they click "Reset to Original", **Then** the original chapter content is restored

---

### User Story 4 - Urdu Translation (Priority: P2)

A logged-in user who prefers reading in Urdu clicks the "Translate to Urdu" button to view the chapter content in Urdu while preserving technical terminology correctly.

**Why this priority**: Urdu translation expands accessibility to Urdu-speaking users who may find English challenging, while maintaining technical accuracy.

**Independent Test**: Can be tested by logging in, navigating to any chapter, clicking "Translate to Urdu", and verifying the content is displayed in Urdu with technical terms preserved or transliterated appropriately.

**Acceptance Scenarios**:

1. **Given** a logged-in user on a chapter page, **When** they click "Translate to Urdu", **Then** the chapter content is displayed in Urdu script
2. **Given** translated content, **When** displaying technical terms like "ROS 2", "LIDAR", or "neural network", **Then** these terms are preserved in English or transliterated according to the glossary rules
3. **Given** a user viewing Urdu translation, **When** they click "Reset to Original", **Then** the English version is restored
4. **Given** any chapter with code blocks, **When** translated to Urdu, **Then** code blocks remain in English without modification

---

### User Story 5 - Chapter Controls Visibility (Priority: P3)

When a user navigates to a chapter, the "Personalize Content" and "Translate to Urdu" buttons are only visible and functional if the user is logged in with a completed background questionnaire.

**Why this priority**: Ensures a clean experience for guests while incentivizing account creation for value-added features.

**Independent Test**: Can be tested by viewing a chapter as a guest (no buttons visible), then logging in and refreshing to see the buttons appear.

**Acceptance Scenarios**:

1. **Given** a guest user (not logged in) on a chapter page, **When** the page loads, **Then** the "Personalize Content" and "Translate to Urdu" buttons are not visible
2. **Given** a logged-in user without a completed background questionnaire, **When** they view a chapter, **Then** they see a prompt to complete their background questionnaire instead of the personalization button
3. **Given** a logged-in user with a completed background, **When** they view a chapter, **Then** both buttons are visible and functional

---

### User Story 6 - Profile Management (Priority: P3)

A logged-in user wants to view and update their profile information and background questionnaire responses.

**Why this priority**: Allows users to correct or update their background as their expertise evolves, improving personalization accuracy.

**Independent Test**: Can be tested by logging in, navigating to /profile, viewing current profile and background data, making updates, and verifying changes are saved.

**Acceptance Scenarios**:

1. **Given** a logged-in user, **When** they navigate to /profile, **Then** they see their email, name, and background questionnaire responses
2. **Given** a user on the profile page, **When** they update their background answers and save, **Then** the changes are persisted and future personalizations reflect the new background

---

### Edge Cases

- What happens when a user requests personalization but their session has expired? → User is redirected to signin page
- What happens when translation service is temporarily unavailable? → User sees an error message with option to retry, original content remains displayed
- How does the system handle very long chapters during personalization? → Content is processed in chunks with progress indication
- What happens if a user clicks "Personalize" while personalization is in progress? → Button is disabled during processing to prevent duplicate requests
- What happens when network connectivity is lost during transformation? → Operation fails gracefully with error message, original content preserved

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication

- **FR-001**: System MUST allow users to create accounts with email, password, and display name
- **FR-002**: System MUST validate email format and password strength (minimum 8 characters)
- **FR-003**: System MUST hash passwords securely before storage
- **FR-004**: System MUST issue session tokens upon successful authentication
- **FR-005**: System MUST support session-based authentication with configurable expiry
- **FR-006**: System MUST allow users to sign out, invalidating their session
- **FR-007**: System MUST prevent duplicate account creation with the same email

#### Background Questionnaire

- **FR-008**: System MUST collect user background information during or after signup
- **FR-009**: Background questionnaire MUST capture software experience level (none, beginner, intermediate, advanced)
- **FR-010**: Background questionnaire MUST capture hardware experience level (none, beginner, intermediate, advanced)
- **FR-011**: Background questionnaire MUST capture primary domain interest (software-focused, hardware-focused, balanced)
- **FR-012**: Background questionnaire MAY capture specific skills (e.g., Python, ROS, Arduino, LIDAR)
- **FR-013**: System MUST persist background responses associated with user account

#### Content Personalization

- **FR-014**: System MUST personalize chapter content based on user's stored background
- **FR-015**: Personalization MUST adapt content complexity based on experience level
- **FR-016**: Personalization MUST emphasize domain-relevant examples (robotics for hardware, ROS 2/AI for software)
- **FR-017**: Personalization MUST NOT alter factual meaning or technical accuracy
- **FR-018**: System MUST allow users to reset to original content after personalization
- **FR-019**: System MUST log all personalization requests with timestamps

#### Urdu Translation

- **FR-020**: System MUST translate chapter content to Urdu for logged-in users
- **FR-021**: Translation MUST preserve technical terms according to defined glossary rules
- **FR-022**: Translation MUST NOT translate code blocks, file names, or command examples
- **FR-023**: Translation MUST be performed server-side, not client-side
- **FR-024**: System MUST allow users to reset to English after translation
- **FR-025**: System MUST log all translation requests with timestamps

#### UI Requirements

- **FR-026**: Chapter pages MUST display "Personalize Content" and "Translate to Urdu" buttons for authenticated users with background data
- **FR-027**: Buttons MUST be hidden for unauthenticated users
- **FR-028**: Buttons MUST show loading state during transformation operations
- **FR-029**: System MUST display error messages for failed operations
- **FR-030**: Transformed content MUST render correctly preserving MDX formatting

#### Integration

- **FR-031**: Authentication MUST integrate with existing FastAPI backend
- **FR-032**: User data MUST be stored in existing Neon Postgres database
- **FR-033**: Personalization/translation MUST NOT interfere with existing RAG chatbot functionality
- **FR-034**: Navbar MUST show appropriate auth status (Sign In/Sign Up or User name/Sign Out)

### Non-Functional Requirements

#### Security

- **NFR-001**: Passwords MUST be hashed using industry-standard algorithms (bcrypt or Argon2)
- **NFR-002**: Session tokens MUST be cryptographically secure and unpredictable
- **NFR-003**: All authentication endpoints MUST be rate-limited to prevent brute force attacks
- **NFR-004**: User data MUST be transmitted over HTTPS only in production
- **NFR-005**: Password reset tokens MUST expire after single use or time limit

#### Performance

- **NFR-006**: Authentication operations MUST complete within 2 seconds
- **NFR-007**: Content personalization MUST complete within 15 seconds for typical chapter length
- **NFR-008**: Content translation MUST complete within 15 seconds for typical chapter length
- **NFR-009**: System MUST handle at least 50 concurrent authenticated users
- **NFR-010**: Rate limiting MUST be enforced: 10 transformation requests per user per hour

#### Content Quality

- **NFR-011**: Personalized content MUST maintain technical accuracy of original content
- **NFR-012**: Translated content MUST preserve meaning and technical accuracy
- **NFR-013**: System MUST use controlled LLM prompts to prevent hallucinations
- **NFR-014**: Technical glossary MUST be applied consistently in translations

#### Accessibility & UX

- **NFR-015**: All form inputs MUST have appropriate labels for screen readers
- **NFR-016**: Error messages MUST be descriptive and actionable
- **NFR-017**: Loading states MUST be clearly indicated to users
- **NFR-018**: Transformed content MUST maintain the same heading structure and navigation

#### Compatibility

- **NFR-019**: Features MUST work alongside existing RAG chatbot without interference
- **NFR-020**: Features MUST be compatible with Docusaurus's MDX rendering
- **NFR-021**: Authentication state MUST be synchronized with chatbot context

### Key Entities

- **User**: Represents a registered user with email, password hash, display name, and creation timestamp
- **UserBackground**: Stores user's software experience, hardware experience, domain focus, and specific skills list
- **Session**: Tracks active user sessions with token, expiry time, and user association
- **TransformationLog**: Records all personalization and translation requests with user, chapter, transformation type, timestamps, and outcome

## Data Schema

### User Table (Better-Auth compatible)

| Field         | Description                                    |
|---------------|------------------------------------------------|
| id            | Unique user identifier                         |
| email         | User email address (unique)                    |
| name          | Display name                                   |
| password_hash | Securely hashed password                       |
| email_verified| Whether email is verified                      |
| image         | Optional profile image URL                     |
| created_at    | Account creation timestamp                     |
| updated_at    | Last update timestamp                          |

### Session Table

| Field      | Description                              |
|------------|------------------------------------------|
| id         | Unique session identifier                |
| token      | Session token (unique, indexed)          |
| expires_at | Session expiration timestamp             |
| user_id    | Foreign key to user                      |
| ip_address | Client IP address                        |
| user_agent | Client user agent string                 |
| created_at | Session creation timestamp               |
| updated_at | Last activity timestamp                  |

### UserBackground Table

| Field              | Description                                          |
|--------------------|------------------------------------------------------|
| id                 | Unique background identifier                         |
| user_id            | Foreign key to user (unique, one-to-one)             |
| software_experience| Enum: none, beginner, intermediate, advanced         |
| hardware_experience| Enum: none, beginner, intermediate, advanced         |
| domain_focus       | Enum: software, hardware, balanced                   |
| skills             | Array of skill tags (e.g., Python, ROS, Arduino)     |
| created_at         | Background creation timestamp                        |
| updated_at         | Last update timestamp                                |

### TransformationLog Table

| Field            | Description                                       |
|------------------|---------------------------------------------------|
| id               | Unique log identifier                             |
| user_id          | Foreign key to user                               |
| chapter_slug     | Identifier for the transformed chapter           |
| transformation_type | Enum: personalization, translation              |
| input_length     | Character count of original content               |
| output_length    | Character count of transformed content            |
| duration_ms      | Processing time in milliseconds                   |
| status           | Enum: success, failure                            |
| error_message    | Error details if failed (nullable)                |
| created_at       | Request timestamp                                 |

## API Requirements

### POST /auth/signup

**Description**: Register a new user account with optional background data.

**Request Format**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe",
  "background": {
    "software_experience": "intermediate",
    "hardware_experience": "beginner",
    "domain_focus": "software",
    "skills": ["Python", "ROS 2"]
  }
}
```

**Response Format (201 Created)**:
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "session_token_here",
  "expires_at": "2025-12-20T00:00:00Z"
}
```

**Error States**:
- 400: Invalid email format, weak password, or missing required fields
- 409: Email already registered
- 429: Rate limit exceeded

**Rate Limit**: 5 requests per IP per minute

**Logging**: Log signup attempts (success/failure, email, timestamp)

---

### POST /auth/signin

**Description**: Authenticate an existing user.

**Request Format**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response Format (200 OK)**:
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "has_background": true
  },
  "token": "session_token_here",
  "expires_at": "2025-12-20T00:00:00Z"
}
```

**Error States**:
- 400: Missing required fields
- 401: Invalid credentials
- 429: Rate limit exceeded

**Rate Limit**: 10 requests per IP per minute

**Logging**: Log signin attempts (success/failure, email, timestamp, IP)

---

### POST /auth/signout

**Description**: Invalidate the current session.

**Auth Required**: Yes (Bearer token)

**Response Format (200 OK)**:
```json
{
  "message": "Successfully signed out"
}
```

**Error States**:
- 401: Invalid or missing token

---

### GET /auth/session

**Description**: Get current session information.

**Auth Required**: Yes (Bearer token)

**Response Format (200 OK)**:
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "session": {
    "id": "session_uuid",
    "expires_at": "2025-12-20T00:00:00Z"
  },
  "has_background": true
}
```

**Error States**:
- 401: Invalid or expired session

---

### GET /profile/background

**Description**: Get user's background questionnaire data.

**Auth Required**: Yes (Bearer token)

**Response Format (200 OK)**:
```json
{
  "software_experience": "intermediate",
  "hardware_experience": "beginner",
  "domain_focus": "software",
  "skills": ["Python", "ROS 2"]
}
```

**Error States**:
- 401: Unauthorized
- 404: Background not completed

---

### PUT /profile/background

**Description**: Create or update user's background questionnaire.

**Auth Required**: Yes (Bearer token)

**Request Format**:
```json
{
  "software_experience": "advanced",
  "hardware_experience": "intermediate",
  "domain_focus": "balanced",
  "skills": ["Python", "ROS 2", "Arduino", "LIDAR"]
}
```

**Response Format (200 OK)**:
```json
{
  "message": "Background updated successfully",
  "background": {
    "software_experience": "advanced",
    "hardware_experience": "intermediate",
    "domain_focus": "balanced",
    "skills": ["Python", "ROS 2", "Arduino", "LIDAR"]
  }
}
```

**Error States**:
- 400: Invalid experience level or domain focus values
- 401: Unauthorized

---

### POST /content/personalize

**Description**: Personalize chapter content based on user background.

**Auth Required**: Yes (Bearer token, with completed background)

**Request Format**:
```json
{
  "chapter_slug": "introduction-to-ros2",
  "content": "The original chapter content in MDX format..."
}
```

**Response Format (200 OK)**:
```json
{
  "personalized_content": "The personalized chapter content...",
  "processing_time_ms": 2500,
  "background_applied": {
    "experience_level": "intermediate",
    "domain_focus": "software"
  }
}
```

**Error States**:
- 400: Missing content or invalid chapter slug
- 401: Unauthorized
- 403: Background questionnaire not completed
- 429: Rate limit exceeded (10/hour/user)
- 503: Personalization service unavailable

**Rate Limit**: 10 requests per user per hour

**Logging**: Log request to TransformationLog table

---

### POST /content/translate

**Description**: Translate chapter content to Urdu.

**Auth Required**: Yes (Bearer token)

**Request Format**:
```json
{
  "chapter_slug": "introduction-to-ros2",
  "content": "The original chapter content in MDX format...",
  "target_language": "urdu"
}
```

**Response Format (200 OK)**:
```json
{
  "translated_content": "اردو میں ترجمہ شدہ مواد...",
  "processing_time_ms": 3200,
  "preserved_terms": ["ROS 2", "LIDAR", "neural network"]
}
```

**Error States**:
- 400: Missing content or invalid parameters
- 401: Unauthorized
- 429: Rate limit exceeded (10/hour/user)
- 503: Translation service unavailable

**Rate Limit**: 10 requests per user per hour

**Logging**: Log request to TransformationLog table

---

### GET /content/logs

**Description**: Get user's transformation history.

**Auth Required**: Yes (Bearer token)

**Query Parameters**:
- `limit` (optional, default 20, max 100)
- `offset` (optional, default 0)
- `type` (optional: personalization, translation)

**Response Format (200 OK)**:
```json
{
  "logs": [
    {
      "id": "uuid",
      "chapter_slug": "introduction-to-ros2",
      "transformation_type": "personalization",
      "status": "success",
      "duration_ms": 2500,
      "created_at": "2025-12-13T10:30:00Z"
    }
  ],
  "total": 15,
  "limit": 20,
  "offset": 0
}
```

## Personalization Logic

### Experience-Based Adaptation

| User Level | Content Adaptation |
|------------|-------------------|
| Beginner   | Simplify technical jargon, add foundational context, include "What this means" explanations |
| Intermediate | Maintain technical accuracy, add practical examples, link related concepts |
| Advanced   | Include deeper technical details, optimization tips, edge cases, and advanced use cases |

### Domain-Based Emphasis

| Domain Focus | Content Emphasis |
|--------------|------------------|
| Software     | ROS 2 architecture, AI/ML integration, Python code examples, software design patterns |
| Hardware     | Robotics mechanics, sensor integration, actuator control, physical system design |
| Balanced     | Equal coverage of both domains with cross-domain integration examples |

### Personalization Rules

1. **Factual Integrity**: Original factual content MUST NOT be altered or contradicted
2. **Additive Approach**: Personalization adds context, examples, or simplifications; it does not remove core content
3. **Reversibility**: Users can always access original content via reset function
4. **Determinism**: Same user background + same content = same personalization output (given same model version)

## Urdu Translation Rules

### Translation Approach

1. Backend LLM processes translation with specialized prompts
2. Content is chunked appropriately for processing
3. Glossary rules are applied during translation

### Term Preservation Glossary

| English Term | Urdu Handling |
|--------------|---------------|
| ROS 2, ROS   | Keep as "ROS 2", "ROS" (transliterated: راس 2) |
| LIDAR        | Keep as "LIDAR" (transliterated: لائیڈار) |
| Neural Network | نیورل نیٹ ورک (transliteration preferred) |
| Robot        | روبوٹ (transliteration) |
| Sensor       | سینسر (transliteration) |
| Actuator     | ایکچویٹر (transliteration) |
| Python       | پائتھون (transliteration) |
| Algorithm    | الگورتھم (transliteration) |
| AI, ML       | Keep as "AI", "ML" with optional transliteration |
| Code blocks  | Preserve exactly as-is (English) |
| File paths   | Preserve exactly as-is |
| Commands     | Preserve exactly as-is |

### Translation Error Handling

1. If translation fails partially, return the successfully translated portion with error flag
2. Log all translation errors for debugging
3. Never display partially broken or malformed Urdu text to users
4. Provide "Translation unavailable" fallback with original content

## UI Specification

### Button Placement

The "Personalize Content" and "Translate to Urdu" buttons appear:
- At the top of each chapter page, below the chapter title
- In a horizontal button group with clear visual separation
- Styled consistently with Docusaurus theme

### Button States

| State | Personalize Button | Translate Button |
|-------|-------------------|------------------|
| Guest User | Hidden | Hidden |
| Logged in, no background | "Complete Profile" (links to questionnaire) | Hidden |
| Logged in, ready | "Personalize Content" (enabled) | "Translate to Urdu" (enabled) |
| Loading | "Personalizing..." (disabled, spinner) | "Translating..." (disabled, spinner) |
| Content personalized | "Reset to Original" | "Translate to Urdu" (enabled) |
| Content translated | "Personalize Content" | "Reset to Original" |

### Loading States

- Button shows spinner icon and text change during processing
- Content area may show subtle loading overlay
- Estimated time indicator for operations > 5 seconds

### Transformed Content Rendering

- Personalized/translated content replaces original in the same container
- All MDX formatting (headings, code blocks, lists, tables) preserved
- Right-to-left (RTL) text direction applied for Urdu content
- Reset button persists to restore original

## Integration Requirements

### Existing RAG Chatbot Compatibility

- Authentication state shared with chatbot context
- Personalization preferences may inform chatbot response style (future enhancement)
- Chatbot continues to work for unauthenticated users
- No blocking dependencies between chatbot and auth features

### FastAPI Backend Integration

- New auth routes added under /api/v1/auth/*
- New profile routes added under /api/v1/profile/*
- New content routes added under /api/v1/content/*
- Existing /api/v1/chat and other routes unchanged
- Shared database connection and configuration

### Neon Postgres Integration

- New tables created via migrations in backend/migrations/
- Foreign key relationships to users table
- Consistent UUID usage across all entities
- Timezone-aware timestamps

### Docusaurus Integration

- AuthProvider context wraps the app in Root.tsx
- NavbarAuth component in navbar for auth controls
- ChapterControls component injected in doc pages
- Custom DocItem layout to support chapter-level features
- Theme-consistent styling for all new components

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account registration (including background questionnaire) in under 3 minutes
- **SC-002**: 95% of signin attempts with valid credentials succeed within 2 seconds
- **SC-003**: Content personalization completes within 15 seconds for chapters under 10,000 words
- **SC-004**: Urdu translation completes within 15 seconds for chapters under 10,000 words
- **SC-005**: System supports at least 50 concurrent authenticated users without performance degradation
- **SC-006**: 90% of users successfully personalize or translate content on first attempt without errors
- **SC-007**: Zero security incidents related to authentication or session management
- **SC-008**: Personalized content maintains 100% factual accuracy compared to original
- **SC-009**: Translated content is comprehensible to native Urdu speakers (validated by sample review)
- **SC-010**: Existing RAG chatbot functionality remains fully operational after feature deployment

## Assumptions

1. **Better-Auth Compatibility**: Better-Auth library can be integrated with the existing FastAPI backend, or an equivalent JWT-based auth flow will be implemented that mirrors Better-Auth patterns
2. **LLM Availability**: Gemini API will be available for personalization and translation with sufficient quota
3. **Urdu Font Support**: Target browsers support Urdu script rendering (standard assumption for modern browsers)
4. **Content Length**: Typical chapters are under 10,000 words; longer chapters may require chunked processing
5. **User Base**: Primary users are students/developers familiar with technical content and registration flows
